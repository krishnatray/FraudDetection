import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import cPickle as pickle

graph = True

def feature_importance(rf):
    plt.style.use('seaborn-white')
    importances = rf.feature_importances_
    std = np.std([tree.feature_importances_ for tree in rf.estimators_], axis=0)
    idxs = np.argsort(importances)[::-1]

    col_labels = ['sale_duration', 'channels', 'delivery_method', 'user_type', 'fb_published', 'num_order', 'num_previous_payouts', 'total_cost', 'fraud']

    col_labels = {idx: label for idx, label in enumerate(col_labels)}

    # Print the ranking
    print('Feature ranking:')
    for feat in range(importances.shape[0]):
        print("{}. {} ({})".format(feat+1, col_labels.get(idxs[feat], idxs[feat]), importances[idxs[feat]]))

    plt.figure(figsize=(10, 8))
    plt.title('Feature Importances')

    plt.bar(range(importances.shape[0]), importances[idxs], yerr=std[idxs], align='center')
    xticks = [col_labels.get(idx, idx) for idx in idxs]
    plt.xticks(range(importances.shape[0]), xticks, rotation=-45)
    plt.xlim([-1, importances.shape[0]])
    plt.tight_layout()

    plt.show()

if __name__ == "__main__":

    # read in a single example and vectorize
    df = pd.read_csv('../data/test_script_examples.csv').iloc[0]
    y = df.pop('fraud')
    x = df.values.reshape(1, -1)

    # unpickle model
    with open("model.pkl") as f:
        model = pickle.load(f)

    # predict probability
    y = model.predict(x)[0]

    # print probability
    print y
    if graph:
        feature_importance(model)
