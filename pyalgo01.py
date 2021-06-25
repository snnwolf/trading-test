"""
```bash
python -m "pyalgotrade.tools.quandl" --source-code="WIKI" --table-code="ORCL" --from-year=2000 --to-year=2000 --storage=. --force-download --frequency=daily
```

The code is doing 3 main things:
Declaring a new strategy. There is only one method that has to be defined, onBars, which is called for every bar in the feed.
Loading the feed from a CSV file.
Running the strategy with the bars supplied by the feed.
"""
from pyalgotrade import strategy
from pyalgotrade.barfeed import quandlfeed


class MyStrategy(strategy.BacktestingStrategy):
    def __init__(self, feed_: quandlfeed.Feed, instrument: str):
        super().__init__(feed_)
        self.__instrument = instrument

    def onBars(self, bars):
        bar = bars[self.__instrument]
        self.info(bar.getClose())


feed = quandlfeed.Feed()
feed.addBarsFromCSV('orcl', 'WIKI-ORCL-2000-quandl.csv')

myStrategy = MyStrategy(feed, 'orcl')
myStrategy.run()
