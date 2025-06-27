import os
from pathlib import Path
import logging

logging.basicConfig(level=logging.INFO, format='[%(asctime)s]: %(message)s:')
project_name = "Collaborative-Filtering-Based-Recommender-System"

list_of_files = [
    f"{project_name}/__init__.py",
    f"{project_name}/components/__init__.py",
    f"{project_name}/components/stage_01_data_ingestion.py",
    f"{project_name}/components/stage_02_data_validation.py",
    f"{project_name}/components/stage_03_data_transformation.py",
    f"{project_name}/components/stage_04_model_trainer.py",
    f"{project_name}/config/__init__.py",
    f"{project_name}/config/configuration.py",
    f"{project_name}/constant/__init__.py",
    f"{project_name}/entity/__init__.py",
    f"{project_name}/entity/config_entity.py",
    f"{project_name}/exception/__init__.py",
    f"{project_name}/exception/exception_handler.py",
    f"{project_name}/logger/__init__.py",
    f"{project_name}/logger/log.py",
    f"{project_name}/pipeline/__init__.py",
    f"{project_name}/pipeline/training_pipeline.py",
    f"{project_name}/utils/__init__.py",
    f"{project_name}/utils/util.py",
    ".dockerignore",
    "app.py",
    "Dockerfile",
    "setup.py"
]

for file_path in list_of_files:
    file_path = Path(file_path)
    filedir, filename = os.path.split(file_path)

    if filedir != "":
        os.makedirs(filedir, exist_ok=True)
        logging.info(f"Creating empty file: {filename} for the file: {filename}")
    if (not os.path.exists(filename)) or (os.path.getsize(filename) == 0):
        with open(file_path, 'w') as f:
            pass
            logging.info(f"Creating empty file: {filename}")
    else:
        logging.info(f"{filename} is already created")


