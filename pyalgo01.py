"""
This is very similar to the previous example, except that:

We’re initializing an SMA filter over the closing price data series.
We’re printing the current SMA value along with the closing price.
"""
from pyalgotrade import strategy
from pyalgotrade.barfeed import quandlfeed
from pyalgotrade.technical import ma


def safe_round(value, digits):
    if value is not None:
        value = round(value, digits)
    return value


class MyStrategy(strategy.BacktestingStrategy):
    def __init__(self, feed_: quandlfeed.Feed, instrument: str):
        super().__init__(feed_)
        # We want a 15 period SMA over the closing prices.
        self.__sma = ma.SMA(feed_[instrument].getCloseDataSeries(), 15)
        self.__instrument = instrument

    def onBars(self, bars):
        bar = bars[self.__instrument]
        self.info('%s %s' % (bar.getClose(), safe_round(self.__sma[-1], 2)))


# Load the bar feed from the CSV file
feed = quandlfeed.Feed()
feed.addBarsFromCSV('orcl', 'WIKI-ORCL-2000-quandl.csv')

# Evaluate the strategy with the feed's bars
myStrategy = MyStrategy(feed, 'orcl')
myStrategy.run()

# All the technicals will return None when the value can’t be calculated at a given time.
