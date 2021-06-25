"""
This is very similar to the previous example, except that:

The first 14 RSI values are None. That is because we need at least 15 values to get an RSI value.
The first 28 SMA values are None. That is because the first 14 RSI values are None, and the 15th one is the
first not None value that the SMA filter receives. We can calculate the SMA(15) only when we have 15 not None values .
"""
from pyalgotrade import strategy
from pyalgotrade.barfeed import quandlfeed
from pyalgotrade.technical import ma


class MyStrategy(strategy.BacktestingStrategy):
    def __init__(self, feed: quandlfeed.Feed, instrument: str, sma_period: int):
        super().__init__(feed, 1000)
        self.__position = None
        self.__instrument = instrument
        # We'll use adjusted close values instead of regular close values.
        self.setUseAdjustedValues(True)
        self.__sma = ma.SMA(feed[instrument].getPriceDataSeries(), sma_period)

    def onEnterOk(self, position):
        exec_info = position.getEntryOrder().getExecutionInfo()
        self.info("BUY at $%.2f" % (exec_info.getPrice()))

    def onEnterCanceled(self, position):
        self.__position = None

    def onExitOk(self, position):
        exec_info = position.getExitOrder().getExecutionInfo()
        self.info("SELL at $%.2f" % (exec_info.getPrice()))
        self.__position = None

    def onExitCanceled(self, position):
        # If the exit was canceled, re-submit it.
        self.__position.exitMarket()

    def onBars(self, bars):
        # Wait for enough bars to be available to calculate a SMA.
        if self.__sma[-1] is None:
            return

        bar = bars[self.__instrument]
        if self.__position is None:
            if bar.getPrice() > self.__sma[-1]:
                self.__position = self.enterLong(self.__instrument, 10, True)
        elif bar.getPrice() < self.__sma[-1] and not self.__position.exitActive():
            self.__position.exitMarket()


def run_strategy(sma_period):
    # Load the bar feed from the CSV file
    instrument = 'orcl'
    feed = quandlfeed.Feed()
    feed.addBarsFromCSV(instrument, 'WIKI-ORCL-2000-quandl.csv')

    # Evaluate the strategy with the feed's bars
    myStrategy = MyStrategy(feed, instrument, sma_period)
    myStrategy.run()
    print("Final portfolio value: $%.2f" % myStrategy.getBroker().getEquity())


run_strategy(15)
