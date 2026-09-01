import os
from Supplier_clustering.utils.logger import logger
from Supplier_clustering.entity.config_entity import FeatureSelectionConfig
import pandas as pd

class FeatureSelection:

    def __init__(self, config: FeatureSelectionConfig):
        self.config = config

    # ---------------------------------------------------------
    # Descriptive Statistics
    # ---------------------------------------------------------

    def analyze_descriptive_statistics(
        self,
        df: pd.DataFrame
    ) -> pd.DataFrame:

        return df.describe().T

    # ---------------------------------------------------------
    # Skewness
    # ---------------------------------------------------------

    def analyze_skewness(
        self,
        df: pd.DataFrame
    ) -> pd.Series:

        return df.skew().sort_values()

    # ---------------------------------------------------------
    # Outlier Detection
    # ---------------------------------------------------------

    def detect_outliers(
        self,
        df: pd.DataFrame
    ) -> dict:

        outlier_results = {}

        for col in df.columns:

            Q1 = df[col].quantile(0.25)
            Q3 = df[col].quantile(0.75)

            IQR = Q3 - Q1

            lower_bound = Q1 - 1.5 * IQR
            upper_bound = Q3 + 1.5 * IQR

            outliers = df[
                (df[col] < lower_bound) |
                (df[col] > upper_bound)
            ]

            outlier_results[col] = {
                "Q1": Q1,
                "Q3": Q3,
                "IQR": IQR,
                "lower_bound": lower_bound,
                "upper_bound": upper_bound,
                "number_of_outliers": len(outliers)
            }

        return outlier_results

    # ---------------------------------------------------------
    # Correlation Analysis
    # ---------------------------------------------------------

    def analyze_correlation(
        self,
        df: pd.DataFrame
    ) -> pd.DataFrame:

        return df.corr()

    # ---------------------------------------------------------
    # Final Feature Selection
    # ---------------------------------------------------------

    def select_features(
        self,
        df: pd.DataFrame
    ) -> pd.DataFrame:

        selected_features = [
            "price_competitiveness",
            "cost_variability",
            "total_spend",
            "order_frequency",
            "quality_rejection_rate",
            "average_late_days"
        ]

        return df[selected_features]

    # ---------------------------------------------------------
    # Main Feature Selection Pipeline
    # ---------------------------------------------------------

    def initiate_feature_selection(self) :

        df = pd.read_csv(self.config.input_data_path)

        logger.info("Starting feature selection")

        # Create feature-selection artifact directory
        self.config.root_dir.mkdir(
            parents=True,
            exist_ok=True
        )

        # -----------------------------------------------------
        # Keep supplier_id as identifier
        # -----------------------------------------------------

        supplier_ids = df[["supplier_id"]].copy()

        # -----------------------------------------------------
        # Remove supplier_id from feature analysis
        # -----------------------------------------------------

        feature_data = df.drop(
            columns=["supplier_id"]
        )

        # -----------------------------------------------------
        # 1. Descriptive Statistics
        # -----------------------------------------------------

        statistics = self.analyze_descriptive_statistics(
            feature_data
        )

        statistics.to_csv(
            self.config.root_dir /
            "descriptive_statistics.csv"
        )

        # -----------------------------------------------------
        # 2. Skewness
        # -----------------------------------------------------

        skewness = self.analyze_skewness(
            feature_data
        )

        skewness.to_csv(
            self.config.root_dir /
            "skewness.csv",
            header=["skewness"]
        )

        # -----------------------------------------------------
        # 3. Outlier Analysis
        # -----------------------------------------------------

        outliers = self.detect_outliers(
            feature_data
        )

        outlier_df = pd.DataFrame(
            outliers
        ).T

        outlier_df.to_csv(
            self.config.root_dir /
            "outlier_analysis.csv"
        )

        # -----------------------------------------------------
        # 4. Correlation Analysis
        # -----------------------------------------------------

        correlation = self.analyze_correlation(
            feature_data
        )

        correlation.to_csv(
            self.config.root_dir /
            "correlation_matrix.csv"
        )

        # -----------------------------------------------------
        # 5. Select Final Features
        # -----------------------------------------------------

        selected_features = self.select_features(
            feature_data
        )

        # -----------------------------------------------------
        # Add supplier_id back as identifier
        # -----------------------------------------------------

        final_data = pd.concat(
            [
                supplier_ids,
                selected_features
            ],
            axis=1
        )

        # -----------------------------------------------------
        # 6. Save Final Selected Dataset
        # -----------------------------------------------------

        final_data.to_csv(
                    os.path.join(
                        self.config.root_dir,
                        "selected_features.csv"
                    ),
                    index=False
                )

        logger.info(
            "Feature selection completed successfully"
        )

        logger.info(
            f"Final selected features: "
            f"{list(selected_features.columns)}"
        )

        logger.info(
            f"Final dataset shape: {final_data.shape}"
        )

        print("\nFinal Selected Features:")
        print(selected_features.columns.tolist())

        print("\nFinal Dataset:")
        print(final_data.head())

        print("\nFinal Dataset Shape:")
        print(final_data.shape)

        return final_data