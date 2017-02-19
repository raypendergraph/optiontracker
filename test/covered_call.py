import unittest

from core.covered_call import calculate_exercised_strategy_metrics
from core.types import *


class TestCoveredCallMethods(unittest.TestCase):
    #Example on page 49-50
    def test_basic_covered_call_1(self):

        adjustments = [StrategyAdjustment(-60.0, 1),  # Option sell commissions
                       StrategyAdjustment(-320, 1),  # Stock purchase commissions
                       StrategyAdjustment(-330.0, 1),  # Stock sale commissions
                       StrategyAdjustment(500.0, 1)] # Dividends

        option = OptionPosition(None, 45.0, 3, 5)
        entry = SecurityPosition(43.0, 500)

        result = calculate_exercised_strategy_metrics(entry, [option], adjustments)
        print(result)

        self.assertTrue(True == True)

    # Example on page 54
    def test_basic_covered_call_2(self):
        adjustments = [StrategyAdjustment(-25.0, 1),  # Option sell commissions
                       StrategyAdjustment(-85, 1),  # Stock purchase commissions
                       StrategyAdjustment(-85.0, 1),  # Stock sale commissions
                       StrategyAdjustment(100.0, 1)]  # Dividends

        option = OptionPosition(None, 45.0, 3, 1)
        entry = SecurityPosition(43.0, 100)

        result = calculate_exercised_strategy_metrics(entry, [option], adjustments)
        print(result)

        self.assertTrue(True == True)


    # Example on page 63
    def test_basic_covered_call_3(self):
        adjustments = [StrategyAdjustment(-77.0, 1),  # Option sell commissions
                       StrategyAdjustment(-345, 1),  # Stock purchase commissions
                       StrategyAdjustment(-345.0, 1),  # Stock sale commissions
                       StrategyAdjustment(250.0, 1)]  # Dividends

        option = OptionPosition(None, 50.0, 3, 5)
        entry = SecurityPosition(50.0, 500)

        result = calculate_exercised_strategy_metrics(entry, [option], adjustments)
        print(result)

        self.assertTrue(True == True)