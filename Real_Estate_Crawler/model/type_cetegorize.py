from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import FunctionTransformer
from sklearn.metrics import accuracy_score, recall_score, precision_score, f1_score
from sklearn.svm import SVC
import pandas as pd
from joblib import dump
from model.cleaner import cleanRealEstateDescription

pipeline = Pipeline(steps=[('clean',FunctionTransformer(func=cleanRealEstateDescription)),
                           ('tf-idf', TfidfVectorizer(ngram_range=(1,3), max_features=10000)),
                           ('classifier', SVC())])
data = pd.read_csv('../crawling_real_estate_alonhadat.com.vn.csv',header=None,
                   names=['title', 'value', 'area', 'address', 'ward', 'district', 'province',
                          'type', 'description', 'sellerName', 'time', 'source', 'image'])
data["text"] = data.apply(lambda x: x["title"]+" "+x["description"], axis=1)
train = data.sample(frac=0.7, random_state=15)
test = data.drop(train.index)
model = pipeline.fit(X=train["text"],y=train["type"])
dump(model, "typeClassifier.joblib")
predict = model.predict(X=test["text"])
print("Accuracy :", accuracy_score(y_true=test["type"], y_pred=predict))
print("Precision :", precision_score(y_true=test["type"], y_pred=predict,average="macro", zero_division=1))
print("Recall :", recall_score(y_true=test["type"], y_pred=predict,average="macro", zero_division=1))
print("F1-score :", f1_score(y_true=test["type"], y_pred=predict, average="macro", zero_division=1))