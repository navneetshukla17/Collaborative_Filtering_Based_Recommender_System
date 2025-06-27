import sys
import os
from Collaborative_Filtering_Based_Recommender_System.exception.exception_handler import AppException
from Collaborative_Filtering_Based_Recommender_System.logger.log import logging

try:
    a = 1 / 0
except Exception as e:
    logging.info(e)
    raise AppException(e, sys) from e
