from newspaper import Article

# URL of the article you want to extract
url = 'https://www.billboard.com/culture/product-recommendations/bose-noise-cancelling-headphones-deal-9590493/'

# Create an Article object and pass the URL
article = Article(url)

# Download and parse the article
article.download()
article.parse()

# Access the main article content
article_content = article.text

# Print the extracted content
print(article_content)
