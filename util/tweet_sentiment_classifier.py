import re, string, random

from nltk.stem.wordnet import WordNetLemmatizer
from nltk.corpus import twitter_samples, stopwords
from nltk.tag import pos_tag
from nltk.tokenize import word_tokenize
from nltk import FreqDist, classify, NaiveBayesClassifier

"""
Required NLTK Downloads
import nltk
nltk.download('wordnet')
nltk.download('averaged_perceptron_tagger')
nltk.download('stopwords')
nltk.download('twitter_samples')
nltk.download('punkt')
"""

def remove_noise(tweet_tokens, stop_words = ()):

    cleaned_tokens = []

    for token, tag in pos_tag(tweet_tokens):
        token = re.sub('http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+#]|[!*\(\),]|'\
                       '(?:%[0-9a-fA-F][0-9a-fA-F]))+','', token)
        token = re.sub("(@[A-Za-z0-9_]+)","", token)
        if tag.startswith("NN"):
            pos = 'n'
        elif tag.startswith('VB'):
            pos = 'v'
        else:
            pos = 'a'

        lemmatizer = WordNetLemmatizer()
        token = lemmatizer.lemmatize(token, pos)

        if len(token) > 0 and token not in string.punctuation and token.lower() not in stop_words:
            cleaned_tokens.append(token.lower())
    return cleaned_tokens


def get_all_words(cleaned_tokens_list):
    for tokens in cleaned_tokens_list:
        for token in tokens:
            yield token


def get_tweets_for_model(cleaned_tokens_list):
    for tweet_tokens in cleaned_tokens_list:
        yield dict([token, True] for token in tweet_tokens)



class TweetSentimentClassifier:
    def __init__(self):
        stop_words = stopwords.words('english')
        positive_tweet_tokens = twitter_samples.tokenized('positive_tweets.json')
        negative_tweet_tokens = twitter_samples.tokenized('negative_tweets.json')

        positive_cleaned_tokens_list = []
        negative_cleaned_tokens_list = []

        for tokens in positive_tweet_tokens:
            positive_cleaned_tokens_list.append(remove_noise(tokens, stop_words))

        for tokens in negative_tweet_tokens:
            negative_cleaned_tokens_list.append(remove_noise(tokens, stop_words))

        positive_tokens_for_model = get_tweets_for_model(
            positive_cleaned_tokens_list)
        negative_tokens_for_model = get_tweets_for_model(
            negative_cleaned_tokens_list)

        positive_dataset = [(tweet_dict, 1)
                             for tweet_dict in positive_tokens_for_model]

        negative_dataset = [(tweet_dict, 0)
                            for tweet_dict in negative_tokens_for_model]

        dataset = positive_dataset + negative_dataset

        random.shuffle(dataset)
        train_data = dataset[:7000]
        test_data = dataset[7000:]
        self.classifier = NaiveBayesClassifier.train(train_data)
        self.accuracy = classify.accuracy(self.classifier, test_data)

    def predict(self, tweet):
        tokens = remove_noise(word_tokenize(tweet))
        return self.classifier.classify(
            dict([token, True] for token in tokens))


if __name__ == "__main__":
    x = TweetSentimentClassifier()
    custom_tweet = "Yo I ordered just once from Starbucks, they screwed up, never used the app again."
    prediction = x.predict(custom_tweet)
    print(prediction)
