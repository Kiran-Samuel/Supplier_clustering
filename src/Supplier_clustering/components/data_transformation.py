import os
from Supplier_clustering.utils.logger import logger
from Supplier_clustering.entity.config_entity import DataTransformationConfig
import pandas as pd
import numpy as np
import joblib
from sklearn.preprocessing import StandardScaler

class DataTransformation:

    def __init__(self, config):
        self.config = config

    def transform(self):

        # Load selected features
        df = pd.read_csv(self.config.input_data_path)

        logger.info("Loaded selected features")

        # Keep supplier ID separately
        supplier_ids = df["supplier_id"].copy()

        # Remove supplier ID from clustering features
        X = df.drop(columns=["supplier_id"]).copy()

        # Log transformations
        X["total_spend_log"] = np.log1p(X["total_spend"])
        X["order_frequency_log"] = np.log1p(X["order_frequency"])
        X["quality_rejection_rate_log"] = np.log1p(
            X["quality_rejection_rate"]
        )
        X["average_late_days_log"] = np.log1p(
            X["average_late_days"]
        )

        # Remove original features
        X = X.drop(
            columns=[
                "total_spend",
                "order_frequency",
                "quality_rejection_rate",
                "average_late_days"
            ]
        )

        logger.info("Log transformation completed")

        # Scale features
        scaler = StandardScaler()
        X_scaled = scaler.fit_transform(X)

        # Convert array back to DataFrame
        X_scaled = pd.DataFrame(
            X_scaled,
            columns=X.columns
        )

        # Add supplier ID back
        X_scaled.insert(
            0,
            "supplier_id",
            supplier_ids.reset_index(drop=True)
        )

        # Create root directory
        self.config.root_dir.mkdir(
            parents=True,
            exist_ok=True
        )

        # Save transformed dataset inside root_dir
        transformed_data_path = (
            self.config.root_dir / "transformed_data.csv"
        )

        X_scaled.to_csv(
            transformed_data_path,
            index=False
        )

        # Save scaler inside root_dir
        scaler_path = (
            self.config.root_dir / "scaler.joblib"
        )

        joblib.dump(
            scaler,
            scaler_path
        )

        logger.info(
            "Transformed dataset and scaler saved successfully"
        )

        return X_scaled