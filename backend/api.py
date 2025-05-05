#!/usr/bin/env python3

from fastapi import FastAPI
from db import get_articles as db_get_articles, get_categories as db_get_categories
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/hello")
def hello():
    return {"message": "Hello, World!"}

@app.get("/api/articles")
def get_articles_route(
    search: str = "",
    page: int = 1,
    limit: int = 10,
    subCategory: str = None,
    category: str = None,
    startDate: str = None,
    endDate: str = None 
):
    data = db_get_articles(search, page, limit, subCategory, category, startDate, endDate)
    return JSONResponse(content=data, media_type="application/json")

@app.get("/api/categories")
def get_categories_route():
    data = db_get_categories()
    return JSONResponse(content=data, media_type="application/json")