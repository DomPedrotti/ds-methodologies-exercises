import pandas as pd
from bs4 import BeautifulSoup
from requests import get
from os import path

def acquire_news_articles(from_cache = True):
    '''
    acquire_news_articles(from_cache = True):

    reads article data from https://inshorts.com and documents article titles, bodies, and categories into a json file and returns data in a pandas dataframe

    args: 
    from_cache (bool) - if True, function checks that cached file exists and reads data from cache rather than making server requests. if False, scrapes fresh data from server and writes fresh cache 'news_articles.json'
    '''
    if from_cache == True and path.exists('news_articles.json'):
        return pd.read_json('news_articles.json', orient='records')
    else:
        categories = ['business','sports','technology','entertainment']
        headers = {'User-Agent': 'Codeup Bayes Data Science'}
        news_df = pd.DataFrame(columns=['title','content','category'])
        for i in categories:
            url = f'https://inshorts.com/en/read/{i}'
            response = get(url,headers)
            soup = BeautifulSoup(response.text)

            headlines = soup.find_all('span', itemprop = 'headline')
            headlines = [x.get_text() for x in headlines]

            content = soup.find_all('div', itemprop = 'articleBody')
            content = [x.get_text() for x in content]

            category = pd.DataFrame(headlines, columns=['title'])
            category['content'] = content
            category['category'] = i
            news_df = news_df.append(category, ignore_index=True)
        news_df.to_json('news_articles.json',orient='records')
        return news_df

def get_blog_articles(from_cache = True):
    if from_cache == True and path.exists('blog_posts.json'):
        return pd.read_json('blog_posts.json', orient='records')
    else:
        articles = [
            'https://codeup.com/codeups-data-science-career-accelerator-is-here/',
            'https://codeup.com/data-science-myths/',
            'https://codeup.com/data-science-vs-data-analytics-whats-the-difference/','https://codeup.com/10-tips-to-crush-it-at-the-sa-tech-job-fair/',
            'https://codeup.com/competitor-bootcamps-are-closing-is-the-model-in-danger/']
        headers = {'User-Agent': 'Codeup Data Science Student'}
        data = []
        for article in articles:
            response = get(article,headers = headers)
            soup = BeautifulSoup(response.text)
            title = soup.title.get_text()
            content = soup.select_one('div.mk-single-content.clearfix').get_text()
            data.append({'title': title, 'content': content})   

    pd.DataFrame(data).to_json('blog_posts.json', orient = 'records')
    return pd.DataFrame(data)