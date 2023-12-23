

import tweepy

consumer_key = '1659767526321180675-dxDos1uWgGWXqw13hqUKn8KcGJA3wk' #API Key
consumer_secret = 'cPXBwt41pYH8hvRwbdKnKwgNWULxia4IBTrZvfyItxMYZ' #API Key Secret
access_token = ''
access_token_secret = ''


client = tweepy.Client(
    consumer_key=consumer_key, consumer_secret=consumer_secret,
    access_token=access_token, access_token_secret=access_token_secret
)


text = 'Hello, World!'
client.create_tweet(text=text)

