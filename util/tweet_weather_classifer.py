from sklearn.feature_extraction.text import CountVectorizer
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
import pandas as pd

FILE_NAME = "./backend_workflows/output/classified_data.csv"
COLUMNS = ["weather", "tweet"]


class TweetWeatherClassifier:
    def __init__(self, training_path):
        self.training_data = read_data(training_path, COLUMNS)
        self.vectorizer = CountVectorizer()
        self.vectorizer.fit(self.training_data)
        self.score = 0
        self.classifier = self.train()

    def train(self):
        tweets = self.training_data['tweet'].values
        y = self.training_data['weather'].values

        tweets_train, tweets_test, y_train, y_test = train_test_split(
            tweets, y, test_size=0.25)

        x_train = self.vectorizer.transform(tweets_train)
        x_test = self.vectorizer.transform(tweets_test)

        classifier = LogisticRegression()
        classifier.fit(x_train, y_train)
        score = classifier.score(x_test, y_test)
        self.score = score

        return classifier

    def predict(self, tweet):
        """
        Run a tweet through a classifier to predict if the tweet
         is about the weather. Return 1 for true, 0 for false
        :param tweet: tweet
        :return: 1 = about weather, 0 = not
        """
        tweet_vector = self.vectorizer.transform([tweet])
        return self.classifier.predict(tweet_vector)[0]


def read_data(path, names):
    """
    Read Tweet Data For Training
    :param path: path to tweet csv
    :param names: columns to grab
    :return: tweet dataframe
    """
    return pd.read_csv(
        path, usecols=names, sep=",", header=0)


if __name__ == "__main__":
    x = TweetWeatherClassifier("../backend_workflows/output/classified_data.csv")
    custom_tweet = "Escondido CA Tue May 5th PM Forecast: TONIGHT Mostly Clear Lo 61 WEDNESDAY Mostly Sunny Hi 95"
    prediction = x.predict(custom_tweet)
    print(prediction)