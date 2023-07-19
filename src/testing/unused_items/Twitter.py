import tweepy

# Twitter API credentials (replace with your own)
consumer_key = 'YOUR_CONSUMER_KEY'
consumer_secret = 'YOUR_CONSUMER_SECRET'
access_token = 'YOUR_ACCESS_TOKEN'
access_token_secret = 'YOUR_ACCESS_TOKEN_SECRET'

# Authenticate to Twitter API
auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)
api = tweepy.API(auth)

# Fetch worldwide top trends
trends_result = api.trends_place(id=1)

# Print the top trends
print("Top trends on Twitter (Worldwide):")
for trend in trends_result[0]["trends"]:
    print(trend["name"])
