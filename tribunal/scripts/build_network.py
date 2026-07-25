"""CLI script to build, validate, profile, and persist the Transaction Network MultiDiGraph.

Usage:
    python -m tribunal.scripts.build_network
"""

import logging
import sys
from pathlib import Path

# Setup path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent))

from tribunal.investigation.transaction_network_builder import TransactionNetworkBuilder

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
logger = logging.getLogger("build_network")


def main():
    dataset_path = "datasets"
    if not Path(dataset_path).exists() and Path("tribunal/datasets").exists():
        dataset_path = "tribunal/datasets"

    logger.info("Initializing Transaction Network Builder...")
    builder = TransactionNetworkBuilder(dataset_path)
    
    # 1. Build Graph
    logger.info("Building NetworkX MultiDiGraph from processed Parquet datasets...")
    graph = builder.build()
    
    # 2. Validate Graph
    logger.info("Running Network Validation...")
    val_report = builder.validate()
    logger.info(f"Validation Status: {val_report['status']}")
    
    # 3. Compute Network Statistics
    logger.info("Computing Network Topology Statistics...")
    stats = builder.get_network_statistics()
    logger.info(f"Total Nodes: {stats['total_nodes']:,}")
    logger.info(f"Total Edges: {stats['total_edges']:,}")
    logger.info(f"Weakly Connected Components: {stats['weakly_connected_components_count']:,}")
    logger.info(f"Largest Weak Component Size: {stats['largest_weak_component_size']:,}")
    
    # 4. Save Persisted Graph
    saved_path = builder.save()
    logger.info(f"Transaction Network successfully built and persisted to: {saved_path}")


if __name__ == "__main__":
    main()
