from newspaper import Article

# URL of the article you want to extract
url = 'https://www.reuters.com/world/us/trump-says-federal-prosecutor-said-he-was-target-jan-6-attack-probe-2023-07-18/'

# Create an Article object and pass the URL
article = Article(url)

# Download and parse the article
article.download()
article.parse()

# Access the main article content
article_content = article.text

# Print the extracted content
print(article_content)
