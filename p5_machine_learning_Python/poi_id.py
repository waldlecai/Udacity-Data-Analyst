#!/usr/bin/python

import sys
import pickle
sys.path.append("../tools/")
from sklearn.cross_validation import train_test_split
from sklearn import preprocessing
from sklearn.tree import DecisionTreeClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.naive_bayes import GaussianNB
from sklearn.grid_search import GridSearchCV

#### package provided by course
from feature_format import featureFormat, targetFeatureSplit
from tester import dump_classifier_and_data, test_classifier

### my own package
from poi_helper import addFeatures

### Task 1: Select what features you'll use.
### features_list is a list of strings, each of which is a feature name.
### The first feature must be "poi".
### 'poi','salary', 'bonus', 'total_payments', 'exercised_stock_options', 'total_stock_value', 
### 'expenses', 'from_poi_to_this_person', 'from_this_person_to_poi', 'shared_receipt_with_poi'

### 1.1 manual feature selection (use Decision Tree to verify)
### Accuracy: 0.70170	Precision: 0.25114	Recall: 0.24800
### features_list = ['poi','salary']

### 1.2 manual feature selection (use Decision Tree to verify)
### Accuracy: 0.74564	Precision: 0.26990	Recall: 0.23400
### features_list = ['poi','salary', 'from_this_person_to_poi']

### 1.3 manual feature selection
### Accuracy: 0.69691	Precision: 0.15689	Recall: 0.15250
### features_list = ['poi','salary', 'bonus', 'from_this_person_to_poi']

### 1.4 manual feature selection
### Accuracy: 0.73118	Precision: 0.22735	Recall: 0.19950	
### features_list = ['poi', 'salary', 'from_poi_to_this_person', 'from_this_person_to_poi']

### 1.5 manual feature selection
### Accuracy: 0.76892	Precision: 0.25919	Recall: 0.20800
### features_list = ['poi', 'salary', 'from_this_person_to_poi', 'from_poi_to_this_person', 'shared_receipt_with_poi']

### 1.6 manual feature selection
### Accuracy: 0.76421	Precision: 0.18407	Recall: 0.18950
### features_list = ['poi', 'salary', 'total_payments', 'from_this_person_to_poi', 'from_poi_to_this_person', 'shared_receipt_with_poi']

### 1.7 manual feature selection
### Accuracy: 0.81077	Precision: 0.37122	Recall: 0.33150
### features_list = ['poi', 'salary', 'exercised_stock_options', 'from_this_person_to_poi', 'from_poi_to_this_person', 'shared_receipt_with_poi']

### 1.8 manual feature selection (this gives best precision and recall)
### Accuracy: 0.83593	Precision: 0.42012	Recall: 0.39050
features_list = ['poi', 'salary', 'exercised_stock_options', 'expenses', 'from_this_person_to_poi', 'from_poi_to_this_person', 'shared_receipt_with_poi']

### 1.9 manual feature selection
### Accuracy: 0.82729	Precision: 0.39115	Recall: 0.37550
### features_list = ['poi', 'salary', 'exercised_stock_options', 'total_stock_value', 'expenses', 'from_this_person_to_poi', 'from_poi_to_this_person', 'shared_receipt_with_poi']

### Load the dictionary containing the dataset
with open("final_project_dataset.pkl", "r") as data_file:
    data_dict = pickle.load(data_file)

### Task 2: Remove outliers
data_dict.pop("TOTAL", 0)
data_dict.pop('THE TRAVEL AGENCY IN THE PARK', 0)

### Task 3: Create new feature(s)
### Store to my_dataset for easy export below.

### Adding new feature: ratio btw email involved POI and total emails
### Accuracy: 0.81750	Precision: 0.35835	Recall: 0.35100
### not better than without this new feature
features_list, my_dataset = addFeatures(features_list, data_dict)
### my_dataset = data_dict # withou new feature

### Extract features and labels from dataset for local testing
data = featureFormat(my_dataset, features_list, sort_keys = True)
labels, features = targetFeatureSplit(data)

### Scale the features
features = preprocessing.scale(features)

### Task 4: Try a varity of classifiers
### Please name your classifier clf for easy export below.
### Note that if you want to do PCA or other multi-stage operations,
### you'll need to use Pipelines. For more info:
### http://scikit-learn.org/stable/modules/pipeline.html
features_train, features_test, labels_train, labels_test = train_test_split(features, labels, test_size=0.3, random_state=42)

### 4.1 Decision Tree (selected for tuning)
### Accuracy: 0.81786	Precision: 0.35751	Recall: 0.34500
### better then .3 precision and recall

clf = DecisionTreeClassifier()
print("Decision Tree feature importance")
clf.fit(features_train, labels_train)
importances = clf.feature_importances_
for i in range(len(importances)):
	print("Importance is:{}".format(importances[i]))

### 4.2 GaussianNB 
### Accuracy: 0.83779	Precision: 0.38585	Recall: 0.22900
#clf = GaussianNB()

### 4.3 Logistic Regression 
### Accuracy: 0.65050	Precision: 0.05119	Recall: 0.08250
###clf = LogisticRegression()

### Task 5: Tune your classifier to achieve better than .3 precision and recall 
### using our testing script. Check the tester.py script in the final project
### folder for details on the evaluation method, especially the test_classifier
### function. Because of the small size of the dataset, the script uses
### stratified shuffle split cross validation. For more info: 
### http://scikit-learn.org/stable/modules/generated/sklearn.cross_validation.StratifiedShuffleSplit.html
"""
parameters = {'criterion':('gini', 'entropy'),'splitter':('best','random')}
dt_clf = DecisionTreeClassifier()
clf = GridSearchCV(dt_clf, parameters, scoring='recall')
clf.fit(features_train, labels_train)
print("Deciesion Tree Best Parameters")
print clf.best_params_
"""
### Task 6: Dump your classifier, dataset, and features_list so anyone can
### check your results. You do not need to change anything below, but make sure
### that the version of poi_id.py that you submit can be run on its own and
### generates the necessary .pkl files for validating your results.

dump_classifier_and_data(clf, my_dataset, features_list)


