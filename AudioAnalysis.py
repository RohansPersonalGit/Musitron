import json
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeClassifier
from sklearn.metrics import accuracy_score
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier

import pandas as pd
from sklearn import datasets

Features_constant  = ["duration_ms", "key", "mode", "time_signature", "acousticness", "dannceability", "energy", "instr", "liveness", "loudness", "speechiness", "valency", "temp"]
def load_songs():
    dataframe = pd.read_json("./audioanalysismysongs.json")
    print(dataframe)



def train_model():
    dataframe = pd.read_json("./audioanalysismysongs.json")
    train, test = train_test_split(dataframe, test_size=0.10)
    x_train = train[Features_constant]
    y_train = train["target"]

    x_test = test[Features_constant]
    y_test = test["target"]
    c = DecisionTreeClassifier(min_samples_split=100)
    dt = c.fit(x_train,y_train)
    y_pred = c.predict(x_test)
    score = accuracy_score(y_test, y_pred) * 100
    print("accuracy score uscition Desciion tree: ", round(score, 1), "%")

# Select the best split point for a dataset
def get_split(dataset, n_features):
    class_values = list(set(row[-1] for row in dataset))
    b_index, b_value, b_score, b_groups = 999, 999, 999, None
    features = list()
    while len(features) < n_features:
        index = randrange(len(dataset[0])-1)
        if index not in features:
            features.append(index)
    for index in features:
        for row in dataset:
            groups = test_split(index, row[index], dataset)
            gini = gini_index(groups, class_values)
            if gini < b_score:
                b_index, b_value, b_score, b_groups = index, row[index], gini, groups
    return {'index':b_index, 'value':b_value, 'groups':b_groups}
num_features_for_split = sqrt(Features_constant.count())
def main():
    # load_songs()
    train_model()
if __name__ == '__main__':
    main()