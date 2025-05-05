#!/usr/bin/env python3

import requests
from bs4 import BeautifulSoup
from db import create_article, create_category, create_image

headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
}

def fetch(url):
    response = requests.get(url, headers=headers)
    response.raise_for_status()
    soup = BeautifulSoup(response.text, 'html.parser')
    return soup

def format_article(article, category):
    link = article.find('a')
    if link:
        href = link.get('href')
        article_data = fetch_article_data(href)
        article_data['category'] = category
        create_article(article_data)
        return article_data

def fetch_article_data(url):
    main_tag = fetch(url)
    main_tag = main_tag.find('main')

    final_data = {
        'title': '',
        'thumbnail': '',
        'resume': '',
        'posted_on': '',
        'author': '',
        'images': [],
    }

    article_title = main_tag.find('h1', class_='entry-title')
    final_data['title'] = article_title.text.strip()

    thumbnail = main_tag.find('figure', class_='article-hat-img')
    if thumbnail:
        temp_thumbnail = thumbnail.find('img') 
        if temp_thumbnail:
            if 'data:image/svg' in str(temp_thumbnail.get('src')) and temp_thumbnail.get('data-lazy-src'):
                final_data['thumbnail'] = temp_thumbnail.get('data-lazy-src')
            else:
                final_data['thumbnail'] = temp_thumbnail.get('src')

    resume = main_tag.find('div', class_='article-hat')
    if resume:
        final_data['resume'] = resume.find('p').text.strip() if resume.find('p') else 'No resume'

    content = main_tag.find('div', class_='entry-content')
    if content:
        final_data['content'] = str(content) if content else 'No content'

    
    posted_on = main_tag.find('span', class_='posted-on')
    if posted_on:
        final_data['posted_on'] = posted_on.find('time').get('datetime')

    author = main_tag.find('span', class_='byline')
    if author:
        final_data['author'] = author.text.strip() if author.text.strip() else 'No author'

    figures = main_tag.find_all('figure')
    for figure in figures:
        if figure.find('img'):
            img_tag = figure.find('img')
            
            src = img_tag.get('src')
            if 'data:image/svg' in str(src) and img_tag.get('data-lazy-src'):
                src = img_tag.get('data-lazy-src')
            elif not src:
                src = 'No image'
                
            image_object = {
                'src': src,
                'caption': figure.find('figcaption').text.strip() if figure.find('figcaption') else 'No caption',
                'alt': img_tag.get('alt', 'No alt text')
            }
            final_data['images'].append(image_object)

    sub_category = main_tag.find('ul', class_='tags-list')
    if sub_category:
        sub_category_items = sub_category.find_all('li')
        final_data['sub_categories'] = []
        for item in sub_category_items:
            link = item.find('a', class_='post-tags')
            if link:
                final_data['sub_categories'].append(link.text.strip())
    return final_data

def fetch_articles(url):
    
    try:
        articles_data = []

        main_tag = fetch(url)
        main_tag = main_tag.find('main')

        if not main_tag:
            print("No <main> tag found.")
            return []

        articles = main_tag.find_all('article')
        category = url.split('/')[-2]
        print("Fetching page ", url)
        for article in articles:
            article_data = format_article(article, category)
            articles_data.append(article_data)
        
        print("=====FETCHED PAGE=====")
        pages = main_tag.find('div', class_='wp-pagenavi')
        if pages:
            page_links = pages.find_all('a', class_='page')
            for page_link in page_links:
                print("Fetching page", page_link['href'])
                page_url = page_link['href']
                try:
                    page_response = fetch(page_url)
                    articles = page_response.find_all('article')
                    for article in articles:
                        article_data = format_article(article, category)
                        articles_data.append(article_data)

                except requests.exceptions.RequestException as e:
                    print(f"Erreur lors de l'accès à la page {page_url}: {e}")
                    continue
                print("=====FETCHED PAGE=====")

        return articles_data

    except requests.exceptions.RequestException as e:
        print(f"Error: {e}")
        return []

categories = [
    "web",
    "marketing", 
    "social",
    "tech"
]

for category in categories:
    print("Fetching category", category)
    url = f"https://www.blogdumoderateur.com/{category}/"
    articles = fetch_articles(url)
    print("Articles fetched", len(articles))