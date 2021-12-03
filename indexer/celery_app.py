from celery import Celery
from datetime import timedelta


app = Celery("tasks")
app.config_from_object("indexer.celery_config", namespace="CELERY")

# run index_files periodically every 1 minute
app.conf.beat_schedule = {
    "periodic_index_documents": {
        "task": "index_files",
        "schedule": timedelta(minutes=1)
    }
}
