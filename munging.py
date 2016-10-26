import numpy as np
import pandas as pd

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

if __name__ == '__main__':
    filepath = '../data/data.json'
    df = pd.read_json(filepath)
    df = convert_data(df)
    df.to_csv('../data/clean_data.csv', index = False)
