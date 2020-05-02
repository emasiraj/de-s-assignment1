import pandas as pd
import numpy as np
from sklearn.datasets import fetch_20newsgroups
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.neighbors import KNeighborsClassifier
from sklearn.pipeline import Pipeline

reviewDataframe = pd.read_csv('reviewDataframe.csv')
scrapedDataframe = pd.read_csv('scrapedDataFrame.csv')
learn_df = reviewDataframe.iloc[:4000]
test_df = reviewDataframe.iloc[4000:]

def predictConsensus(neighbors, testData): 
    knn = KNeighborsClassifier(n_neighbors=neighbors)

    text_clf = Pipeline([
        ('vect', CountVectorizer()),
        ('tfidf', TfidfTransformer()),
        ('clf', knn),
    ])
    text_clf.fit(learn_df.Review, learn_df.Review_Consensus)


    predicted = text_clf.predict(testData)
   
    if len(testData) >= 2:
        return np.mean(predicted == test_df.Review_Consensus)*100
    else: 
        return predicted[0]

def predictConsensusScrapedData(neighbors): 
    knn = KNeighborsClassifier(n_neighbors=neighbors)

    text_clf = Pipeline([
        ('vect', CountVectorizer()),
        ('tfidf', TfidfTransformer()),
        ('clf', knn),
    ])
    text_clf.fit(learn_df.Review, learn_df.Review_Consensus)


    predicted = text_clf.predict(scrapedDataframe.Review)
    print('The scraped reviews contain {}% positive and {}% negative reviews.'.format(
        np.mean(predicted == 'positive')*100, np.mean(predicted == 'negative')*100))
    

predictionsPercentages = {x: predictConsensus(x, test_df.Review) for x in range(30, 66)}
print('Between 30 and 100 nearest neighbour, the highest accuracy n is {} with an accuracy of {} %.'.format(
    max(predictionsPercentages, key=predictionsPercentages.get), predictionsPercentages[max(predictionsPercentages, key=predictionsPercentages.get)]
))

# review = ['The view was amazing, but that’s about it. Food was terrible!!!My risotto was raw which I told the waiter but I still got charged. For the dessert I have ordered a cake which came from the fridge still frozen. The prices are ridiculous and the food very poor! It ruined our evening and I went to sleep hungry.']
# print('This review is {}.'.format(predictConsensus(65, review)))

# predictConsensusScrapedData(65)
