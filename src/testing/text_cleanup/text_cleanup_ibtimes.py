import re

def clean_text_ibtimes(text):
    # Remove unwanted text at the beginning
    text = re.sub(r'^[\s\S]*?NEWSLETTER SIGNUP.*?KEY POINTS', '', text)
    text = re.sub(r'REGISTER FOR FREE[\s\S]*?All Rights Reserved\.', '', text)
    text = re.sub(r'pic\.twitter\.com\/\w+', '', text)  # Remove chunks like "pic.twitter.com/kwkFzy0Us0"
    # Remove unwanted text at the end
    text = re.sub(r'ABOUT About Us.*$', '', text)
    # Remove extra whitespaces
    text = re.sub(r'\s+', ' ', text).strip()
    return text
