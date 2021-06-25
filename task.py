"""
Objective: We like to automate our buy and sell trades based on rules.
Scope: Test task with any 2 rules.
Skill needed: Python, Mathematical formulas, TA-lib, Pyalgotrade, Zipline.io  (not working)
"""
from pyalgotrade import strategy
from pyalgotrade.barfeed import quandlfeed
from pyalgotrade.technical import ma
import logging

# logging.basicConfig(format='[%(asctime)-15s %(levelname)s] %(message)s')

logger = logging.getLogger('task')
logger.setLevel(logging.DEBUG)


class MyStrategy(strategy.BacktestingStrategy):
    def __init__(self, feed: quandlfeed.Feed, instrument: str, cach: int, ema_period: int):
        super().__init__(feed, cach)
        self.__position = None
        self.__instrument = instrument
        # We'll use adjusted close values instead of regular close values.
        self.setUseAdjustedValues(True)
        self.__ema = ma.EMA(feed[instrument].getPriceDataSeries(), ema_period)

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
        if self.__ema[-1] is None:
            return

        bar = bars[self.__instrument]
        if self.__position is None:
            if bar.getPrice() > self.__ema[-1]:
                self.__position = self.enterLong(self.__instrument, 10, True)
        elif bar.getPrice() < self.__ema[-1] and not self.__position.exitActive():
            self.__position.exitMarket()


def run_strategy(cach, ema_period):
    import glob
    # Load the bar feed from the CSV file
    instrument = 'orcl'
    feed = quandlfeed.Feed()
    for f in glob.glob('WIKI-ORCL*.csv'):
        logger.info('load %s' % f)
        feed.addBarsFromCSV(instrument, f)

    # Evaluate the strategy with the feed's bars
    my_strategy = MyStrategy(feed, instrument, cach, ema_period)
    my_strategy.run()
    logger.info("Final portfolio value: $%.2f", my_strategy.getBroker().getEquity())


run_strategy(100000, 50)
