import os
import numpy as np

#### docker version
LOCAL_TEST_DATA = os.environ.get("LOCAL_TEST_DATA")
SENTIMENT_MODEL_NAME = os.environ.get("SENTIMENT_MODEL_NAME")
CPU_BART_MODEL_NAME = os.environ.get("CPU_BART_MODEL_NAME")



LOCAL_TEST_DATA_PATH = os.path.join('data', LOCAL_TEST_DATA)
SENTIMENT_MODEL_PATH = os.path.join('ml_model', SENTIMENT_MODEL_NAME)
CPU_BART_MODEL_PATH = os.path.join('ml_model', CPU_BART_MODEL_NAME)
