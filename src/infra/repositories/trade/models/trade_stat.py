from tortoise import fields, models
from datetime import datetime


class TradeStatModel(models.Model):
    symbol = fields.CharField(max_length=20, index=True, unique=True)
    min_price = fields.FloatField()
    max_price = fields.FloatField()
    avg_price = fields.FloatField()
    trades_count = fields.IntField(default=0)
    last_updated = fields.DatetimeField(default=datetime.now)
    stat_reset_time = fields.DatetimeField(auto_now_add=True)

    class Meta:
        table = "trade_stats"
