import yaml
import sys
from Collaborative_Filtering_Based_Recommender_System.exception.exception_handler import AppException

def read_yaml_file(file_path:str)->dict:
    """
    Reads a YAML file and returns its content as a dictionary.

    Parameters:
    file_path (str): The path to the YAML file.
    
    Returns:
    dict: The content of the YAML file.
    
    Raises:
    AppException: If there is an error reading the file.
    """
    try:
        with open(file_path, 'rb') as yaml_file:
            return yaml.safe_load(yaml_file)
    except Exception as e:
        raise AppException(e, sys) from e