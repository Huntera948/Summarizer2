import requests

url = "https://bing-news-search1.p.rapidapi.com/news/trendingtopics"

querystring = {"textFormat": "Raw", "safeSearch": "Off"}

headers = {
    "X-BingApis-SDK": "true",
    "X-RapidAPI-Key": "2ae68ace42msh9fb07e15283ad8ep158364jsn6f0d7bebe76d",
    "X-RapidAPI-Host": "bing-news-search1.p.rapidapi.com"
}

response = requests.get(url, headers=headers, params=querystring)
data = response.json()

# Extract query texts
query_texts = [topic['query']['text'] for topic in data['value']]

# Print the array of query texts
print(query_texts)
