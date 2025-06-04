from elasticsearch import Elasticsearch
from elasticsearch.exceptions import NotFoundError
import os

ES_HOST = os.getenv("ES_HOST", "elasticsearch")   # or localhost
ES_PORT = os.getenv("ES_PORT", 9200)

es = Elasticsearch(hosts=[{"host": ES_HOST, "port": ES_PORT,"scheme": "http"}])

def index_item(item: dict, item_id: str = None):
    return es.index(index="knowledgebase", id=item_id, document=item)

def get_item(item_id: str):
    try:
      return es.get(index="knowledgebase", id=item_id)
    except NotFoundError:
      return None  # or raise custom error

def get_items():
    return es.search(index="knowledgebase", body={"query": {"match_all": {}}})



def update_item(item_id: str, updated_fields: dict):
    return es.update(index="knowledgebase", id=item_id, doc={"doc": updated_fields})

def delete_item(item_id: str):
    return es.delete(index="knowledgebase", id=item_id)

def search_items(q: str, tags: list[str], language: str, page: int, size: int):
    must_clauses = []
    filter_clauses = []
    if q:
        must_clauses.append({
          "multi_match": {
            "query": q,
            "fields": ["title^2", "content"]
          }
        })
    if tags:
        filter_clauses.append({"terms": {"tags": tags}})
    if language:
        filter_clauses.append({"term": {"language": language}})

    body = {
      "query": {
        "bool": {
          "must": must_clauses or {"match_all": {}},
          "filter": filter_clauses
        }
      },
      "from": (page - 1) * size,
      "size": size
    }
    return es.search(index="knowledgebase", body=body)
