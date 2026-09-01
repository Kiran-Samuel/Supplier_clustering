# tells your pipeline which stages to run and in what order.
from Supplier_clustering.utils.logger import logger
from Supplier_clustering.pipeline.stage_01_data_ingestion import DataIngestionTrainingPipeline
from Supplier_clustering.pipeline.stage_02_data_validation import DataValidationTrainingPipeline
from Supplier_clustering.pipeline.stage_03_feature_engineering  import FeatureEngineeringPipeline

STAGE_NAME = "Data Ingestion stage"
try:
    logger.info(f">>>>>> {STAGE_NAME} started <<<<<<")
    obj = DataIngestionTrainingPipeline()
    obj.main()
    logger.info(f">>>>>> {STAGE_NAME} completed <<<<<<\n\nx==========x")
except Exception as e:
    logger.exception(e)
    raise e

STAGE_NAME = "Data Validation stage"
try:
    logger.info(f">>>>>> {STAGE_NAME} started <<<<<<")
    obj = DataValidationTrainingPipeline()
    obj.main()
    logger.info(f">>>>>> {STAGE_NAME} completed <<<<<<\n\nx==========x")
except Exception as e:
    logger.exception(e)
    raise e

STAGE_NAME = "Feature Engineering stage"

try:
        
    logger.info(f">>>>>> {STAGE_NAME} started <<<<<<")
    obj = FeatureEngineeringPipeline()
    obj.main()
    logger.info(f">>>>>> {STAGE_NAME} completed <<<<<<\n\nx==========x")
except Exception as e:
    logger.exception(e)
    raise e