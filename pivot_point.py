import numpy as np
import pandas as pd

df = pd.read_csv('NIO.csv')
df['Date'] = pd.to_datetime(df['Date'])
df['Pre_month'] = df['Date'] - pd.DateOffset(months=1)

df_low = df['Low'].groupby([df.Date.dt.year.rename('year'), df.Date.dt.month.rename('month')]).min().reset_index().rename(columns={'Low':'LowPrev'})
df_high = df['High'].groupby([df.Date.dt.year.rename('year'), df.Date.dt.month.rename('month')]).max().reset_index().rename(columns={'High':'HighPrev'})
df_close = df['Close'].groupby([df.Date.dt.year.rename('year'), df.Date.dt.month.rename('month')]).last().reset_index().rename(columns={'Close':'ClosePrev'})
df2 = df_low.merge(df_high,on=['year','month']).merge(df_close,on=['year','month'])
df2 = df2[1:]

# Traditional
df2['PP'] = (df2['HighPrev'] + df2['LowPrev'] + df2['ClosePrev']) / 3
df2['R1'] = df2['PP'] * 2 - df2['LowPrev']
df2['S1'] = df2['PP'] * 2 - df2['HighPrev']
df2['R2'] = df2['PP'] + (df2['HighPrev'] - df2['LowPrev'])
df2['S2'] = df2['PP'] - (df2['HighPrev'] - df2['LowPrev'])
df2['R3'] = df2['PP'] * 2 + (df2['HighPrev'] - 2 * df2['LowPrev'])
df2['S3'] = df2['PP'] * 2 - (2 * df2['HighPrev'] - df2['LowPrev'])
df2['R4'] = df2['PP'] * 3 + (df2['HighPrev'] - 3 * df2['LowPrev'])
df2['S4'] = df2['PP'] * 3 - (3 * df2['HighPrev'] - df2['LowPrev'])
df2['R5'] = df2['PP'] * 4 + (df2['HighPrev'] - 4 * df2['LowPrev'])
df2['S5'] = df2['PP'] * 4 - (4 * df2['HighPrev'] - df2['LowPrev'])

df = df.merge(df2, how='left', left_on=[df['Pre_month'].dt.year,df['Pre_month'].dt.month], right_on=['year','month'])
df_result = df.drop(columns=['Adj Close', 'Volume','Pre_month', 'year', 'month', 'LowPrev', 'HighPrev', 'ClosePrev'])
df_result.to_csv('result.csv')


