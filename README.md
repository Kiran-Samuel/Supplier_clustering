# Supplier_clustering

# Workflow


1. Update config.yaml (locations of raw data, processed data, model, artifacts)
2. Update schema.yaml (columns and datatypes)
3. Update params.yaml (hyperparameters used in the project)
4. Update the entity/config_entity.py (return type of a function)
5. Update the configuration manager in src config
6. Update the components (data ingestion, data validation etc)
7. Update the pipeline (integrating all components separately for training and testing)
8. Update the main.py (Run all the stages of my machine-learning project in the correct order)
9. Update dvc.yaml (pipeline versioning/reproducibility)
10. Update the app.py (UI related functionality)

constants/__init__.py tells Python where the configuration is → 
config.yaml tells Python what values to use → 
config_entity shows the structure of those values in config.yaml
ConfigurationManager reads those values → 
DataIngestionConfig structures them → 
DataIngestion uses them to perform the work.