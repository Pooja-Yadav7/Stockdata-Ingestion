# techapp/admin.py
from django.contrib import admin
from .models import DailyStockData

class DailyStockDataAdmin(admin.ModelAdmin):
    list_display = (
        'symbol',
        'date',
        'high',
        'low',
        'open',
        'close',
        'volume',
    )

admin.site.register(DailyStockData, DailyStockDataAdmin)
