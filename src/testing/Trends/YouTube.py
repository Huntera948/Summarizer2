from googleapiclient.discovery import build

# Set up the YouTube Data API v3 service
api_key = 'AIzaSyAZ1hJY41i1nmpAhAOAlc4gYN-u0kh4amI'
youtube = build('youtube', 'v3', developerKey=api_key)

# Fetch the top trending videos
request = youtube.videos().list(
    part='snippet',
    chart='mostPopular',
    regionCode='US',  # Replace with your desired region code
    maxResults=10  # Number of top trending videos to fetch
)
response = request.execute()

# Print the titles of the top trending videos
print('Top trending videos on YouTube:')
for item in response['items']:
    print(item['snippet']['title'])
