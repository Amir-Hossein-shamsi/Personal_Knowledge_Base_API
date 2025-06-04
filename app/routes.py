from fastapi import APIRouter, HTTPException, Query
from pydantic import BaseModel
from typing import List, Optional
from uuid import uuid4
from datetime import datetime
from utils import index_item, get_item, get_items, update_item, delete_item, search_items

router = APIRouter(prefix="/api/v1", tags=["items"])

class ItemSchema(BaseModel):
    title: str
    content: str
    tags: Optional[List[str]] = []
    language: str

@router.get("/status", status_code=200)
def status():
    return "OK"



@router.post("/items/", status_code=201)
def create_item(item: ItemSchema):
    item_id = str(uuid4())
    now = datetime.utcnow().isoformat()
    doc = {
        "title": item.title,
        "content": item.content,
        "tags": item.tags,
        "language": item.language,
        "created_at": now,
        "updated_at": now,
        "suggest": item.title  # for autocomplete
    }
    try:
        index_item(doc, item_id)
        return {"id": item_id, **doc}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/items/{item_id}")
def read_item(item_id: str):
    try:
        res = get_item(item_id)
        return {"id": res["_id"], **res["_source"]}
    except Exception:
        raise HTTPException(status_code=404, detail="Item not found")




@router.get("/items/",status_code=200)
def read_items():
    try:
        res = get_items()
        return [{"id": hit["_id"], **hit["_source"]} for hit in res['hits']['hits']]
    except Exception:
        raise HTTPException(status_code=404, detail="Item not found")

@router.put("/items/{item_id}")
def update_item_endpoint(item_id: str, item: ItemSchema):
    now = datetime.utcnow().isoformat()
    updated_doc = {
        "title": item.title,
        "content": item.content,
        "tags": item.tags,
        "language": item.language,
        "updated_at": now,
        "suggest": item.title
    }
    try:
        update_item(item_id, updated_doc)
        return {"id": item_id, **updated_doc}
    except Exception:
        raise HTTPException(status_code=404, detail="Failed to update")

@router.delete("/items/{item_id}", status_code=204)
def delete_item_endpoint(item_id: str):
    try:
        delete_item(item_id)
    except Exception:
        raise HTTPException(status_code=404, detail="Item not found")

@router.get("/search/")
def search_endpoint(
    q: Optional[str] = Query(None, description="Full-text query"),
    tags: Optional[str] = Query(None, description="Comma-separated tags"),
    language: Optional[str] = Query(None, description="Language filter"),
    page: int = Query(1, ge=1),
    size: int = Query(10, ge=1, le=100)
):
    tag_list = tags.split(",") if tags else []
    try:
        res = search_items(q, tag_list, language, page, size)
        hits = [
            {
              "id": hit["_id"],
              "_score": hit["_score"],
              **hit["_source"]
            }
            for hit in res["hits"]["hits"]
        ]
        return {
          "total": res["hits"]["total"]["value"],
          "items": hits
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
    
