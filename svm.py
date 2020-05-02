import pandas as pd
import numpy as np
from sklearn.datasets import fetch_20newsgroups
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfTransformer
from sklearn import svm
from sklearn.pipeline import Pipeline
from sklearn.naive_bayes import MultinomialNB
from sklearn.model_selection import GridSearchCV
from sklearn.feature_extraction.text import TfidfVectorizer

reviewDataframe = pd.read_csv('reviewDataframe.csv')
scrapedDataframe = pd.read_csv('scrapedDataFrame.csv')
learn_df = reviewDataframe.iloc[:4000]
test_df = reviewDataframe.iloc[4000:]

tf_vect = TfidfVectorizer(lowercase=True, use_idf=True,
                          smooth_idf=True, sublinear_tf=False)
X_train_tf = tf_vect.fit_transform(learn_df.Review)


def svc_param_selection(X, y, nfolds):
    Cs = [0.001, 0.01, 0.1, 1, 10]
    gammas = [0.001, 0.01, 0.1, 1]
    param_grid = {'C': Cs, 'gamma': gammas}
    grid_search = GridSearchCV(svm.SVC(kernel='linear'), param_grid,
                               cv=nfolds)
    grid_search.fit(X, y)
    return grid_search.best_params_


def supportVectorMachinePredictions():
    svcParameters = svc_param_selection(X_train_tf, learn_df.Review_Consensus, 5)
    text_clf = Pipeline([
        ('vect', CountVectorizer()),
        ('tfidf', TfidfTransformer()),
        ('clf', svm.SVC(C=svcParameters['C'], kernel='linear',
                        degree=3, gamma=svcParameters['gamma'])),
    ])
    text_clf.fit(learn_df.Review, learn_df.Review_Consensus)

    predicted = text_clf.predict(test_df.Review)
    return np.mean(predicted == test_df.Review_Consensus)*100

def supportVectorMachinePredictionsScrapedData():
    svcParameters = svc_param_selection(X_train_tf, learn_df.Review_Consensus, 5)
    text_clf = Pipeline([
        ('vect', CountVectorizer()),
        ('tfidf', TfidfTransformer()),
        ('clf', svm.SVC(C=svcParameters['C'], kernel='linear',
                        degree=3, gamma=svcParameters['gamma'])),
    ])
    text_clf.fit(learn_df.Review, learn_df.Review_Consensus)

    predicted = text_clf.predict(scrapedDataframe.Review)
    return np.mean(predicted == 'positive')*100, np.mean(predicted == 'negative')*100


def supportVectorMachinePredictionsSingle(review):
    svcParameters = svc_param_selection(
        X_train_tf, learn_df.Review_Consensus, 5)
    text_clf = Pipeline([
        ('vect', CountVectorizer()),
        ('tfidf', TfidfTransformer()),
        ('clf', svm.SVC(C=svcParameters['C'],
                        kernel='linear',
                        degree=3,
                        gamma=svcParameters['gamma'])
         ),
    ])
    text_clf.fit(learn_df.Review, learn_df.Review_Consensus)

    predicted = text_clf.predict(review)
    return predicted[0]


print("Accuracy of {}%.".format(supportVectorMachinePredictions()))

# review = ['We celebrated our daughter’s 22nd birthday at the Daniele’s Hotel roof top Terrace. The view was spectacular over looking Venice. We also had the opportunity to watch the Venice Regatta. An exceptional experience!']
# print("This is a {} review.".format(supportVectorMachinePredictionsSingle(review)))

# print("The scraped reviews contain {}% positive and {}% negative reviews.".format(supportVectorMachinePredictionsScrapedData()[0], supportVectorMachinePredictionsScrapedData()[1]))
