from Supplier_clustering.config.configuration import ConfigurationManager
from Supplier_clustering.components.data_transformation import DataTransformation
from Supplier_clustering.utils.logger import logger

STAGE_NAME = "Data Transformation stage"


class DataTransformationPipeline:
    def __init__(self):
        pass

    def main(self):

        config = ConfigurationManager()

        data_transformation_config = config.get_data_transformation_config()

        data_transformation = DataTransformation(
            config=data_transformation_config
        )

        data_transformation.transform()



#But if another file does:

#from data_transformation import DataTransformationPipeline

#the pipeline doesn't run immediately. It only imports the class.
if __name__ == '__main__':  # "Start executing this file from here if I personally ran this file."
    try:
        logger.info(f">>>>>> {STAGE_NAME} started <<<<<<")
        obj = DataTransformationPipeline()
        obj.main()
        logger.info(f">>>>>> {STAGE_NAME} completed <<<<<<\n\nx==========x")
    except Exception as e:
        logger.exception(e)
        raise e