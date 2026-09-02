from Supplier_clustering.config.configuration import ConfigurationManager
from Supplier_clustering.components.feature_selection import FeatureSelection
from Supplier_clustering.utils.logger import logger

STAGE_NAME = "Feature Selection stage"


class FeatureSelectionPipeline:
    def __init__(self):
        pass

    def main(self):

        config = ConfigurationManager()

        feature_selection_config = config.get_feature_selection_config()

        feature_selection = FeatureSelection(
            config=feature_selection_config
        )

        feature_selection.initiate_feature_selection()



#But if another file does:

#from feature_selection import FeatureSelectionPipeline

#the pipeline doesn't run immediately. It only imports the class.
if __name__ == '__main__':  # "Start executing this file from here if I personally ran this file."
    try:
        logger.info(f">>>>>> {STAGE_NAME} started <<<<<<")
        obj = FeatureSelectionPipeline()
        obj.main()
        logger.info(f">>>>>> {STAGE_NAME} completed <<<<<<\n\nx==========x")
    except Exception as e:
        logger.exception(e)
        raise e