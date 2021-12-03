from flask import request, Response, jsonify
from elasticsearch import NotFoundError
from elasticsearch_dsl import Search
from elasticsearch_dsl.query import MultiMatch

from config import DOC_INDEX_NAME
from web_server import es_client, flask_app


@flask_app.route("/query", methods=["GET"])
def query_api():
    """
    API for querying
    :return:
    """
    query = request.args.get('q')
    if not query:
        return Response("No query specified", status=400)

    query_search = Search(using=es_client, index=DOC_INDEX_NAME).query(
        MultiMatch(query=query, fields=['text', 'text.w_synonyms'], fuzziness='AUTO'))

    resp = query_search.execute()

    return_docs = [{"id": hit.meta.id, "title": hit.title, "score": hit.meta.score} for hit in resp]
    return jsonify(return_docs)


@flask_app.route("/doc/<doc_id>", methods=["GET"])
def get_doc(doc_id):
    """
    API to return documents
    :param doc_id:
    :return:
    """
    try:
        doc = es_client.get(DOC_INDEX_NAME, doc_id)
    except NotFoundError:
        return Response(status=404)

    return jsonify({"title": doc["_source"]["title"], "text": doc["_source"]["text"]})
