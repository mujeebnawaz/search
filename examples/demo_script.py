import urllib.parse

from requests import request
from pprint import pprint

server_ip = "159.89.84.20"

queries = [
    "Dogs with cats!",
    "What do cats eat?",
    "What is the other name for england",
]

for query in queries:
    print("\n\n\n*****")
    print("Query: ", query)
    print("Response:")
    response = request("GET", "http://{server_ip}:5000/query?q={query}".format(
        server_ip=server_ip,
        query=urllib.parse.quote(query)
    ))
    for item in response.json():
        pprint(item)

