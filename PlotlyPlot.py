import plotly.graph_objects as go
from plotly.subplots import make_subplots
import pandas as pd


class PlotlyPlot():
    """Plotly Plot

    Plot the stock data as well as indicator data.

    Args:
        time(pandas.Series): dataset 'Timestamp' column.
        close(pandas.Series): dataset 'Close' column.
        open(pandas.Series): dataset 'Open' column.
        high(pandas.Series): dataset 'High' column.
        low(pandas.Series): dataset 'Low' column.
        excludeMissing(bool): exclude missing dates.
    """

    def __init__(self,
                 time: pd.Series,
                 close: pd.Series,
                 open: pd.Series = None,
                 high: pd.Series = None,
                 low: pd.Series = None,
                 excludeMissing: bool = False):
        self._time = time
        self._open = open
        self._high = high
        self._low = low
        self._close = close
        self._fig = None
        self._data = None
        self._excludeMissing = excludeMissing
        self._getlayout()

    def _getlayout(self):
        margin = go.layout.Margin(
            b=50,
            t=50
        )
        if self._excludeMissing:
            self._layout = go.Layout(
                xaxis=dict(type='category'),
                margin=margin
            )
        else:
            self._layout = go.Layout(
                margin=margin
            )

    def candlestickplot(self,
                        increasing_line_color: str = 'green',
                        decreasing_line_color: str = 'red',
                        showlegend: bool = True
                        ):
        """Candlestick Plot

        Create the candlestick chart.

        Args:
            increasing_line_color(str): single candlestick color of increasing pattern.
            decreasing_line_color(str): single candlestick color of decreasing pattern.
            showlegend(bool): if True, show the legend
        """
        self._main_data = [
            go.Candlestick(
                x=self._time,
                open=self._open,
                high=self._high,
                low=self._low,
                close=self._close,
                name="Candlestick",
                increasing_line_color=increasing_line_color,
                decreasing_line_color=decreasing_line_color,
                showlegend=showlegend)
        ]

    def lineplot(self,
                 showlegend: bool = True
                 ):
        """Line Plot

        Create the close price line chart.

        Args:
            showlegend(bool): if True, show the legend
        """
        self._main_data = [
            go.Scatter(
                x=self._time,
                y=self._close,
                name="Close",
                showlegend=showlegend
            )]

    def ohlcplot(self,
                 increasing_line_color: str = 'green',
                 decreasing_line_color: str = 'red',
                 showlegend: bool = True
                 ):
        """OHLC Plot

        Create the OHLC chart

        Args:
            increasing_line_color(str): single candlestick color of increasing pattern.
            decreasing_line_color(str): single candlestick color of decreasing pattern.
            showlegend(bool): if True, show the legend
        """
        self._main_data = [
            go.Ohlc(
                x=self._time,
                open=self._open,
                high=self._high,
                low=self._low,
                close=self._close,
                name="OHLC",
                increasing_line_color=increasing_line_color,
                decreasing_line_color=decreasing_line_color,
                showlegend=showlegend
            )
        ]
    
    def _plot(self, slider, layout):
        if not layout:
            self._fig = go.Figure(
                data=self._main_data,
                layout=self._layout
            )
        else:
            self._fig = go.Figure(
                data=self._main_data,
                layout=layout
            )
        self._fig.update_layout(xaxis_rangeslider_visible=slider)

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
        self._fig.show()

    def addTrace(self,
                 time: pd.Series,
                 indicator_data: pd.Series,
                 name: str = "",
                 showlegend: bool = True
                 ):
        """Add Trace

        Adding indicator data to the main stock figure

        Args:
            time(pandas.Series): dataset 'Timestamp' column.
            indicator_data(pandas.Series): dataset 'indicator_data' column.
            name(str): name of the indicator
            showlegend(bool): if True, show the legend
        """
        self._main_data.append(
            go.Scatter(
                x=time,
                y=indicator_data,
                name=name,
                showlegend=showlegend
            )
        )
    
    def _subplot(self,
                 time: pd.Series,
                 indicator_datas: list,
                 names: list,
                 positions: list,
                 row_scale: list,
                 showlegend: bool = True,
                 layout: go.layout = None,
                 ):
        self._fig = make_subplots(
            rows=len(row_scale),
            shared_xaxes=True,
            shared_yaxes=True,
            cols=1,
            print_grid=False,
            vertical_spacing=0.05,
            row_heights=row_scale
        )
        # main plot
        for i in range(len(self._main_data)):
            self._fig.add_trace(self._main_data[i], row=1, col=1)

        # subplot
        for i in range(len(indicator_datas)):
            self._fig.add_trace(go.Scatter(
                x=time,
                y=indicator_datas[i],
                name=names[i],
                showlegend=showlegend
            ), row=positions[i] + 1, col=1
            )
        if not layout:
            self._fig.update_layout(
                height=(500 + (len(row_scale) - 1) * 100),
                xaxis_rangeslider_visible=False
            )
        else:
            self._fig.layout = layout

        if self._excludeMissing:
            self._fig.layout.xaxis.type = 'category'

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

        self._fig.show()
    
    def _separatePlot(self,
                     time: pd.Series,
                     indicator_data: pd.Series,
                     name: str = "",
                     showlegend: bool = True,
                     height: int = 200,
                     layout: go.layout = None
                     ):
        line = go.Scatter(
            x=time,
            y=indicator_data,
            name=name,
            showlegend=showlegend
        )
        if not layout:
            layout = go.Layout(
                height=height,
                margin=go.layout.Margin(
                    b=50,
                    t=50,
                )
            )
        self._fig = go.Figure(data=[line], layout=layout)
        if self._excludeMissing:
            self._fig.layout.xaxis.type = 'category'
        
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
        self._separatePlot(time, indicator_data, name, showlegend, height, layout)
        self._fig.show()






if __name__ == '__main__':
    import yfinance as yf
    import pandas as pd

    from ta.momentum import RSIIndicator, StochasticOscillator

    data = yf.download(
                tickers = 'TSLA',
                period =  "1mo",
                group_by = 'ticker',
                auto_adjust = True,
                prepost = False,
                threads = True,
            )
    df = data.reset_index()
    df['Date'] = pd.to_datetime(df['Date'])
    df['EMA_9'] = df['Close'].ewm(span=9, adjust=False).mean()
    df['RSI'] = RSIIndicator(close=df['Close'], n=14).rsi()
    indicator = StochasticOscillator(high=df['High'], low=df['Low'], close=df['Close'], n=14, d_n=3)
    df['Stoch'] = indicator.stoch()
    df['Stoch_signal'] = indicator.stoch_signal()

    pp = PlotlyPlot(
                time=df['Date'],
                close=df['Close'],
                open=df['Open'],
                high=df['High'],
                low=df['Low']
            )
    pp.candlestickplot(showlegend=False)
    pp.addTrace(time=df['Date'],
                indicator_data=df['EMA_9'],
                name="EMA_9",
               showlegend=False)

    pp.subplot(time=df['Date'],
                indicator_datas=[df['RSI'],df['Stoch'],df['Stoch_signal']],
                names=["RSI",'Stoch','Stoch_signal'],
               positions=[1,2,2],
               row_scale = [0.6,0.2,0.2],
                showlegend=True)
