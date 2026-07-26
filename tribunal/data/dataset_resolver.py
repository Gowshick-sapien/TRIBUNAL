"""DatasetResolver — Centralized dataset reference resolution & registry for TRIBUNAL."""

from __future__ import annotations

import logging
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Dict, List, Optional

logger = logging.getLogger("tribunal.data.dataset_resolver")


try:
    from api.services.investigation_service import DatasetNotFoundError
except ImportError:
    class DatasetNotFoundError(Exception):
        """Raised when a dataset reference cannot be resolved or located."""

        def __init__(
            self,
            dataset_ref: str = "",
            message: Optional[str] = None,
            searched_locations: Optional[List[str]] = None,
            hint: Optional[str] = None,
        ) -> None:
            self.dataset_ref = dataset_ref
            self.searched_locations = searched_locations or []
            self.hint = (
                hint
                or "Expected a valid CSV/Parquet file path or a registered dataset alias (e.g., 'default', 'li_small', 'ibm_small')."
            )
            msg = message or f"Dataset '{dataset_ref}' could not be located."
            super().__init__(msg)


@dataclass
class DatasetMetadata:
    """Dataclass describing an available dataset."""
    id: str
    name: str
    description: str
    path: str
    default: bool = False
    record_count: Optional[int] = None


@dataclass
class ResolvedDataset:
    """Container holding resolved dataset path information."""
    ref_id: str
    resolved_path: Path
    is_file: bool
    metadata: Optional[DatasetMetadata] = None


# Canonical registry of supported datasets
DATASET_REGISTRY: Dict[str, DatasetMetadata] = {
    "default": DatasetMetadata(
        id="default",
        name="IBM AML Small (Default)",
        description="Default IBM AML transaction dataset",
        path="tribunal/datasets/LI-Small_Trans.csv",
        default=True,
    ),
    "li_small": DatasetMetadata(
        id="li_small",
        name="IBM AML Small CSV",
        description="IBM Laundering Small CSV transaction dataset",
        path="tribunal/datasets/LI-Small_Trans.csv",
        default=False,
    ),
    "ibm_small": DatasetMetadata(
        id="ibm_small",
        name="IBM Transactions Parquet",
        description="Optimized Parquet transaction dataset",
        path="tribunal/datasets/processed/transactions.parquet",
        default=False,
    ),
    "synthetic": DatasetMetadata(
        id="synthetic",
        name="Synthetic AML Demo",
        description="In-memory synthetic demonstration dataset",
        path="tribunal/datasets",
        default=False,
    ),
}


class DatasetResolver:
    """Centralized resolver converting dataset IDs or file paths into validated dataset files."""

    def __init__(self, base_dir: Optional[Path] = None) -> None:
        self.base_dir = base_dir or Path.cwd()
        self.registry = DATASET_REGISTRY

    def list_datasets(self) -> List[DatasetMetadata]:
        """Return list of available dataset metadata objects."""
        return list(self.registry.values())

    def resolve(self, dataset_ref: str) -> ResolvedDataset:
        """Resolve a dataset reference (alias ID or file/dir path) to a validated file or directory Path.
        
        Args:
            dataset_ref: Dataset alias ID (e.g. 'default', 'li_small') or filesystem path string.
            
        Returns:
            ResolvedDataset container with validated file/dir path.
            
        Raises:
            DatasetNotFoundError: If the dataset reference cannot be located.
        """
        if not dataset_ref or not dataset_ref.strip():
            dataset_ref = "default"

        dataset_ref_clean = dataset_ref.strip()
        searched_locations: List[str] = []

        # 1. Check registered alias
        meta: Optional[DatasetMetadata] = None
        target_path_str = dataset_ref_clean
        if dataset_ref_clean in self.registry:
            meta = self.registry[dataset_ref_clean]
            target_path_str = meta.path

        # 2. Convert to Path candidates
        raw_path = Path(target_path_str)
        candidates = [
            raw_path,
            self.base_dir / raw_path,
            Path(__file__).resolve().parent.parent.parent / raw_path,
        ]

        # STEP 1: Check if any candidate is a DIRECT FILE
        for cand in candidates:
            resolved = cand.expanduser().resolve()
            searched_locations.append(str(resolved))
            if resolved.exists() and resolved.is_file():
                logger.info(f"Resolved dataset '{dataset_ref}' directly to file: {resolved}")
                return ResolvedDataset(
                    ref_id=dataset_ref_clean,
                    resolved_path=resolved,
                    is_file=True,
                    metadata=meta,
                )

        # STEP 2: Only if NOT a file, search inside DIRECTORIES
        for cand in candidates:
            resolved = cand.expanduser().resolve()
            if resolved.exists() and resolved.is_dir():
                # Search subfolders for transaction data files
                dir_searches = [
                    resolved / "processed" / "transactions.parquet",
                    resolved / "raw" / "LI-Small_Trans.csv",
                    resolved / "LI-Small_Trans.csv",
                    resolved / "raw" / "transactions.csv",
                    resolved / "transactions.csv",
                ]
                for ds in dir_searches:
                    ds_resolved = ds.resolve()
                    searched_locations.append(str(ds_resolved))
                    if ds_resolved.exists() and ds_resolved.is_file():
                        logger.info(f"Resolved dataset directory '{dataset_ref}' to file: {ds_resolved}")
                        return ResolvedDataset(
                            ref_id=dataset_ref_clean,
                            resolved_path=ds_resolved,
                            is_file=True,
                            metadata=meta,
                        )

                # If directory exists but no standard subfiles, return directory itself
                logger.info(f"Resolved dataset '{dataset_ref}' to directory: {resolved}")
                return ResolvedDataset(
                    ref_id=dataset_ref_clean,
                    resolved_path=resolved,
                    is_file=False,
                    metadata=meta,
                )

        # Failure: Raise DatasetNotFoundError with searched locations
        logger.warning(f"Dataset '{dataset_ref}' could not be located. Searched: {searched_locations}")
        raise DatasetNotFoundError(
            dataset_ref=dataset_ref_clean,
            message=f"Dataset '{dataset_ref_clean}' could not be located.",
            searched_locations=searched_locations,
            hint="Expected a valid CSV/Parquet file path or a registered dataset alias (e.g., 'default', 'li_small', 'ibm_small').",
        )
