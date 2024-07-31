# techapp/views.py
from datetime import timedelta
from django.utils import timezone
from rest_framework import generics
from rest_framework.response import Response
from .models import DailyStockData
from .serializers import DailyStockDataSerializer
from django.db.models import Max, Min, F, FloatField, ExpressionWrapper

class StockKPIsView(generics.GenericAPIView):
    def get(self, request, *args, **kwargs):
        today = timezone.now().date()
        one_day_ago = today - timedelta(days=1)
        thirty_days_ago = today - timedelta(days=30)
        one_year_ago = today - timedelta(days=365)

        stocks = DailyStockData.objects.values('symbol').distinct()

        result = []

        for stock in stocks:
            symbol = stock['symbol']
            data = DailyStockData.objects.filter(symbol=symbol)
            
            # Daily Closing Price
            last_entry = data.order_by('-date').first()
            daily_closing_price = last_entry.close if last_entry else None

            # Price Change Percentage
            price_change_percentage_24h = self.calculate_price_change_percentage(symbol, one_day_ago, today)
            price_change_percentage_30d = self.calculate_price_change_percentage(symbol, thirty_days_ago, today)
            price_change_percentage_1y = self.calculate_price_change_percentage(symbol, one_year_ago, today)

            # Top Gainers/Losers
            top_gainers_losers = self.calculate_top_gainers_losers(symbol, one_day_ago, today)

            result.append({
                'symbol': symbol,
                'daily_closing_price': daily_closing_price,
                'price_change_percentage_24h': price_change_percentage_24h,
                'price_change_percentage_30d': price_change_percentage_30d,
                'price_change_percentage_1y': price_change_percentage_1y,
                'top_gainers_losers': top_gainers_losers
            })

        return Response(result)

    def calculate_price_change_percentage(self, symbol, start_date, end_date):
        try:
            start_price = DailyStockData.objects.filter(symbol=symbol, date=start_date).values('close').first()['close']
            end_price = DailyStockData.objects.filter(symbol=symbol, date=end_date).values('close').first()['close']
            percentage_change = ((end_price - start_price) / start_price) * 100
            return percentage_change
        except TypeError:
            return None

    def calculate_top_gainers_losers(self, symbol, start_date, end_date):
        data = DailyStockData.objects.filter(symbol=symbol, date__range=(start_date, end_date))
        gainers_losers = data.order_by('-close')[:10]  # Example: Get top 10
        return [
            {
                'date': entry.date,
                'close': entry.close
            }
            for entry in gainers_losers
        ]
