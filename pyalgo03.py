"""
This is very similar to the previous example, except that:

The first 14 RSI values are None. That is because we need at least 15 values to get an RSI value.
The first 28 SMA values are None. That is because the first 14 RSI values are None, and the 15th one is the
first not None value that the SMA filter receives. We can calculate the SMA(15) only when we have 15 not None values .
"""
from pyalgotrade import strategy
from pyalgotrade.barfeed import quandlfeed
from pyalgotrade.technical import ma, rsi


def safe_round(value, digits):
    if value is not None:
        value = round(value, digits)
    return value


class MyStrategy(strategy.BacktestingStrategy):
    def __init__(self, feed_: quandlfeed.Feed, instrument: str):
        super().__init__(feed_)
        self.__rsi = rsi.RSI(feed[instrument].getCloseDataSeries(), 14)
        # We want a 15 period SMA over the closing prices.
        self.__sma = ma.SMA(self.__rsi, 15)
        self.__instrument = instrument

    def onBars(self, bars):
        bar = bars[self.__instrument]
        self.info('%s %s %s' % (bar.getClose(), safe_round(self.__rsi[-1], 2), safe_round(self.__sma[-1], 2)))


# Load the bar feed from the CSV file
instrument_ = 'orcl'
feed = quandlfeed.Feed()
feed.addBarsFromCSV(instrument_, 'WIKI-ORCL-2000-quandl.csv')

# Evaluate the strategy with the feed's bars
myStrategy = MyStrategy(feed, instrument_)
myStrategy.run()

# All the technicals will return None when the value can’t be calculated at a given time.
