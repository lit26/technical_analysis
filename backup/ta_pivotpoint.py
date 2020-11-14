# timeframe = daily
import pandas as pd
df = pd.read_csv('data/NIO_D.csv')
df['Date'] = pd.to_datetime(df['Date'])

class PivotPoint():
    def __init__(self,
                 date: pd.Series,
                 low: pd.Series,
                 high: pd.Series,
                 close: pd.Series,
                 timeframe: str='D'):
        self._df = pd.concat([date, low, high, close], axis=1)
        self._df.set_index(date, inplace=True)
        self._timeframe = timeframe
        # self._run()

    def _run(self):
        _resample = None
        if self._timeframe == 'D':
            self._df['Last'] = self._df['Date'] - pd.DateOffset(months=1)
            _resample = 'M'
        elif self._timeframe == 'W' or self._timeframe == 'M':
            self._df['Last'] = self._df['Date'] - pd.DateOffset(years=1)
            _resample = 'A'

        # Get previous high, low, close
        _low = self._df['Low'].resample(_resample).min().reset_index().rename(columns={'Low': 'LowPrev'})
        _high = self._df['High'].resample(_resample).max().reset_index().rename(columns={'High': 'HighPrev'})
        _close = self._df['Close'].resample(_resample).last().reset_index().rename(columns={'Close': 'ClosePrev'})
        _df2 = _low.merge(_high, on='Date').merge(_close, on='Date')
        _df2 = _df2[1:]

        # Traditional
        _df2['PP'] = (_df2['HighPrev'] + _df2['LowPrev'] + _df2['ClosePrev']) / 3
        _df2['R1'] = _df2['PP'] * 2 - _df2['LowPrev']
        _df2['S1'] = _df2['PP'] * 2 - _df2['HighPrev']
        _df2['R2'] = _df2['PP'] + (_df2['HighPrev'] - _df2['LowPrev'])
        _df2['S2'] = _df2['PP'] - (_df2['HighPrev'] - _df2['LowPrev'])
        _df2['R3'] = _df2['PP'] * 2 + (_df2['HighPrev'] - 2 * _df2['LowPrev'])
        _df2['S3'] = _df2['PP'] * 2 - (2 * _df2['HighPrev'] - _df2['LowPrev'])
        _df2['R4'] = _df2['PP'] * 3 + (_df2['HighPrev'] - 3 * _df2['LowPrev'])
        _df2['S4'] = _df2['PP'] * 3 - (3 * _df2['HighPrev'] - _df2['LowPrev'])
        _df2['R5'] = _df2['PP'] * 4 + (_df2['HighPrev'] - 4 * _df2['LowPrev'])
        _df2['S5'] = _df2['PP'] * 4 - (4 * _df2['HighPrev'] - _df2['LowPrev'])

        _left_join = None
        _right_join = None
        if self._timeframe == 'D':
            _left_join = [self._df['Last'].dt.year, self._df['Last'].dt.month]
            _right_join = [_df2['Date'].dt.year,_df2['Date'].dt.month]

        elif self._timeframe == 'W' or self._timeframe == 'M':
            _left_join = [self._df['Last'].dt.year]
            _right_join = [_df2['Date'].dt.year]

        self._df = self._df.merge(_df2, how='left', left_on=_left_join, right_on=_right_join)


if __name__ == '__main__':
    df = pd.read_csv('data/NIO_D.csv')
    PivotPoint(date=df['Date'],low=df['Low'],high=df['High'],close=df['Close'])






# timeframe = 'D'
# resample = None
# if timeframe == 'D':
#     df['Last'] = df['Date'] - pd.DateOffset(months=1)
#     resample = 'M'
# elif timeframe == 'W' or timeframe == 'M':
#     df['Last'] = df['Date'] - pd.DateOffset(years=1)
#     resample = 'A'
#
# cols = ['Date_x','Open', 'High','Low','Close','Adj Close',
#                 'PP', 'R1','S1' , 'R2', 'S2', 'R3','S3','R4','S4','R5','S5']
# df.set_index(df["Date"],inplace=True)
#
# df_low = df['Low'].resample(resample).min().reset_index().rename(columns={'Low':'LowPrev'})
# df_high = df['High'].resample(resample).max().reset_index().rename(columns={'High':'HighPrev'})
# df_close = df['Close'].resample(resample).last().reset_index().rename(columns={'Close':'ClosePrev'})
# df2 = df_low.merge(df_high,on='Date').merge(df_close,on='Date')
# df2 = df2[1:]
#
# # Traditional
# df2['PP'] = (df2['HighPrev'] + df2['LowPrev'] + df2['ClosePrev']) / 3
# df2['R1'] = df2['PP'] * 2 - df2['LowPrev']
# df2['S1'] = df2['PP'] * 2 - df2['HighPrev']
# df2['R2'] = df2['PP'] + (df2['HighPrev'] - df2['LowPrev'])
# df2['S2'] = df2['PP'] - (df2['HighPrev'] - df2['LowPrev'])
# df2['R3'] = df2['PP'] * 2 + (df2['HighPrev'] - 2 * df2['LowPrev'])
# df2['S3'] = df2['PP'] * 2 - (2 * df2['HighPrev'] - df2['LowPrev'])
# df2['R4'] = df2['PP'] * 3 + (df2['HighPrev'] - 3 * df2['LowPrev'])
# df2['S4'] = df2['PP'] * 3 - (3 * df2['HighPrev'] - df2['LowPrev'])
# df2['R5'] = df2['PP'] * 4 + (df2['HighPrev'] - 4 * df2['LowPrev'])
# df2['S5'] = df2['PP'] * 4 - (4 * df2['HighPrev'] - df2['LowPrev'])
#
# left_join = [df['Last'].dt.year,df['Last'].dt.month]
# right_join = [df2['Date'].dt.year,df2['Date'].dt.month]
#
# df = df.merge(df2, how='left', left_on=left_join, right_on=right_join)
#
# df_result = df[cols]
#
# print(df_result)
# df_result.to_csv('result2.csv')