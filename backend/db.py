#!/usr/bin/env python3

import pymongo
import os
from dotenv import load_dotenv
from bson.objectid import ObjectId

load_dotenv()

mongo_user = os.getenv("MONGODB_USERNAME", "root")
mongo_password = os.getenv("MONGODB_PASSWORD", "password")
mongo_host = os.getenv("MONGODB_URL", "localhost:27017")
mongo_db = os.getenv("MONGODB_DATABASE", "blogdumoderateur")

connection_string = f"mongodb://{mongo_user}:{mongo_password}@{mongo_host}/"
myclient = pymongo.MongoClient(connection_string)
mydb = myclient[mongo_db]
collist = mydb.list_collection_names()

def create_article(article):
    mycol = mydb["articles"]
    
    existing_article = mycol.find_one({"title": article["title"]})
    if existing_article:
        return existing_article["_id"]
    
    category_id = None
    if "category" in article:
        category_name = article["category"]
        category_id = create_category({"name": category_name})
    
    sub_category_ids = []
    if "sub_categories" in article:
        sub_category_names = article["sub_categories"]
        if isinstance(sub_category_names, list):
            for sub_cat in sub_category_names:
                sub_cat_id = create_sub_category({"name": sub_cat})
                if sub_cat_id:
                    sub_category_ids.append(sub_cat_id)
                    if category_id:
                        link_category_sub_category(category_id, sub_cat_id)
        else:
            sub_cat_id = create_sub_category({"name": sub_category_names})
            if sub_cat_id:
                sub_category_ids.append(sub_cat_id)
                if category_id:
                    link_category_sub_category(category_id, sub_cat_id)
    
    image_ids = []
    if "images" in article and article["images"]:
        for image in article["images"]:
            if "src" in image and image["src"] != article.get("thumbnail", ""):
                image_id = create_image(image)
                if image_id:
                    image_ids.append(image_id)
    
    article_to_insert = {
        "title": article["title"],
        "resume": article.get("resume", ""),
        "thumbnail": article.get("thumbnail", ""),
        "content": article.get("content", ""),
        "posted_on": article.get("posted_on", ""),
        "author": article.get("author", ""),
        "category_id": category_id,
        "sub_category_ids": sub_category_ids,
        "image_ids": image_ids
    }
    
    result = mycol.insert_one(article_to_insert)
    return result.inserted_id

def create_category(category):
    mycol = mydb["categories"]
    
    existing_category = mycol.find_one({"name": category["name"]})
    if existing_category:
        return existing_category["_id"]
    
    category_to_insert = {
        "name": category["name"],
        "sub_category_ids": []
    }
    
    result = mycol.insert_one(category_to_insert)
    return result.inserted_id

def create_sub_category(sub_category):
    mycol = mydb["sub_categories"]
    
    existing_sub_category = mycol.find_one({"name": sub_category["name"]})
    if existing_sub_category:
        return existing_sub_category["_id"]
    
    sub_category_to_insert = {
        "name": sub_category["name"],
        "category_ids": []
    }
    
    result = mycol.insert_one(sub_category_to_insert)
    return result.inserted_id

def link_category_sub_category(category_id, sub_category_id):
    """Crée une relation many-to-many entre catégorie et sous-catégorie"""
    cat_col = mydb["categories"]
    sub_cat_col = mydb["sub_categories"]
    
    cat_col.update_one(
        {"_id": ObjectId(category_id)}, 
        {"$addToSet": {"sub_category_ids": ObjectId(sub_category_id)}}
    )
    
    sub_cat_col.update_one(
        {"_id": ObjectId(sub_category_id)}, 
        {"$addToSet": {"category_ids": ObjectId(category_id)}}
    )

def create_image(image):
    mycol = mydb["images"]
    
    existing_image = mycol.find_one({"src": image["src"]})
    if existing_image:
        return existing_image["_id"]
    
    result = mycol.insert_one(image)
    return result.inserted_id

def get_articles(
    search,
    page,
    limit,
    subCategory=None,
    category=None,
    startDate=None,
    endDate=None
):
    mycol = mydb["articles"]
    query = {}
    
    if search:
        query["title"] = {
            "$regex": search,
            "$options": "i"
        }
    
    if subCategory:
        sub_cat_col = mydb["sub_categories"]
        sub_cat_obj = sub_cat_col.find_one({"name": subCategory})
        if sub_cat_obj:
            query["sub_category_ids"] = {"$in": [sub_cat_obj["_id"]]}
    if category:
        cat_col = mydb["categories"]
        cat_obj = cat_col.find_one({"name": category})
        if cat_obj:
            query["category_id"] = cat_obj["_id"]
    if startDate:
        query["posted_on"] = {"$gte": startDate}
    if endDate:
        query["posted_on"] = {"$lte": endDate}
    skip = (page - 1) * limit   
    
    articles = list(mycol.find(query).skip(skip).limit(limit))
    
    cat_col = mydb["categories"]
    sub_cat_col = mydb["sub_categories"]
    images_col = mydb["images"]
    
    for article in articles:
        if "_id" in article:
            article["_id"] = str(article["_id"])
            
        if "category_id" in article and article["category_id"]:
            category_id = article["category_id"]
            article["category_id"] = str(category_id)
            category = cat_col.find_one({"_id": ObjectId(category_id)})
            if category:
                article["category_name"] = category["name"]
                
        if "sub_category_ids" in article and article["sub_category_ids"]:
            sub_cats = []
            for sub_cat_id in article["sub_category_ids"]:
                article["sub_category_ids"] = [str(id) for id in article["sub_category_ids"]]
                sub_cat = sub_cat_col.find_one({"_id": ObjectId(sub_cat_id)})
                if sub_cat:
                    sub_cats.append({"id": str(sub_cat["_id"]), "name": sub_cat["name"]})
            article["sub_categories"] = sub_cats
        
        if "image_ids" in article and article["image_ids"]:
            article["image_ids"] = [str(id) for id in article["image_ids"]]
            images = []
            for img_id in article["image_ids"]:
                img = images_col.find_one({"_id": ObjectId(img_id)})
                if img:
                    img["_id"] = str(img["_id"])
                    images.append(img)
            article["images"] = images
    
    total_articles = mycol.count_documents(query)
    max_page = (total_articles // limit) + (1 if total_articles % limit > 0 else 0)
    
    return {
        "articles": articles,
        "max_page": max_page,
        "current_page": page,
        "limit": limit,
        "total": total_articles
    }

def get_categories():
    mycol = mydb["categories"]
    categories = list(mycol.find())
    
    sub_cat_col = mydb["sub_categories"]
    
    for category in categories:
        if "_id" in category:
            category["_id"] = str(category["_id"])
            
        sub_categories = []
        if "sub_category_ids" in category:
            category["sub_category_ids"] = [str(id) for id in category["sub_category_ids"]]
            for sub_cat_id in category["sub_category_ids"]:
                sub_cat = sub_cat_col.find_one({"_id": ObjectId(sub_cat_id)})
                if sub_cat:
                    sub_categories.append({
                        "id": str(sub_cat["_id"]),
                        "name": sub_cat["name"]
                    })
        
        category["sub_categories"] = sub_categories
        del category["sub_category_ids"]
    
    return {"categories": categories}