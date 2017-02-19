from enum import Enum
from re import _compile_repl

import core
from django.contrib.postgres.fields import jsonb
from django.utils import timezone
from django.db import models

from core.types import StrategyAdjustmentType


class OptionPositionType(Enum):
    Call = 1
    Put = 2


class AlertFrequencyType(Enum):
    OnDemand = 1
    Hourly = 2
    Daily = 3
    Weekly = 4
    BiWeekly = 5
    Monthly = 6


class StrategyAlert(models.Model):
    FrequencyChoices = (
        (AlertFrequencyType.OnDemand, 'On Demand'),
        (AlertFrequencyType.Hourly, 'Hourly'),
        (AlertFrequencyType.Daily, 'Daily'),
        (AlertFrequencyType.Weekly, 'Weekly'),
        (AlertFrequencyType.BiWeekly, 'Bi-Weekly'),
        (AlertFrequencyType.Monthly, 'Monthly'),
    )

    key = models.CharField(max_length=50)
    settings = jsonb.JSONField(null=True, blank=True)
    frequency = models.IntegerField(choices=FrequencyChoices, default=AlertFrequencyType.OnDemand.value)
    note = models.TextField(null=True, blank=True)


class Strategy(models.Model):
    date = models.DateField(default=timezone.now)
    alerts = models.ManyToManyField(StrategyAlert)
    is_tax_sheltered = models.BooleanField(default=False)

    @property
    def metrics(self) -> core.CoveredCallStrategyMetrics:
        if hasattr(self, '_cached_metrics'):
            return self._cached_metrics
        else:
            model = Strategy()
            options = [position.as_value_type() for position in model.optionposition_set.all()]
            if not options:
                self._cached_metrics = core.CoveredCallStrategyMetrics.Zero
            #TODO multiple securities
            entry_position = [security.as_value_type() for security in model.securityposition_set.all()]
            adjustments = [adjustment.as_value_type() for adjustment in model.adjustment_set.all()]
            self._cached_metrics = core.covered_call_exercised_strategy_metrics(entry_position, options, adjustments)

class SecurityPosition(models.Model):
    strategy = models.ForeignKey(Strategy)
    ticker = models.CharField(max_length=5)
    shares = models.IntegerField()
    purchase_date = models.DateField(default=timezone.now)
    purchase_price = models.PositiveIntegerField()
    sell_date = models.DateField()
    sell_price = models.PositiveIntegerField()

    def as_value_type(self):
        return core.SecurityPosition(self.purchase_price, self.shares)


class OptionPosition(models.Model):
    PositionChoices = (
        (OptionPositionType.Call.value, 'Call'),
        (OptionPositionType.Put.value, 'Put')
    )

    strategy = models.ForeignKey(Strategy)
    option_symbol = models.CharField(max_length=20, blank=False)
    contracts = models.IntegerField()
    expiry_date = models.DateField()
    strike = models.PositiveIntegerField()
    position_type = models.IntegerField(choices=PositionChoices, default=OptionPositionType.Call.value)
    entry_date = models.DateField(default=timezone.now)
    entry_price = models.PositiveIntegerField()
    exit_price = models.IntegerField()
    exit_date = models.DateField()
    rolled_to = models.ForeignKey('OptionPosition', related_name='rolled_from')
    note = models.TextField(null=True, blank=True)

    def as_value_type(self):
        return core.OptionPosition(self.expiry_date, self.strike, self.entry_price, self.contracts)


class StrategyAdjustment(models.Model):
    TypeChoices = (
        (core.StrategyAdjustmentType.TradingFee.value, 'Trading Fee'),
        (core.StrategyAdjustmentType.OptionCommission.value, 'Option Commission'),
        (core.StrategyAdjustmentType.Dividend.value, 'Dividend'),
    )
    strategy = models.ForeignKey(Strategy)
    date = models.DateField(timezone.now)
    quantity = models.PositiveSmallIntegerField()
    unit_amount = models.IntegerField()
    type = models.IntegerField(choices=TypeChoices, default=core.StrategyAdjustmentType.TradingFee.value)
    note = models.TextField(null=True, blank=True)

    def as_value_type(self):
        return core.StrategyAdjustment(self.unit_amount, self.quantity, StrategyAdjustmentType(self.type))
