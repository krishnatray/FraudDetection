import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import confusion_matrix, precision_score, recall_score

def convert_data(df):
    df = df[['sale_duration', 'previous_payouts', 'acct_type', 'channels', 'delivery_method', 'ticket_types', 'has_analytics', 'listed', 'num_order']]

    #need to parse previous_payouts
    df['num_previous_payouts']= [len(row) for row in df['previous_payouts']]

    #Add total_cost
    total = []
    for row in df['ticket_types']:
        cost= 0
        for num in range(len(row)):
            cost +=row[num]['cost']
        total.append(cost)
    df['total_cost'] = total

    #Remove ticket_types and previous_payours columns
    df.drop(['ticket_types', 'previous_payouts'], axis =1, inplace = True)

    #Add Labels column and remove old labels columns
    df['fraud'] = pd.Series(['fraudster' in word for word in df['acct_type']])
    df.drop(['acct_type'], axis = 1, inplace = True)

    #convert listed to boolean
    df['listed'] = [val == 'y' for val in df['listed']]

    # dummies = pd.get_dummies(df['delivery_method'], drop_first = True)
    df.fillna(inplace = True, value = 44.66)

    return df

def split_data(df):
    y = df.pop('fraud').values
    X = df.values
    X_train, X_test, y_train, y_test = train_test_split(X, y)
    return X_train, X_test, y_train, y_test

def model_fit(X_train, X_test, y_train, y_test):
    rf = RandomForestClassifier()
    rf.fit(X_train, y_train)
    return rf

def confuse(model, X_test, y_test):
    y_predict = model.predict(X_test)
    return confusion_matrix(y_test, y_predict), y_predict

def score(model, X_test, y_test):
    score = model.score(X_test, y_test)
    return score

# def score_df(X_costs, prediction, actual):
#     cost_df = pd.DataFrame([X_costs], colnames='Cost')
#     cost_df['prediction'] = prediction
#     cost_df['actual'] = actual
#     return cost_df

def main():
    filepath = '../data/subset.json'
    df = pd.read_json(filepath)
    df = convert_data(df)
    X_train, X_test, y_train, y_test = split_data(df)
    model= model_fit(X_train, X_test, y_train, y_test)
    mat, y_pred = confuse(model, X_test, y_test)
    acc = score(model, X_test, y_test)
    return y_pred, X_test, y_test, mat, acc


if __name__ == "__main__":
    y_pred, X_test, y_test, mat, acc = main()
    print "Accuracy:", acc
