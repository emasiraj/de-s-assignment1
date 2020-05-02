import pandas as pd
import numpy as np
from sklearn.datasets import fetch_20newsgroups
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.naive_bayes import MultinomialNB
from sklearn.pipeline import Pipeline

reviewDataframe = pd.read_csv('reviewDataframe.csv')
scrapedDataframe = pd.read_csv('scrapedDataFrame.csv')
learn_df = reviewDataframe.iloc[:4000]
test_df = reviewDataframe.iloc[4000:]

text_clf = Pipeline([
        ('vect', CountVectorizer()),
        ('tfidf', TfidfTransformer()),
        ('clf', MultinomialNB()),
    ])
text_clf.fit(learn_df.Review, learn_df.Review_Consensus)

def naiveBayesPredictions():
    predicted = text_clf.predict(test_df.Review)
    print('The Naive Bayes classifier got an accuracy of',np.mean(predicted == test_df.Review_Consensus)*100, '% over the test data.')

def naiveBayesPredictionsScrapedData():
    predicted = text_clf.predict(scrapedDataframe.Review)
    print('The scraped reviews contain {}% positive and {}% negative reviews.'.format(
        np.mean(predicted == 'positive')*100, np.mean(predicted == 'negative')*100))

def predictSingleReview(review):
    singlePredict = text_clf.predict(review)
    print('This review is {}.'.format(singlePredict[0]))


review = ['We spent over 2 weeks in Italy, and probably had 40 meals. This was the worst by far! We canceled a reservation and another high-end restaurant to try this one, and we were guests at the Hotel Danieli. For almost 400 euros, the food was terrible, and the service was worse. The view is fantastic, but hardly worth a terrible meal and a 16 euro per person cover charge. Oh, and to top it all off, a seagull pooped on my wife. Wonderful experience!']
# handWrittenReviews = []
# predictSingleReview(review)
naiveBayesPredictions()
# naiveBayesPredictionsScrapedData()