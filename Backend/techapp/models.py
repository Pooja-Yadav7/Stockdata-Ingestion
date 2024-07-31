# techapp/models.py
from django.db import models

class DailyStockData(models.Model):
    symbol = models.CharField(max_length=10)
    date = models.DateField()
    high = models.FloatField()
    low = models.FloatField()
    open = models.FloatField()
    close = models.FloatField()
    volume = models.BigIntegerField()

    class Meta:
        unique_together = ('symbol', 'date')
