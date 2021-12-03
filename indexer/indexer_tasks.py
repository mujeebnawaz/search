import hashlib
from os import walk

from elasticsearch import NotFoundError

from config import DOC_INDEX_NAME
from . import es_client, FILES_DIR
from .celery_app import app


@app.task(name="index_files")
def index_files():
    """
    Function to look at files in the specified directory and index/update them if required
    :return:
    """
    print("Periodic document indexing initiated")
    check_create_index()

    new_count = 0
    updated_count = 0
    up_to_date_count = 0

    files_list = []
    for (dirpath, dirnames, filenames) in walk(FILES_DIR):
        files_list.extend(list(map(lambda x: dirpath + "/" + x, filenames)))

    print("Documents found: {}".format(', '.join(files_list)))
    for file in files_list:
        print("Indexing document '{}'".format(file))

        file_name = file.split("/")[-1]
        with open(file, "r") as data:
            text = data.read()

        sha = hashlib.sha256(text.encode()).hexdigest()
        body = {
            "text": text,
            "hash": sha,
            "title": file_name
        }
        body_ = {
            "query": {
                "bool": {
                    "must": [
                        {"match": {"title": file_name}},
                    ]
                }
            }
        }
        existing_doc = es_client.search(body=body_, index=DOC_INDEX_NAME, params={"_source": "hash"})
        if not existing_doc["hits"]["hits"]:
            new_count += 1
            print("Indexing new document '{}'".format(file_name))
            es_client.index(DOC_INDEX_NAME, body=body)
        else:
            if existing_doc["hits"]["hits"][0]["_source"]["hash"] == sha:
                up_to_date_count += 1
                print("Document '{}' already indexed and up to date".format(file_name))
                continue

            updated_count += 1
            es_client.index(DOC_INDEX_NAME, body)
            print("Document '{}' updated".format(file_name))

    print("Indexing Summary:\nNew Documents: {}\nUpdated Documents: {}\nUp to date Documents: {}".format(
        str(new_count), str(updated_count), str(up_to_date_count)))


def check_create_index():
    """
    Check if the index to store documents exists. If it does not, create it
    :return:
    """
    body = {
        "mappings": {
            "properties": {
                "title": {
                    "type": "text",
                },
                "text": {
                    "type": "text",
                    "term_vector": "with_positions_offsets",
                    "store": True,
                    "analyzer": "fulltext_analyzer",
                    "fields": {
                        "w_synonyms": {
                            "type": "text",
                            "analyzer": "fulltext_analyzer_syn"
                        }
                    }
                },
                "hash": {
                    "type": "text"
                }
            }
        },
        "settings": {
            "index": {
                "number_of_shards": 1,
                "number_of_replicas": 0
            },
            "analysis": {
                "analyzer": {
                    "fulltext_analyzer": {
                        "type": "custom",
                        "tokenizer": "standard",
                        "filter": [
                            "lowercase",
                            "stop",
                            "snowball"
                        ]
                    },
                    "fulltext_analyzer_syn": {
                        "type": "custom",
                        "tokenizer": "standard",
                        "filter": [
                            "lowercase",
                            "stop",
                            "snowball",
                            "synonym"
                        ]
                    }
                },
                "filter": {
                    "synonym": {
                        "type": "synonym",
                        "synonyms": ["cat, dog, animal",
                                     "computer, technology, laptop, cell, phone, telephone, cellular, tele, cellphone",
                                     "mammal, beluga, narwhal, orca, whale, cete, animal, desert",
                                     "drugs, smart, smart drug, brain, power, medicine, dose, needle, booster, inoculation" ,
                                     "country, region, first, world, western, great britain, ireland, england, wales, scotland, bharat, nation" ,
                                     "severe, acute, respiratory, syndrome, disease, middle, east, virus, novel, strain, death, lungs, chest, flu"]
                    }
                }
            }
        }
    }
    print("Checking if index '{}' exists".format(DOC_INDEX_NAME))
    try:
        es_client.indices.get(DOC_INDEX_NAME)
        print("Index '{}' exists".format(DOC_INDEX_NAME))
    except NotFoundError:
        es_client.indices.create(index=DOC_INDEX_NAME, body=body)
        print("New index '{}' created".format(DOC_INDEX_NAME))
