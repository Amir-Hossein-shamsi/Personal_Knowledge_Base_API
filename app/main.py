from fastapi import FastAPI, HTTPException, Query
from pydantic import BaseModel
from typing import List, Optional
from uuid import uuid4
from datetime import datetime

from routes import router
from utils import es

print("Elasticsearch connected:", es.ping())



app = FastAPI(title="Personal Knowledge Base API")

app.include_router(router)