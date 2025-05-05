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

def get_articles():
    mycol = mydb["articles"]
    return mycol.find()

def create_article(article):
    print(article)
    mycol = mydb["articles"]
    
    existing_article = mycol.find_one({"title": article["title"]})
    if existing_article:
        return existing_article["_id"]
    
    category_id = None
    if "category" in article:
        category_name = article["category"]
        category_id = create_category({"name": category_name})
    
    sub_category_ids = []
    if "sub_category" in article:
        # Si c'est une seule sous-catégorie sous forme de chaîne
        if isinstance(article["sub_category"], str):
            sub_cat_name = article["sub_category"]
            sub_cat_id = create_sub_category({"name": sub_cat_name})
            sub_category_ids.append(sub_cat_id)
        # Si c'est une liste de sous-catégories
        elif isinstance(article["sub_category"], list):
            for sub_cat_name in article["sub_category"]:
                sub_cat_id = create_sub_category({"name": sub_cat_name})
                sub_category_ids.append(sub_cat_id)
        
    image_ids = []
    if "images" in article and article["images"]:
        for image in article["images"]:
            image_id = create_image(image)
            image_ids.append(image_id)
    
    article_to_insert = article.copy()
    if category_id:
        article_to_insert["category_id"] = category_id
        del article_to_insert["category"]
    
    if sub_category_ids:
        article_to_insert["sub_category_ids"] = sub_category_ids
        if "sub_category" in article_to_insert:
            del article_to_insert["sub_category"]
    
    if image_ids:
        article_to_insert["image_ids"] = image_ids
        del article_to_insert["images"]
    
    # Insérer l'article
    result = mycol.insert_one(article_to_insert)
    return result.inserted_id

def create_category(category):
    mycol = mydb["categories"]
    
    existing_category = mycol.find_one({"name": category["name"]})
    if existing_category:
        return existing_category["_id"]
    
    result = mycol.insert_one(category)
    return result.inserted_id

def create_sub_category(sub_category):
    mycol = mydb["sub_categories"]
    
    existing_sub_category = mycol.find_one({"name": sub_category["name"]})
    if existing_sub_category:
        return existing_sub_category["_id"]
    
    result = mycol.insert_one(sub_category)
    return result.inserted_id

def create_image(image):
    mycol = mydb["images"]
    
    existing_image = mycol.find_one({"src": image["src"]})
    if existing_image:
        return existing_image["_id"]
    
    result = mycol.insert_one(image)
    return result.inserted_id
