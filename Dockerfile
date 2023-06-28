#2nd edition
FROM python:3.10.6-buster

ENV LANG=en_US.UTF-8
ENV LANGUAGE=en_US:en
ENV LC_ALL=en_US.UTF-8

RUN apt-get update && apt-get install -y locales && \
    locale-gen en_US.UTF-8

COPY . /app
WORKDIR /app

RUN pip install --upgrade setuptools pip && \
    pip install -r requirements.txt && \
    pip install nltk yake transformers sentencepiece torch pegasus distilbert-punctuator && \
    python -m nltk.downloader -d /home/nltk_data stopwords punkt wordnet

CMD uvicorn api.fast:app --host 0.0.0.0 --port $PORT


#original first try
# FROM python:3.10.6-buster

# ENV LANG=en_US.UTF-8
# ENV LANGUAGE=en_US:en
# ENV LC_ALL=en_US.UTF-8

# COPY requirements.txt /requirements.txt
# COPY interface /interface
# COPY new_data /data
# COPY api /api
# COPY ml_logic /ml_logic
# COPY ml_model /ml_model
# COPY .env /.env
# COPY .env.yaml /.env.yaml
# COPY .envrc /.envrc
# COPY setup.py /setup.py
# COPY home /home

# RUN apt-get update && apt-get install -y locales
# RUN locale-gen en_US.UTF-8
# RUN pip install nltk
# RUN pip install yake
# RUN pip install transformers
# RUN pip install sentencepiece
# RUN pip install --upgrade torch transformers pegasus
# RUN pip install distilbert-punctuator
# RUN python -m nltk.downloader stopwords
# RUN python -m nltk.downloader punkt
# RUN python -m nltk.downloader wordnet

# RUN pip install --upgrade setuptools
# RUN pip install --upgrade pip
# RUN pip install -r requirements.txt
# RUN python setup.py install

# CMD uvicorn api.fast:app --host 0.0.0.0 --port $PORT




#3rd edition haven try yet
# FROM python:3.10.6-buster

# ENV LANG=en_US.UTF-8
# ENV LANGUAGE=en_US:en
# ENV LC_ALL=en_US.UTF-8

# COPY requirements.txt /requirements.txt
# COPY interface /interface
# COPY new_data /data
# COPY api /api
# COPY ml_logic /ml_logic
# COPY ml_model /ml_model
# COPY .env /.env
# COPY .env.yaml /.env.yaml
# COPY .envrc /.envrc
# COPY setup.py /setup.py
# COPY home /home

# RUN pip install --upgrade setuptools pip && \
#     pip install -r requirements.txt && \
#     pip install nltk yake transformers sentencepiece torch pegasus distilbert-punctuator && \
#     python -m nltk.downloader stopwords punkt wordnet \
#     python setup.py install

# # Install NLTK stopwords, punkt, and wordnet
# RUN python -c "import nltk; nltk.download('stopwords'); nltk.download('punkt'); nltk.download('wordnet')"

# CMD uvicorn api.fast:app --host 0.0.0.0 --port $PORT
