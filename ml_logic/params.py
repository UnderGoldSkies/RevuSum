import os
import numpy as np

#### docker version
LOCAL_TEST_DATA = os.environ.get("LOCAL_TEST_DATA")
SENTIMENT_MODEL_NAME = os.environ.get("SENTIMENT_MODEL_NAME")
PEGASUS_MODEL_NAME = os.environ.get("PEGASUS_MODEL_NAME")
PEGASUS_TOKENIZER_NAME = os.environ.get("PEGASUS_TOKENIZER")


LOCAL_TEST_DATA_PATH = os.path.join('data', LOCAL_TEST_DATA)
SENTIMENT_MODEL_PATH = os.path.join('ml_model', SENTIMENT_MODEL_NAME)
PEGASUS_MODEL_PATH = os.path.join('ml_model', PEGASUS_MODEL_NAME)
PEGASUS_TOKENIZER_PATH = os.path.join('ml_model', PEGASUS_TOKENIZER_NAME)
