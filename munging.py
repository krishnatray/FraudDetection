import numpy as np
import pandas as pd

def clean_data(df):
    df = df[['sale_duration', 'previous_payouts', 'acct_type', 'org_name', 'payout_type', 'channels', 'country', 'delivery_method', 'ticket_types', 'has_analytics', 'listed', 'num_order']]

    #need to parse ticket_type
    # df['av_cost_of_tic']=[np.mean(row[num]['cost']) for row in df['ticket_types'] for num in range(len(row))]

    #need to parse previous_payouts
    df['num_previous_payouts']= [len(row) for row in df['previous_payouts']]

    #Remove ticket_types and previous_payours columns
    df.drop(['ticket_types', 'previous_payouts'], axis =1, inplace = True)

    #Make target column boolean
    df['fraud'] = pd.Series(['fraudster' in word for word in df['acct_type']])
    df.drop(['acct_type'], axis = 1, inplace = True)

    #convert listed to boolean
    df['listed'] = [df['listed'] == 'y']
    
    return df


def main():
    filepath = '../data/subset.json'
    df = pd.read_json(filepath)
    df = clean_data(df)

if __name__ == '__main__':
    main()
