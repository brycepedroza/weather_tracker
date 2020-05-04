import pandas as pd
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression

file_name = "./output/classified_data.csv"
columns = ["weather", "tweet"]


def read_data(path, names):
    df = pd.read_csv(
        path, usecols=names, sep=",", header=0)
    return df


if __name__ == "__main__":
    tweets_df = read_data(file_name, columns)
    tweets = tweets_df['tweet'].values
    y = tweets_df['weather'].values

    tweets_train, tweets_test, y_train, y_test = train_test_split(
        tweets, y, test_size=0.25)

    vectorizer = CountVectorizer()
    vectorizer.fit(tweets_train)

    X_train = vectorizer.transform(tweets_train)
    X_test = vectorizer.transform(tweets_test)

    classifier = LogisticRegression()
    classifier.fit(X_train, y_train)
    score = classifier.score(X_test, y_test)

    print("Accuracy:", score)

    """
    To Predict
    tweet = "this is my tweet"
    tweet_vector = vectorizer.transform([tweet])
    prediction = classifier.predict(test)[0]
    # If it is 1 then it is related to weather. Get the sentiment and  weather data at that location
    """
    # classifier.predict()