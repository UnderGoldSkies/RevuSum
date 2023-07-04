import os
import numpy as np

#### docker version
LOCAL_TEST_DATA = os.environ.get("LOCAL_TEST_DATA")
SENTIMENT_MODEL_NAME = os.environ.get("SENTIMENT_MODEL_NAME")
GOOGLE_CREDENTIAL = os.environ.get("GOOGLE_APPLICATION_CREDENTIALS")

LOCAL_TEST_DATA_PATH = os.path.join('data', LOCAL_TEST_DATA)
SENTIMENT_MODEL_PATH = os.path.join('ml_model', SENTIMENT_MODEL_NAME)
GOOGLE_CREDENTIAL_PATH = os.path.join(os.path.dirname(__file__), '..', 'gcp', os.path.basename(GOOGLE_CREDENTIAL))
