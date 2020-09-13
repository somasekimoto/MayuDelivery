import os
import tweepy

consumer_key = os.getenv('TWITTER_CONSUMER_KEY')
consumer_secret = os.getenv('TWITTER_CONSUMER_SECRET')
access_token = os.getenv('TWITTER_ACCESS_TOKEN')
access_token_secret = os.getenv('TWITTER_ACCESS_TOKEN_SECRET')
bearer_token = os.getenv('TWITTER_ACCESS_TOKEN_SECRET')


# twitter で#松岡茉優の画像検索してURL取得
def search_photos():
    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)
    api = tweepy.API(auth)

    cric_tweet = tweepy.Cursor(
        api.search, q='#松岡茉優 filter:images min_faves:7', lang='ja', result_type='mixed').items(15)
    print(cric_tweet)

    photo_urls = []
    for tweet in cric_tweet:
        try:
            print(tweet.text)
            print(tweet.entities)
            print(tweet.entities['media'][0]['media_url_https'])
            photo_urls.append(tweet.entities['media'][0]['media_url_https'])
            print('--------------------------------------------')
        except:
            print('noPhotoUrl')
            print('--------------------------------------------')
    return photo_urls


if __name__ == "__main__":
    search_photos()
