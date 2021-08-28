import re
import nltk
import emoji

class Data_clean:
    words = nltk.download('words')

    def __init__(self):
        pass


    def cleaner(self,tweet):
        tweet = tweet.lower()
        tweet = re.sub(r'\brt\b', '', tweet)
        tweet = re.sub('[^A-Za-z0-9 ]+','', tweet)
        tweet = re.sub("@[A-Za-z0-9]+", "", tweet)  # Remove @ sign
        tweet = re.sub(r"(?:\@|http?\://|https?\://|www)\S+", "", tweet)  # Remove http links
        tweet = " ".join(tweet.split())
        tweet = ''.join(c for c in tweet if c not in emoji.UNICODE_EMOJI)  # Remove Emojis
        tweet = tweet.replace("#", "").replace("_", " ")  # Remove hashtag sign but keep the text
        tweet = " ".join(w for w in nltk.wordpunct_tokenize(tweet))
        return tweet

    def cleaner_all(self,tweets):
        outs = []
        for tweet in tweets:
            tweet = tweet.lower()
            tweet = re.sub(r'\brt\b', '', tweet)
            tweet = re.sub('[^A-Za-z ]+', '', tweet)
            tweet = re.sub("@[A-Za-z0-9]+", "", tweet)  # Remove @ sign
            tweet = re.sub(r"(?:\@|http?\://|https?\://|www)\S+", "", tweet)  # Remove http links
            tweet = " ".join(tweet.split())
            tweet = ''.join(c for c in tweet if c not in emoji.UNICODE_EMOJI)  # Remove Emojis
            tweet = tweet.replace("#", "").replace("_", " ").replace("rt", " ")  # Remove hashtag sign but keep the text
            tweet = " ".join(w for w in nltk.wordpunct_tokenize(tweet))
            outs.append(tweet)
        return outs