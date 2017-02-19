from collections import namedtuple
from enum import Enum
from typing import SupportsFloat, SupportsInt, Union

from datetime import date

FloatValue = Union[float, SupportsFloat]
IntValue = Union[int, SupportsInt]


class SecurityPosition(namedtuple("SecurityPositionBase", ('market_price', 'shares'))):
    def __new__(cls, cost_basis: FloatValue, shares: IntValue):
        return super(SecurityPosition, cls).__new__(cls, float(cost_basis), int(shares))

    @property
    def market_price(self) -> float:
        return self[0]

    @property
    def shares(self) -> int:
        return self[1]

    @property
    def market_value(self) -> float:
        return self.market_price * self.shares


OptionContractBase = namedtuple('OptionContractPositionBase', ('expiry', 'strike', 'contract_value', 'contracts'))


class OptionPosition(OptionContractBase):
    def __new__(cls, expiry: date, strike: FloatValue, contract_value: FloatValue, contracts: IntValue):
        return super(OptionPosition, cls).__new__(cls, date, float(strike), float(contract_value), int(contracts))

    @property
    def date(self) -> date:
        return self[0]

    @property
    def strike(self) -> float:
        return self[1]

    @property
    def contract_value(self) -> float:
        return self[2]

    @property
    def contracts(self) -> int:
        return self[3]

    @property
    def premium(self) -> float:
        return float(self.contracts) * 100.0 * self.contract_value


class StrategyAdjustmentType(Enum):
    TradingFee = 1
    OptionCommission = 2
    Dividend = 3


class StrategyAdjustment(namedtuple('AdjustmentBase', ('adjustment_amount', 'applied_quantity', 'type'))):
    def __new__(cls, adjustment_amount: FloatValue, applied_quantity: IntValue, type: StrategyAdjustmentType):
        return super(StrategyAdjustment, cls).__new__(cls, float(adjustment_amount), int(applied_quantity), type)

    @property
    def adjustment_amount(self) -> float:
        return self[0]

    @property
    def applied_quantity(self) -> int:
        return self[1]

    @property
    def type(self):
        return self[2]

    @property
    def value(self) -> float:
        return self.adjustment_amount * self.applied_quantity


CoveredCallStrategyMetricsBase = namedtuple('CoveredCallStrategyMetrics',
                                            ('net_profit', 'roi', 'share_break_even', 'downside_protection'))


class CoveredCallStrategyMetrics(CoveredCallStrategyMetricsBase):
    def __new__(cls, net_profit: FloatValue, roi: FloatValue,
                share_break_even: FloatValue, downside_protection: FloatValue):
        return super(CoveredCallStrategyMetrics, cls).__new__(cls, float(net_profit), float(roi),
                                                              float(share_break_even), float(downside_protection))

    @property
    def net_profit(self) -> float:
        return self[0]

    @property
    def roi(self) -> float:
        return self[1]

    @property
    def share_break_even(self) -> float:
        return self[2]

    @property
    def downside_protection(self) -> float:
        return self[3]

CoveredCallStrategyMetrics.Zero = CoveredCallStrategyMetrics(0, 0, 0, 0)