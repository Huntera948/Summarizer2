import json
import aiohttp
import asyncio

# Assuming insert_articles and clean_text_ibtimes are defined elsewhere
from insertArticles2db import insert_articles
from text_cleanup_ibtimes import clean_text_ibtimes

apiKey = "pub_2529453bb1703552da9694fe294be8dd033c3"
domains = [
    ["bbc", "billboard", "cnet", "cbsnews", "futurism"],
    ["gizmodo", "forbes", "ibtimes", "nasa", "npr"],
    ["nytimes", "pcgamer", "propublica", "reutersagency", "techcrunch"],
    ["theverge", "time", "thurrott", "universetoday", "wired"],
    ["wsj", "yahoo"],
]

async def fetch_news_data(session, url):
    async with session.get(url) as resp:
        data = await resp.text()
    return data

async def get_news_data():
    article_array = []
    
    async with aiohttp.ClientSession() as session:
        while len(domains) > 0:
            initial_url = f"https://newsdata.io/api/1/news?apikey={apiKey}&domain={','.join(domains[0])}"
            
            while True:
                data = await fetch_news_data(session, initial_url)
                data = json.loads(data)

                articles = data.get('results', [])

                if not isinstance(articles, list):
                    print(f"Unexpected response: {articles}")
                    break
                
                articles = data['results']
                for article in articles:
                    if (article['content'] is not None 
                        and len(article['content']) >= 1000
                        and article['language'] == "english"):
                        
                        if article['source_id'] == "ibtimes":
                            article['content'] = clean_text_ibtimes(article['content'])

                        article_object = {
                            'pubDate': article['pubDate'],
                            'title': article['title'],
                            'link': article['link'],
                            'content': article['content'],
                            'creator': article['creator'],
                            'keywords': article['keywords'],
                            'country': article['country'],
                            'category': article['category'],
                            'source_id': article['source_id'],
                            'language': article['language'],
                            'description': article['description'],
                        }

                        article_array.append(article_object)

                if 'nextPage' in data:
                    initial_url = f"https://newsdata.io/api/1/news?apikey={apiKey}&domain={','.join(domains[0])}&page={data['nextPage']}"
                else:
                    break
                
            domains.pop(0)
        
        if len(article_array) == 0:
            print("No articles to insert")
        else:
            await insert_articles(article_array)
        
        return article_array

loop = asyncio.get_event_loop()
results = loop.run_until_complete(get_news_data())
print(results)
