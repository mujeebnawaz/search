from flask import Flask
from elasticsearch import Elasticsearch

from config import ELASTICSEARCH_HOST, ELASTICSEARCH_PORT
flask_app = Flask(__name__)
es_client = Elasticsearch(hosts=[{"host": ELASTICSEARCH_HOST, "port": ELASTICSEARCH_PORT}])

from .api import query_api
