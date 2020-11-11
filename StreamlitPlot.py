import streamlit as st
import yfinance as yf
import pandas as pd
from PlotlyPlot import PlotlyPlot
from ta.momentum import RSIIndicator, StochasticOscillator
import plotly.graph_objects as go

class StreamlitPlot(PlotlyPlot):
    def __init__(self,
                 df: pd.DataFrame,
                 time: str = 'Date',
                 close: str = 'Close',
                 open: str = 'Open',
                 high: str = 'Open',
                 low: str = 'Low',
                 excludeMissing: bool = False):
        self._time = df[time]
        self._open = df[open]
        self._high = df[high]
        self._low = df[low]
        self._close = df[close]
        self._fig = None
        self._data = None
        self._excludeMissing = excludeMissing
        self._getlayout()
        self._df = self._get_data(df)
        self._run()

    @st.cache
    def _get_data(self,df):
        return df

    def _run(self):
        st.title("TA Library streamlit plot")
        st.dataframe(self._df)

    def plot(self,
             slider: str = True,
             layout: go.Layout = None):
        """Plot

        Ploting existing figure

        Args:
            slider(bool): if True, show the slider.
            layout(go.Layout): customize layout for the plot.
        """
        self._plot(slider, layout)
        st.plotly_chart(self._fig)

    def subplot(self,
                time: pd.Series,
                indicator_datas: list,
                names: list,
                positions: list,
                row_scale: list,
                showlegend: bool = True,
                layout: go.layout = None
                ):
        """Subplot

        Create a subplots of plot of indicator data

        Args:
            time(pandas.Series): dataset 'Timestamp' column.
            indicator_datas(list): list of dataset 'indicator_data' columns.
            names(list): list of names of the indicators
            positions(list): list of positions of the subplot of indicator_data
            row_scale(list): list of row scale of the plots
            showlegend(bool): if True, show the legend
            layout(go.Layout): customize layout for the subplot.
        """
        self._subplot(time, indicator_datas, names, positions, row_scale, showlegend, layout)
        st.plotly_chart(self._fig)

    def separatePlot(self,
                     time: pd.Series,
                     indicator_data: pd.Series,
                     name: str = "",
                     showlegend: bool = True,
                     height: int = 200,
                     layout: go.layout = None
                     ):
        """Separate Plot

        Create a separate of plot of indicator data

        Args:
            time(pandas.Series): dataset 'Timestamp' column.
            indicator_data(pandas.Series): dataset 'indicator_data' column.
            name(str): name of the indicator
            showlegend(bool): if True, show the legend
            height(int): height of the plot
            layout(go.Layout): customize layout for the separate plot.
        """
        self._separatePlot(time, indicator_data, name, showlegend, height)
        st.plotly_chart(self._fig)


data = yf.download(
        tickers='TSLA',
        period="1mo",
        group_by='ticker',
        auto_adjust=True,
        prepost=False,
        threads=True,
    )
df = data.reset_index()
df['Date'] = pd.to_datetime(df['Date'])
df['EMA_9'] = df['Close'].ewm(span=9, adjust=False).mean()
df['RSI'] = RSIIndicator(close=df['Close'], n=14).rsi()
indicator = StochasticOscillator(high=df['High'], low=df['Low'], close=df['Close'], n=14, d_n=3)
df['Stoch'] = indicator.stoch()
df['Stoch_signal'] = indicator.stoch_signal()

sp = StreamlitPlot(df)
sp.candlestickplot(showlegend=False)
sp.addTrace(time=df['Date'],
            indicator_data=df['EMA_9'],
            name="EMA_9",
            showlegend=False)
sp.plot()

sp.candlestickplot(showlegend=False)
sp.addTrace(time=df['Date'],
            indicator_data=df['EMA_9'],
            name="EMA_9",
            showlegend=False)
sp.subplot(time=df['Date'],
            indicator_datas=[df['RSI'],df['Stoch'],df['Stoch_signal']],
            names=["RSI",'Stoch','Stoch_signal'],
            positions=[1,2,2],
            row_scale = [0.6,0.2,0.2],
            showlegend=True)





