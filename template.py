import os
from pathlib import Path
import logging

logging.basicConfig(level=logging.INFO, format='[%(asctime)s]: %(message)s:')

project_name = "Supplier_clustering"

list_of_files = [
    ".github/workflows/.gitkeep",
    f"src/{project_name}/__init__.py",
    f"src/{project_name}/components/data_ingestion.py",
    f"src/{project_name}/components/data_validation.py",
    f"src/{project_name}/components/feature_engineering.py",
    f"src/{project_name}/components/feature_selection.py",
    f"src/{project_name}/components/data_transformation.py",
    f"src/{project_name}/components/model_trainer.py",
    f"src/{project_name}/components/model_evaluation.py",
    f"src/{project_name}/utils/__init__.py",
    f"src/{project_name}/utils/common.py",
    f"src/{project_name}/utils/custom_exceptions.py",
    f"src/{project_name}/utils/logger.py",
    f"src/{project_name}/config/__init__.py",
    f"src/{project_name}/config/configuration.py",
    f"src/{project_name}/pipeline/stage_01_data_ingestion.py",
    f"src/{project_name}/pipeline/stage_02_data_validation.py",
    f"src/{project_name}/pipeline/stage_03_feature_engineering.py",
    f"src/{project_name}/pipeline/stage_04_feature_selection.py",
    f"src/{project_name}/pipeline/stage_05_data_transformation.py",
    f"src/{project_name}/pipeline/stage_06_model_trainer.py",
    f"src/{project_name}/pipeline/stage_07_model_evaluation.py",
    f"src/{project_name}/entity/__init__.py",
    f"src/{project_name}/entity/config_entity.py",
    f"src/{project_name}/constants/__init__.py",
    "config/config.yaml",
    "params.yaml",
    "schema.yaml",
    "dvc.yaml",
    "main.py",
    "app.py",
    "Dockerfile",
    "requirements.txt",
    "setup.py",
    "research/01_data_ingestion.ipynb",
    "research/02_data_validation.ipynb",
    "research/03_feature_engineering.ipynb",
    "research/04_feature_selection.ipynb",
    "research/05_data_transformation.ipynb",
    "research/06_model_trainer.ipynb",
    "research/07_model_evaluation.ipynb",
    "research/trials.ipynb",
    "templates/index.html",
    "test.py"

]



for filepath in list_of_files:
    filepath = Path(filepath)
    filedir, filename = os.path.split(filepath)

    if filedir !="":
        os.makedirs(filedir, exist_ok=True)
        logging.info(f"Creating directory; {filedir} for the file: {filename}")

    if (not os.path.exists(filepath)) or (os.path.getsize(filepath) == 0):
        with open(filepath, "w") as f:
            pass
            logging.info(f"Creating empty file: {filepath}")

    else:
        logging.info(f"{filename} is already exists")

