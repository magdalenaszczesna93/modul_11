import pandas as pd
import datetime as dt
import os
import plotly.graph_objs as go


class db:
    def __init__(self):
        self.transactions = db.transation_init()
        self.cc = pd.read_csv(r'db\country_codes.csv',index_col=0)
        self.customers = db.customers_init()
        # self.customers = pd.read_csv(r'db\customers.csv',index_col=0)
        self.prod_info = pd.read_csv(r'db\prod_cat_info.csv')

    @staticmethod
    def transation_init():
        transactions = pd.DataFrame()
        src = r'db\transactions'
        for filename in os.listdir(src):
            transactions = transactions.append(pd.read_csv(os.path.join(src,filename),index_col=0))

        def convert_dates(x):
            try:
                return dt.datetime.strptime(x,'%d-%m-%Y')
            except:
                return dt.datetime.strptime(x,'%d/%m/%Y')
        transactions['tran_date'] = transactions['tran_date'].apply(lambda x: convert_dates(x))
        return transactions
    
    @staticmethod
    def customers_init(): 
        customers = pd.DataFrame()
        customers = customers.append(pd.read_csv(r'db\customers.csv', index_col=0))
        customers['DOB'] = pd.to_datetime(customers['DOB'], format='%d-%m-%Y')
        def pokolenie(row):
            if row['DOB'] <= dt.datetime(1946,12,31):
                return f'silent generation'
            elif row['DOB'] <= dt.datetime(1964,12,31):
                return f'baby boomers'
            elif row['DOB'] <= dt.datetime(1979,12,31):
                return f'pokolenie X'
            elif row['DOB'] <= dt.datetime(1996,12,31):
                return f'milenialsi'
            else:
                return f'pokolenie Z'

        customers['Pokolenie'] = customers.apply(lambda row: pokolenie(row), axis=1)
        
        return customers
    

    def merge(self):
        df = self.transactions.join(self.prod_info.drop_duplicates(subset=['prod_cat_code'])
        .set_index('prod_cat_code')['prod_cat'],on='prod_cat_code',how='left')

        df = df.join(self.prod_info.drop_duplicates(subset=['prod_sub_cat_code'])
        .set_index('prod_sub_cat_code')['prod_subcat'],on='prod_subcat_code',how='left')

        df = df.join(self.customers.join(self.cc,on='country_code').set_index('customer_Id'),on='cust_id')

        self.merged = df

df = db()
df.merge()
df=df.merged

import pandas as pd

print(df.columns)

# tutaj jest problem
grouped = df[df['total_amt']>0].pivot_table(index='Store_type',columns='Pokolenie',values='total_amt',aggfunc='sum').assign(
    _sum=lambda x: x['silent generation']+x['baby boomers']+x['pokolenie X']+x['milenialsi']+x['pokolenie Z']).sort_values(by='_sum').round(2)


traces = []
for col in ['silent generation','baby boomers','pokolenie X','milenialsi','pokolenie Z']:
    traces.append(go.Bar(x=grouped[col],y=grouped.index,orientation='h',name=col))

data = traces
fig = go.Figure(data=data,layout=go.Layout(title='Kanały sprzedaży według pokolenia',barmode='stack'))

grouped = df[df['total_amt']>0].groupby('Store_type')['total_amt'].sum().round(2).unstack()

print(grouped)