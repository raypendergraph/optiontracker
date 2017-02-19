from _operator import add
from collections import namedtuple
from functools import reduce
from typing import List

from core.types import SecurityPosition, OptionPosition, StrategyAdjustment, CoveredCallStrategyMetrics


def exercised_strategy_metrics(entry_position: SecurityPosition,
                               options: List[OptionPosition],
                               adjustments: List[StrategyAdjustment]):

    assert entry_position.shares == reduce(add, (option.contracts * 100 for option in
                                                 options)), 'The total number of securities must match the number of contracts.'

    security_proceeds = reduce(add, (option.strike * option.contracts * 100 for option in options))
    premium_proceeds = reduce(add, (option.premium for option in options))
    adjustments_value = reduce(add, (adjustment.value for adjustment in adjustments))

    # Adjustments are individually credit or debit adjustments. Commissions and fees are negative
    # adjustments and dividends are positive.

    # For whatever reason McMillan does not apply any closing commissions to the net investment figures and
    # for break even cost only applies dividends received. This considers all fees and income from dividends
    # when calculating the net position which seems to me to be a more holistic approach. So the result is the
    # downside protection and break even price are not as `optimistic`.
    net_strategy_cost = entry_position.market_value - adjustments_value - premium_proceeds
    net_profit = security_proceeds - net_strategy_cost
    roi = net_profit / net_strategy_cost
    share_break_even_cost = net_strategy_cost / entry_position.shares
    downside_protection = (entry_position.market_value - net_strategy_cost) / entry_position.market_value

    return CoveredCallStrategyMetrics(net_profit, roi, share_break_even_cost, downside_protection)
