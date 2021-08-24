import tweepy
import requests
import base64
import re
from dotenv import load_dotenv
import os

emoji_pattern = re.compile("["
    u"\U0001F600-\U0001F64F"  # emoticons
    u"\U0001F300-\U0001F5FF"  # symbols & pictographs
    u"\U0001F680-\U0001F6FF"  # transport & map symbols
    u"\U0001F1E0-\U0001F1FF"  # flags (iOS)
    u"\U0001F1F2-\U0001F1F4"  # Macau flag
    u"\U0001F1E6-\U0001F1FF"  # flags
    u"\U0001F600-\U0001F64F"
    u"\U00002702-\U000027B0"
    u"\U000024C2-\U0001F251"
    u"\U0001f926-\U0001f937"
    u"\U0001F1F2"
    u"\U0001F1F4"
    u"\U0001F620"
    u"\u200d"
    u"\u2640-\u2642"
    "]+", flags=re.UNICODE)

def popular_topic_tweets(topic, language):
    #Load env variables for keys
    load_dotenv()
    consumer_key = os.environ['CONSUMER_KEY']
    consumer_secret = os.environ['CONSUMER_SECRET']
    #Reformat the keys and encode them
    key_secret = '{}:{}'.format(consumer_key, consumer_secret).encode('ascii')
    #Transform from bytes to bytes that can be printed
    b64_encoded_key = base64.b64encode(key_secret)
    #Transform from bytes back into Unicode
    b64_encoded_key = b64_encoded_key.decode('ascii')
    
    base_url = 'https://api.twitter.com/'
    auth_url = '{}oauth2/token'.format(base_url)
    auth_headers = {
        'Authorization': 'Basic {}'.format(b64_encoded_key),
        'Content-Type': 'application/x-www-form-urlencoded;charset=UTF-8'
    }
    auth_data = {
        'grant_type': 'client_credentials'
    }
    auth_resp = requests.post(auth_url, headers=auth_headers, data=auth_data)
    #print(auth_resp.status_code)
    access_token = auth_resp.json()['access_token']
    
    topic_headers = {
    'Authorization': 'Bearer {}'.format(access_token)    
    }
    topic_params = {
        'q': f'{topic}',
        'result_type': 'mixed',
        'lang':f'{language}',
        'include_entities':'false',
        'tweet_mode':'extended'
    }
    topic_url = 'https://api.twitter.com/1.1/search/tweets.json'  
    topic_resp = requests.get(topic_url, headers=topic_headers, params=topic_params)
    tweet_data = topic_resp.json()
    topic_tweets={}
    for i in range(0,10):
        
        topic_tweets[(tweet_data['statuses'][i]['user']['name'])] = clean_text(tweet_data['statuses'][i]['full_text'])
    
    return topic_tweets

def clean_text(tweet_text):
    cleaned = re.sub(r"http\S+", "", tweet_text)
    cleaned = emoji_pattern.sub(r'', cleaned)
    return cleaned
    