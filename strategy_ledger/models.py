from enum import Enum

from django.contrib.postgres.fields import jsonb
from django.utils import timezone
from django.db import models


class SecurityPosition(models.Model):
    ticker = models.CharField(max_length=5)
    purchase_date = models.DateField()
    purchase_price = models.PositiveIntegerField
    exit_price = models.PositiveIntegerField
    shares = models.IntegerField()


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
    settings = jsonb.JSONField()
    frequency = models.IntegerField(choices=FrequencyChoices, default=AlertFrequencyType.OnDemand.value)
    note = models.TextField()


class Strategy(models.Model):
    date = models.DateField()
    alerts = models.ManyToManyField(StrategyAlert)


class OptionPosition(models.Model):
    PositionChoices = (
        (OptionPositionType.Call.value, 'Call'),
        (OptionPositionType.Put.value, 'Put')
    )

    strategy = models.ForeignKey(Strategy)
    option_symbol = models.CharField(max_length=20)
    strike = models.PositiveIntegerField()
    expiry_date = models.DateField()
    entry_date = models.DateField(default=timezone.now)
    entry_price = models.PositiveIntegerField()
    exit_price = models.IntegerField()
    exit_date = models.DateField()
    contracts = models.IntegerField()
    position_type = models.IntegerField(choices=PositionChoices, default=OptionPositionType.Call.value)
    rolled_to = models.ForeignKey('OptionPosition', related_name='rolled_from')
    note = models.TextField()


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
    date = models.DateField()
    quantity = models.PositiveSmallIntegerField()
    unit_amount = models.IntegerField()
    type = models.IntegerField(choices=TypeChoices, default=StrategyAdjustmentType.TradingFee.value)
    note = models.TextField()