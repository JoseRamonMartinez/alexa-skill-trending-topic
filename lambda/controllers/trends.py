import tweepy
import requests
import base64
import json
from dotenv import load_dotenv
import os

country_woeid = {
    'Spain':23424950,
    'españa':23424950,
    'espagne':23424950,
    'Argentina':332471,
    'argentina':332471,
    'argentine':332471,
    'Canada':4118,
    'canadá':4118,
    'UK':44418,
    'United Kingdom':44418,
    'royaume-Uni':44418,
    'reino':44418,
    'England':44418,
    'inglaterra':44418,
    'angleterre':44418,
    'Dominican Republic':76456,
    'república dominicana':76456,
    'république dominicaine':76456,
    'Guatemala':83123,
    'guatemala':83123,
    'Mexico':116545,
    'méxico':116545,
    'méjico':116545,
    'mexique':116545,
    'Chile':349859,
    'chile':349859,
    'Colombia':368148,
    'colombia':368148,
    'colombie':368148,
    'Ecuador':375732,
    'ecuador':375732,
    'équateur':375732,
    'Venezuela':395269,
    'venezuela':395269,
    'Peru':418440,
    'perú':418440,
    'pérou':418440,
    'Brazil':455825,
    'brasil':455825,
    'brésil':455825,
    'Poland':502075,
    'polonia':502075,
    'pologne':502075,
    'Austria':551801,
    'austria':551801,
    'Autriche':551801,
    'Ireland':560472,
    'irlanda':560472,
    'irlande':560472,
    'France':615702,
    'francia':615702,
    'france':615702,
    'Deutschland':638242,
    'Germany':638242,
    'alemania':638242,
    'allemagne':638242,
    'Italy':721943,
    'italia':721943,
    'italie':721943,
    'Netherlands':727232,
    'países bajos':727232,
    'holanda':727232,
    'holland':727232,
    'pays Bas':727232,
    'Switzerland':784794,
    'suiza':784794,
    'suisse':784794,
    'Belarus':834463,
    'bielorrusia':834463,
    'biélorussie':834463,
    'Latvia':854823,
    'letonia':854823,
    'lettonie':854823,
    'Norway':857105,
    'noruega':857105,
    'norvège':857105,
    'Sweden':906057,
    'suecia':906057,
    'suède':906057,
    'Ukraine':924938,
    'ucrania':924938,
    'ukraine':924938,
    'Greece':946738,
    'grecia':946738,
    'grèce':946738,
    'Indonesia':1032539,
    'indonesia':1032539,
    'indonésie':1032539,
    'Singapore':1062617,
    'singapur':1062617,
    'singapour':1062617,
    'Australia':1105779,
    'australia':1105779,
    'australie':1105779,
    'Japan':1118370,
    'japón':1118370,
    'japon':1118370,
    'USA':2442047,
    'United States':2442047,
    'estados unidos':2442047,
    'états-unis':2442047,
    'Portugal':23424925,
    'portugal':23424925,
    'Andorra':23424950,
    'andorra':23424950,
    'andorre':23424950,
    'India':23424848,
    'india':23424848,
    'inde':23424848,
    'Israel':23424852,
    'israel':23424852,
    'israël':23424852,
    'Korea':23424868,
    'corea':23424868,
    'corée':23424868,
    'Malaysia':23424901,
    'malasia':23424901,
    'malaisie':23424901,
    'New Zealand':23424916,
    'nueva zelanda':23424916,
    'nouvelle zélande':23424916,
    'Qatar':23424930,
    'qatar':23424930,
    'Philippines':23424934,
    'filipinas':23424934,
    'philippines':23424934,
    'Puerto Rico':23424935,
    'puerto rico':23424935,
    'porto rico':23424935,
    'Russia':23424936,
    'rusia':23424936,
    'russie':23424936,
    'South Africa':23424942,
    'sudáfrica':23424942,
    'afrique du sud':23424942,
    'Turkey':23424969,
    'turquía':23424969,
    'turquie':23424969,
    'Vietnam':23424984,
    'vietnam':23424984,
    'viêt nam':23424984,
}

def trends(country):
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
    trend_headers = {
        'Authorization': 'Bearer {}'.format(access_token)    
    }

    trend_params = {
        'id': country_woeid[country],
    }

    trend_url = 'https://api.twitter.com/1.1/trends/place.json'  
    trend_resp = requests.get(trend_url, headers=trend_headers, params=trend_params)

    tweet_data = trend_resp.json()
    output=[]
    for i in range(0,10):
        output.append(tweet_data[0]['trends'][i]['name'])

    return output
