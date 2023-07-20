import json
import aiohttp
import asyncio
import copy

from insertArticles2db import insert_articles
from text_cleanup.text_cleanup_ibtimes import clean_text_ibtimes
from NER import perform_ner_extraction

apiKey = "pub_2529453bb1703552da9694fe294be8dd033c3"
domains = [
    ["bbc", "billboard", "cnet", "cbsnews", "futurism"],
    ["gizmodo", "forbes", "ibtimes", "nasa", "npr"],
    ["nytimes", "pcgamer", "propublica", "reutersagency", "techcrunch"],
    ["theverge", "time", "thurrott", "universetoday", "wired"],
    ["wsj", "yahoo"],
]
domains_copy = copy.deepcopy(domains)

ranks = {
    "bbc": 9,
    "billboard": 6,
    "cnet": 8,
    "cbsnews": 6,
    "futurism": 7,
    "gizmodo": 7,
    "forbes": 8,
    "ibtimes": 6,
    "nasa": 7,
    "npr": 9,
    "nytimes": 10,
    "pcgamer": 8,
    "propublica": 10,
    "reutersagency": 9,
    "techcrunch": 9,
    "theverge": 7,
    "time": 9,
    "thurrott": 6,
    "universetoday": 7,
    "wired": 8,
    "wsj": 10,
    "yahoo": 4,
}

async def fetch_news_data(session, url):
    async with session.get(url) as resp:
        data = await resp.text()
        return json.loads(data)

async def process_articles(data, article_array):
    articles = data.get('results', [])

    if not isinstance(articles, list):
        print(f"Unexpected response: {articles}")
        return

    for article in articles:
        if (
            article['content'] is not None
            and len(article['content']) >= 1000
            and article['language'] == "english"
        ):
            if article['source_id'] == "ibtimes":
                article['content'] = clean_text_ibtimes(article['content'])

            rank = ranks.get(article['source_id'].lower(), 0)
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
                'rank': rank
            }

            article_array.append(article_object)

async def fetch_and_process(session, domain):
    url = f"https://newsdata.io/api/1/news?apikey={apiKey}&domain={','.join(domain)}"
    article_array = []
    while url:
        data = await fetch_news_data(session, url)
        await process_articles(data, article_array)
        next_page = data.get('nextPage')
        url = f"https://newsdata.io/api/1/news?apikey={apiKey}&domain={','.join(domain)}&page={next_page}" if next_page else None
    return article_array

async def get_news_data():
    async with aiohttp.ClientSession() as session:
        all_articles = []
        while domains_copy:
            domain = domains_copy.pop(0)
            articles = await fetch_and_process(session, domain)
            all_articles.extend(articles)
        if all_articles:
            insert_articles(all_articles)  # Call insert_articles directly without run_in_executor
            extracted_entities = await perform_ner_extraction(all_articles)  # Perform NER extraction on inserted articles
            print(extracted_entities)  # Print or process the extracted entities as desired
        else:
            print("No articles to insert")
        return all_articles

loop = asyncio.get_event_loop()
results = loop.run_until_complete(get_news_data())
print(results)
