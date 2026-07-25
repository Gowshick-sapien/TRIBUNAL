"""CLI script to build, validate, profile, and persist the Feature Store.

Usage:
    python -m tribunal.scripts.build_feature_store
"""

import logging
import sys
from pathlib import Path

# Setup path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent))

from tribunal.tools.feature_store_builder import FeatureStoreBuilder

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
logger = logging.getLogger("build_feature_store")


def main():
    dataset_path = "datasets"
    if not Path(dataset_path).exists() and Path("tribunal/datasets").exists():
        dataset_path = "tribunal/datasets"

    logger.info("Initializing Feature Store Builder...")
    builder = FeatureStoreBuilder(dataset_path)

    # 1. Build Feature Store
    logger.info("Building Feature Store across financial, behavioural, network, temporal, statistical, and rule-ready categories...")
    feature_df = builder.build()

    # 2. Validate Feature Store
    logger.info("Running Feature Store Validation...")
    val_report = builder.validate()
    logger.info(f"Validation Status: {val_report['status']}")

    # 3. Compute Profile Statistics
    logger.info("Computing Feature Store Profile Statistics...")
    profile = builder.get_feature_profile()
    logger.info(f"Total Accounts Processed: {profile['accounts_processed']:,}")
    logger.info(f"Total Features per Account: {profile['feature_count']}")
    logger.info(f"High Structuring Risk Accounts (>0.5): {profile['high_structuring_risk_accounts_count']:,}")

    # 4. Save Feature Store Parquet
    saved_path = builder.save()
    logger.info(f"Feature Store successfully built and persisted to: {saved_path}")


if __name__ == "__main__":
    main()
