import os
from Supplier_clustering.utils.logger import logger
from Supplier_clustering.entity.config_entity import DataValidationConfig
import pandas as pd




class DataValidation:
    def __init__(self, config: DataValidationConfig):
        self.config = config


    def validate_columns(self, data: pd.DataFrame) -> bool:
        """
        Validate that:
        1. No expected columns are missing.
        2. No unexpected columns are present.
        """

        expected_columns = set(self.config.all_schema.keys())
        actual_columns = set(data.columns)

        missing_columns = expected_columns - actual_columns
        extra_columns = actual_columns - expected_columns

        validation_status = True

        if missing_columns:
            print(f"Missing columns: {missing_columns}")
            validation_status = False

        if extra_columns:
            print(f"Unexpected columns: {extra_columns}")
            validation_status = False

        return validation_status

    def validate_datatypes(self, data: pd.DataFrame) -> bool:
        """
        Validate that the dataframe columns have
        the expected datatypes defined in schema.yaml.
        """

        validation_status = True

        for column, expected_dtype in self.config.all_schema.items():

            if column in data.columns:

                actual_dtype = str(data[column].dtype)

                if actual_dtype != expected_dtype:
                    print(
                        f"Datatype mismatch for '{column}': "
                        f"expected {expected_dtype}, "
                        f"got {actual_dtype}"
                    )

                    validation_status = False

        return validation_status

    def validate_all_columns(self) -> bool:
        """
        Run all data validation checks.
        """

        try:
            data = pd.read_csv(self.config.unzip_data_dir)

            columns_valid = self.validate_columns(data)

            datatypes_valid = self.validate_datatypes(data)

            validation_status = columns_valid and datatypes_valid

            with open(self.config.STATUS_FILE, "w") as f:
                f.write(f"Validation status: {validation_status}")

            return validation_status

        except Exception as e:
            raise e