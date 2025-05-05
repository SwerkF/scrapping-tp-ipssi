#!/usr/bin/env python3

import requests
from bs4 import BeautifulSoup
from api import create_article, create_category, create_image

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
        article_data['sub_category'] = article.find('span', class_='favtag color-b').text.strip()
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

    article_title = main_tag.find('h1')
    final_data['title'] = article_title.text.strip()

    thumbnail = main_tag.find('figure', class_='article-hat-img')
    if thumbnail:
        final_data['thumbnail'] = thumbnail.find('img').get('src') if thumbnail.find('img') else 'No thumbnail'

    resume = main_tag.find('div', class_='article-hat t-quote pb-md-8 pb-5')
    if resume:
        final_data['resume'] = resume.find('p').text.strip() if resume.find('p') else 'No resume'

    posted_on = main_tag.find('span', class_='posted-on')
    if posted_on:
        final_data['posted_on'] = posted_on.text.strip() + " " + posted_on.find('time')['datetime'] if posted_on.find('time') else 'No posted on'

    author = main_tag.find('span', class_='byline')
    if author:
        final_data['author'] = author.text.strip() if author.text.strip() else 'No author'

    figures = main_tag.find_all('figure')
    for figure in figures:
        if figure.find('img'):
            img_tag = figure.find('img')
            print(img_tag)
            
            # Gestion des images avec data-lazy-src (images chargées en lazy loading)
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
    
    standalone_images = main_tag.find_all('img', recursive=True)
    for img in standalone_images:
        if img.parent.name != 'figure':  
            src = img.get('src')
            if 'data:image/svg' in str(src) and img.get('data-lazy-src'):
                src = img.get('data-lazy-src')
            elif not src:
                src = 'No image'
                
            image_object = {
                'src': src,
                'caption': 'No caption',
                'alt': img.get('alt', 'No alt text')
            }
            final_data['images'].append(image_object)

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