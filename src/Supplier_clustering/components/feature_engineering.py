import os
from Supplier_clustering.utils.logger import logger
from Supplier_clustering.entity.config_entity import FeatureEngineeringConfig
import pandas as pd

class FeatureEngineering:

    def __init__(self, config: FeatureEngineeringConfig):
        self.config = config

    def engineer_features(self):

        # ---------------------------------------------------------
        # 1. Read cleaned data
        # ---------------------------------------------------------
        data = pd.read_csv(self.config.data_path)

        logger.info(f"Input data shape: {data.shape}")

        # ---------------------------------------------------------
        # 2. Calculate supplier-level features
        # ---------------------------------------------------------

        date_columns=['order_date','promised_delivery_date','actual_delivery_date']

        for col in date_columns:
            data[col] = pd.to_datetime(data[col])

        data['delivery_delay'] = (data['actual_delivery_date'] - data['promised_delivery_date']).dt.days

        # Total spend per supplier
        total_spend = (
            data.groupby("supplier_id")["line_total"]
            .sum()
        )

        # Number of orders per supplier
        order_frequency = (
            data.groupby("supplier_id")["po_id"]
            .nunique()
        )

        # Average delivery delay per supplier
        average_delivery_delay = (
            data.groupby("supplier_id")["delivery_delay"]
            .mean()
        )

        # Quality rejection rate
        quality_rejection_rate = (
            data.groupby("supplier_id")["quality_rejected"]
            .mean()
        )

        data['on_time'] = data['delivery_delay'].apply(lambda x: 1 if x<=0 else 0)

        # On-time delivery rate
        on_time_delivery_rate = (
            data.groupby("supplier_id")["on_time"]
            .mean()
        )

        # Late days
        # Average late days → When they are late, how severe is the delay?
        data["late_days"] = data["delivery_delay"].clip(lower=0)
        average_late_days = (data.groupby("supplier_id")["late_days"].mean().rename("average_late_days"))

        # ---------------------------------------------------------
        # 3. Price competitiveness
        # ---------------------------------------------------------
        item_avg_price = data.groupby('item')['unit_price'].mean().reset_index().rename(columns={"unit_price": "item_avg_price"})
        #
        # price_ratio = supplier price / average item price
        data = data.merge(item_avg_price, on='item', how='left')
        data['price_ratio']= data['unit_price']/data['item_avg_price']
        #
        # Lower value = more price competitive
        # Around 1 = close to market average
        # Higher value = more expensive
        #
        price_competitiveness = (
            data.groupby("supplier_id")["price_ratio"]
            .mean()
        )

        # ---------------------------------------------------------
        # 4. Cost variability
        # ---------------------------------------------------------
        #
        # Calculate coefficient of variation of supplier prices.
        #
        # CV = standard deviation / mean
        #
        data["item_supplier_price_cv"] = (
            data.groupby(["supplier_id", "item"])["unit_price"]
            .transform(lambda x: x.std() / x.mean() if x.mean() != 0 else 0)
        )
        cost_variability = (
            data.groupby("supplier_id")["item_supplier_price_cv"].mean())

        # ---------------------------------------------------------
        # 5. Create supplier-level dataset
        # ---------------------------------------------------------

        engineered_data = pd.DataFrame({
            "supplier_id": total_spend.index,

            "price_competitiveness":
                price_competitiveness.reindex(total_spend.index),

            "cost_variability":
                cost_variability.reindex(total_spend.index),

            "total_spend":
                total_spend,

            "order_frequency":
                order_frequency.reindex(total_spend.index),

            "average_delivery_delay":
                average_delivery_delay.reindex(total_spend.index),

            "quality_rejection_rate":
                quality_rejection_rate.reindex(total_spend.index),

            "on_time_delivery_rate":
                on_time_delivery_rate.reindex(total_spend.index),

            "average_late_days":
                average_late_days.reindex(total_spend.index)
        })

        # ---------------------------------------------------------
        # 6. Reset index
        # ---------------------------------------------------------

        engineered_data = engineered_data.reset_index(drop=True)

        logger.info(
            f"Supplier-level feature shape: {engineered_data.shape}"
        )

        logger.info(
            f"Supplier-level features created: "
            f"{list(engineered_data.columns)}"
        )

        # ---------------------------------------------------------
        # 7. Check missing values
        # ---------------------------------------------------------

        if engineered_data.isnull().sum().sum() > 0:

            logger.warning(
                "Missing values detected in supplier features"
            )

            logger.warning(
                engineered_data.isnull().sum()
            )

        # ---------------------------------------------------------
        # 8. Save engineered features
        # ---------------------------------------------------------

        engineered_data.to_csv(
            os.path.join(
                self.config.root_dir,
                "engineered_data.csv"
            ),
            index=False
        )

        logger.info(
            "Engineered features saved successfully"
        )

        print(engineered_data.head())
        print(engineered_data.shape)

        return engineered_data