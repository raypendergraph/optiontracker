from enum import Enum

from django.contrib.postgres.fields import jsonb
from django.utils import timezone
from django.db import models


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


class SecurityPosition(models.Model):
    strategy = models.ForeignKey(Strategy)
    ticker = models.CharField(max_length=5)
    shares = models.IntegerField()
    purchase_date = models.DateField(default=timezone.now)
    purchase_price = models.PositiveIntegerField()
    sell_date = models.DateField()
    sell_price = models.PositiveIntegerField()


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


class StrategyAdjustmentType(Enum):
    TradingFee = 1
    OptionCommission = 2
    Dividend = 3


class StrategyAdjustment(models.Model):
    TypeChoices = (
        (StrategyAdjustmentType.TradingFee.value, 'Trading Fee'),
        (StrategyAdjustmentType.OptionCommission.value, 'Option Commission'),
        (StrategyAdjustmentType.Dividend.value, 'Dividend'),
    )
    strategy = models.ForeignKey(Strategy)
    date = models.DateField(timezone.now)
    quantity = models.PositiveSmallIntegerField()
    unit_amount = models.IntegerField()
    type = models.IntegerField(choices=TypeChoices, default=StrategyAdjustmentType.TradingFee.value)
    note = models.TextField(null=True, blank=True)