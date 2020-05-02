import database
import os
import fnmatch
from textblob import TextBlob
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from nltk.corpus import stopwords
from nltk import pos_tag,pos_tag_sents
import regex as re
import operator
from sklearn.svm import SVC, LinearSVC
from sklearn.metrics import classification_report, accuracy_score, confusion_matrix
from sklearn.model_selection import train_test_split  
from sklearn import metrics
from sklearn import svm
from sklearn.model_selection import GridSearchCV
import pickle
from nltk.corpus import stopwords

SVMDataFrame = database.reviewDataframe

stopwordsColumn = stopwords.words('english')
SVMDataFrame['review_without_stopwords'] = SVMDataFrame['Review'].apply(lambda x: ' '.join([word for word in x.split() if word not in (stopwordsColumn)]))

def pos(review_without_stopwords):
    return TextBlob(review_without_stopwords).tags

os = SVMDataFrame.review_without_stopwords.apply(pos)
os1 = pd.DataFrame(os)
os1['pos'] = os1['review_without_stopwords'].map(lambda x:" ".join(["/".join(x) for x in x ]) )
SVMDataFrame = SVMDataFrame = pd.merge(SVMDataFrame, os1,right_index=True,left_index = True)
# pd.set_option('display.max_columns', 6)
review_train, review_test, label_train, label_test = train_test_split(SVMDataFrame['pos'],SVMDataFrame['Review_Consensus'], test_size=0.2,random_state=13)

tf_vect = TfidfVectorizer(lowercase = True, use_idf=True, smooth_idf=True, sublinear_tf=False)

X_train_tf = tf_vect.fit_transform(review_train)
X_test_tf = tf_vect.transform(review_test)

# def svc_param_selection(X, y, nfolds):
#     Cs = [0.001, 0.01, 0.1, 1, 10]
#     gammas = [0.001, 0.01, 0.1, 1]
#     param_grid = {'C': Cs, 'gamma' : gammas}
#     grid_search = GridSearchCV(svm.SVC(kernel='linear'), param_grid, cv=nfolds)
#     grid_search.fit(X, y)
#     return grid_search.best_params_

# print(svc_param_selection(X_train_tf,label_train,5))
# {'C': 1, 'gamma': 0.001}

# clf = svm.SVC(C=1,gamma=0.001,kernel='linear')
# clf.fit(X_train_tf,label_train)
# pred = clf.predict(X_test_tf)

# with open('vectorizer.pickle', 'wb') as fin:
#     pickle.dump(tf_vect, fin)
# with open('mlmodel.pickle','wb') as f:
#     pickle.dump(clf,f)

pkl = open('mlmodel.pickle', 'rb')
clf = pickle.load(pkl)   
vec = open('vectorizer.pickle', 'rb')
tf_vect = pickle.load(vec)

X_test_tf = tf_vect.transform(review_test)
pred = clf.predict(X_test_tf)

print(metrics.accuracy_score(label_test, pred))
print (confusion_matrix(label_test, pred))
print (classification_report(label_test, pred))

# print(SVMDataFrame.head(1))