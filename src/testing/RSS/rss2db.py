import feedparser
import requests
from pymongo import MongoClient
from bs4 import BeautifulSoup
from RSS_Feed_URLs import feed_urls
import concurrent.futures
import re
import html

# Set up a connection to MongoDB
client = MongoClient('mongodb://127.0.0.1:27017/')
db = client['newsdata']
collection = db['RSSdata']

entities = []  # Define your entities here

# Define a function to fetch and parse a single RSS feed
def parse_single_rss(url):
    try:
        response = requests.get(url, timeout=60)
        feed = feedparser.parse(response.content)
        
        if not feed.entries:
            print(f"Invalid RSS feed or no entries found for URL: {url}")
            return
        
        print(f"Parsing RSS feed from {url}...")
        
        entries = feed.entries
        article_count = 0  # Counter for number of articles added
        
        for entry in entries:
            content = entry.get('content', '')
            description = entry.get('description', '')
            summary = entry.get('summary', '')
            pub_date = entry.get('published', '')
            author = entry.get('author', '')
            category = entry.get('category', '')
            comments = entry.get('comments', '')
            
            # Check if the tag starts with <![CDATA[
            if is_cdata(description):
                print(f"Skipping <![CDATA[ tag for URL: {url}")
                continue

            # Extract relevant text from the summary field
            summary_text = extract_text_from_html(summary)

            # Skip articles with empty or insufficient information
            if not description or not summary_text:
                print(f"Skipping article with insufficient information for URL: {url}")
                continue

            # Preserve the original HTML content in description, summary, and content fields
            data = {
                'url': url,
                'content': content,
                'description': description,
                'summary': summary,
                'entities': entities,
                'pubDate': pub_date,
                'author': author,
                'category': category,
                'comments': comments
            }

            # Update the specific fields with extracted text
            data['summary'] = summary_text

            collection.insert_one(data)
            
            article_count += 1  # Increment article count
        
        print(f"Articles added for URL {url}: {article_count}")
        return article_count
        
    except requests.Timeout:
        print(f"Timeout occurred while accessing RSS feed: {url}")
        return 0
    except Exception as e:
        print(f"Error parsing RSS feed from {url}: {e}")
        return 0

# Function to check if a tag starts with <![CDATA[
def is_cdata(tag):
    return tag.startswith('<![CDATA[')

# Function to extract relevant text from HTML content
def extract_text_from_html(html_content):
    soup = BeautifulSoup(html_content, 'html.parser')
    # Remove unwanted elements such as images, links, figures, and figcaptions
    for element in soup(['img', 'a', 'figure', 'figcaption']):
        element.extract()
    # Convert the preserved HTML to unescaped text
    unescaped_text = html.unescape(str(soup))
    # Clean the extracted text
    cleaned_text = re.sub(r'\s+', ' ', unescaped_text.strip())
    cleaned_text = re.sub(r"<p[^>]*>(.*?)<\/p>", '', cleaned_text.strip())
    cleaned_text = re.sub(r"<span[^>]*>(.*?)<\/span>", '', cleaned_text.strip())
    return cleaned_text

# Use multithreading to fetch and parse the RSS feeds concurrently
with concurrent.futures.ThreadPoolExecutor() as executor:
    futures = [executor.submit(parse_single_rss, url) for url in feed_urls]
    article_counts = concurrent.futures.wait(futures, timeout=60)

total_articles = sum(filter(None, (article.result() for article in article_counts[0])))
print(f"Total articles added to the database: {total_articles}")

print("All RSS feeds parsed successfully.")
