import os

from elasticsearch import Elasticsearch

from config import ELASTICSEARCH_HOST, ELASTICSEARCH_PORT


es_client = Elasticsearch(hosts=[{"host": ELASTICSEARCH_HOST, "port": ELASTICSEARCH_PORT}])
FILES_DIR = os.environ.get("FILES_DIR")

from .indexer_tasks import index_files
