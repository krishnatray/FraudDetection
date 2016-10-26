import pandas as pd

def clean_data(df):
    df = df[['sale_duration', 'previous_payouts', 'acct_type', 'org_name', 'payout_type', 'channels', 'country', 'delivery_method', 'ticket_types', 'has_analytics', 'listed', 'num_order']]

    #need to parse ticket_type
    df['cost'] = pd.Series([cell[0]['cost'] for cell in df['ticket_types']])
    df['qty_sold'] = pd.Series([cell[0]['quantity_sold'] for cell in df['ticket_types']])

    #need to parse previous_payouts
    df['num_previous_payouts']= [len(row) for row in df['previous_payouts']]

    #Remove ticket_types and previous_payours columns
    df.drop(['ticket_types', 'previous_payouts'], axis =1, inplace = True)

    return df


if __name__ == '__main__':
    filepath = '../data/subset.json'
    df = pd.read_json(filepath)
    df = clean_data(df)
    print df
