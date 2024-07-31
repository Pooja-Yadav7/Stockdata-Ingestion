# techapp/serializers.py
from rest_framework import serializers
from .models import DailyStockData

class DailyStockDataSerializer(serializers.ModelSerializer):
    class Meta:
        model = DailyStockData
        fields = '__all__'
