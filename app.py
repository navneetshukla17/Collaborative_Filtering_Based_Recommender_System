import sys
import os

from Collaborative_Filtering_Based_Recommender_System.exception.exception_handler import AppException

try:
    a = 1 / 0
except Exception as e:
    raise AppException(e, sys) from e
