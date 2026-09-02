from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True)
class DataIngestionConfig:
    root_dir: Path
    source_URL: str
    local_data_file: Path
    unzip_dir: Path

@dataclass(frozen=True)
class DataValidationConfig:
    root_dir: Path
    STATUS_FILE: str
    unzip_data_dir: Path
    all_schema: dict

@dataclass(frozen=True)
class FeatureEngineeringConfig:
    # These values are set in the config.yaml file and passed to the FeatureEngineeringConfig class
    root_dir: Path  
    data_path: Path

@dataclass(frozen=True)
class FeatureSelectionConfig:
    # These values are set in the config.yaml file and passed to the FeatureSelectionConfig class
    root_dir: Path  # where the selected features will be saved
    input_data_path: Path  # where the input data for feature selection is located

@dataclass(frozen=True)
class DataTransformationConfig:
    # These values are set in the config.yaml file and passed to the DataTransformationConfig class
    root_dir: Path  # where the transformed data will be saved
    input_data_path: Path  # where the input data for transformation is located