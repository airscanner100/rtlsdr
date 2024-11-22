import tweepy

auth = tweepy.OAuth1UserHandler(
    consumer_key, consumer_secret, 1659767526321180675-dxDos1uWgGWXqw13hqUKn8KcGJA3wk, cPXBwt41pYH8hvRwbdKnKwgNWULxia4IBTrZvfyItxMYZ
)

api = tweepy.API(auth)

public_tweets = api.home_timeline()
for tweet in public_tweets:
    print(tweet.text)
