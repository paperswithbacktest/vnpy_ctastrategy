from vnpy_ctastrategy import (
    CtaTemplate,
    StopOrder,
    TickData,
    BarData,
    TradeData,
    OrderData
)

from time import time


class TestStrategy(CtaTemplate):
    """"""
    author = "Trader in Python"

    test_trigger = 10

    tick_count = 0
    test_all_done = False

    parameters = ["test_trigger"]
    variables = ["tick_count", "test_all_done"]

    def __init__(self, cta_engine, strategy_name, vt_symbol, setting):
        """"""
        super().__init__(cta_engine, strategy_name, vt_symbol, setting)

        self.test_funcs = [
            self.test_market_order,
            self.test_limit_order,
            self.test_cancel_all,
            self.test_stop_order
        ]
        self.last_tick = None

    def on_init(self):
        """
        Callback when strategy is inited.
        """
        self.write_log("Strategy initialization")

    def on_start(self):
        """
        Callback when strategy is started.
        """
        self.write_log("Strategy started")

    def on_stop(self):
        """
        Callback when strategy is stopped.
        """
        self.write_log("Strategy stopped")

    def on_tick(self, tick: TickData):
        """
        Callback of new tick data update.
        """
        if self.test_all_done:
            return

        self.last_tick = tick

        self.tick_count += 1
        if self.tick_count >= self.test_trigger:
            self.tick_count = 0

            if self.test_funcs:
                test_func = self.test_funcs.pop(0)

                start = time()
                test_func()
                time_cost = (time() - start) * 1000
                self.write_log("Took %s milliseconds." % (time_cost))
            else:
                self.write_log("Testing is all done")
                self.test_all_done = True

        self.put_event()

    def on_bar(self, bar: BarData):
        """
        Callback of new bar data update.
        """
        pass

    def on_order(self, order: OrderData):
        """
        Callback of new order data update.
        """
        self.put_event()

    def on_trade(self, trade: TradeData):
        """
        Callback of new trade data update.
        """
        self.put_event()

    def on_stop_order(self, stop_order: StopOrder):
        """
        Callback of stop order update.
        """
        self.put_event()

    def test_market_order(self):
        """"""
        self.buy(self.last_tick.limit_up, 1)
        self.write_log("Executing market order test")

    def test_limit_order(self):
        """"""
        self.buy(self.last_tick.limit_down, 1)
        self.write_log("Executing limit order test")

    def test_stop_order(self):
        """"""
        self.buy(self.last_tick.ask_price_1, 1, True)
        self.write_log("Executing stoplist test")

    def test_cancel_all(self):
        """"""
        self.cancel_all()
        self.write_log("Executing cancel all test")
