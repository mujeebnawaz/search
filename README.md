# Search
Information Retrieval Model Based on Elastic Search and Docker. 

### Requirements:
- Docker and docker-compose installed on the host
    - https://docs.docker.com/engine/install/ubuntu/ (docker)
    - https://docs.docker.com/compose/install/
- Port 5000 to be available

** Note: Unix based OS is preferred, however, since Search Engine is docker based 
the Search Engine will be functional on any OS. **

### Running the Application.

In the terminal, go to the root of the project and type:
`docker-compose up -d`

This will run the application and install / download all of the dependencies required in the containers.
This will not install anything on the host system.

To confirm the successful installations, run 
```docker-compose ps```

The output should look like this:
```         Name                       Command               State                    Ports                 
---------------------------------------------------------------------------------------------------------
groupi_elasticsearch_1   /usr/local/bin/docker-entr ...   Up      9200/tcp, 9300/tcp                     
groupi_rabbitmq_1        docker-entrypoint.sh rabbi ...   Up      25672/tcp, 4369/tcp, 5671/tcp, 5672/tcp
groupi_scheduler_1       celery -A indexer.celery_a ...   Up                                             
groupi_web_server_1      python run_web_server.py         Up      0.0.0.0:5000->5000/tcp                 
groupi_worker_1          celery -A indexer.celery_a ...   Up                                             
```

Double check that all containers are UP.

With this your app should be up and running. You can use any http client like postman or 
google chrome to interact with the app.

The web server is running on the host on port 5000 and has two API Endpoints with the following API Docs

---

##### Query API
**Description:** Query from the search engine

**Method:** GET

**Route:** /query

**Params:** 
- q (for query)

**Response:** List of json objects containing the id of the document, title of the document, 
and the relevance score

**Example:**

For querying 'dog and cat'

GET http://localhost:5000/query?q=dog+and+cat

Response
```
[{
	"id": "ZUiuhHEB25J9ZSBzeZIU",
	"score": 4.801333,
	"title": "06AnimalCamel.txt"
}, {
	"id": "qRz0gnEB0dyYazvy843x",
	"score": 4.300805,
	"title": "document3"
}, {
	"id": "qBz0gnEB0dyYazvy843X",
	"score": 4.0984063,
	"title": "document1"
}, {
	"id": "qhz0gnEB0dyYazvy9I0B",
	"score": 4.0984063,
	"title": "document4"
}, {
	"id": "qxz0gnEB0dyYazvy9I0b",
	"score": 4.0984063,
	"title": "document2"
}, {
	"id": "bkiuhHEB25J9ZSBzepIC",
	"score": 4.008063,
	"title": "04AnimalDolphins.txt"
}, {
	"id": "cUiuhHEB25J9ZSBzepIv",
	"score": 3.9867494,
	"title": "05AnimalMeerkat.txt"
}, {
	"id": "Z0iuhHEB25J9ZSBzeZJ6",
	"score": 2.3243575,
	"title": "08MedAntibiotics.txt"
}, {
	"id": "aUiuhHEB25J9ZSBzeZKo",
	"score": 2.2762318,
	"title": "09MedVaccinations.txt"
}, {
	"id": "bUiuhHEB25J9ZSBzeZL2",
	"score": 1.5467865,
	"title": "03DevicesMobileGoogle.txt"
}]
```

---
##### Get Document API
**Description:** Get a document's text and title by ID

**Method:** GET

**Route:** /doc/<doc_id>

**Response:** A json object containing the title of the document, and the text

**Example:**

For querying 'dog and cat'

GET http://localhost:5000/doc/qRz0gnEB0dyYazvy843x

Response
```
{
	"text": "this document is about cats and dogs both",
	"title": "document3"
}
```

---
### Demonstration:
#### Requirements

- Python 3.x
- pip3
- Requests package via pip

In the example folder run demo_scipt.py with `python3 demo_scrypt.py`
