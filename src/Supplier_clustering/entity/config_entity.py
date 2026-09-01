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
    root_dir: Path  # where your output will be stored
    data_path: Path  # the location of the input data that Feature Engineering will read.