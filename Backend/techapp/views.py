# views.py
from rest_framework.views import APIView
from rest_framework.response import Response
from prometheus_client import Gauge, generate_latest, CONTENT_TYPE_LATEST
from .models import DailyStockData
from .serializers import DailyStockDataSerializer
from django.db.models import F, ExpressionWrapper, FloatField, Subquery, OuterRef
from django.db.models.functions import Coalesce
from django.db.models.functions import Cast
from datetime import timedelta
from django.utils import timezone
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.shortcuts import render
from django.views import View
from django.http import HttpResponse
import threading
import time

STOCK_PRICE_CHANGE = {
    '24h': Gauge('stock_price_change_24h', 'Price change percentage over 24 hours', ['symbol']),
    '7d': Gauge('stock_price_change_7d', 'Price change percentage over 7 days', ['symbol']),
    '30d': Gauge('stock_price_change_30d', 'Price change percentage over 30 days', ['symbol']),
    '1y': Gauge('stock_price_change_1y', 'Price change percentage over 1 year', ['symbol']),
}

@method_decorator(login_required, name='dispatch')

class DashboardView(View):
    def get(self, request):
        return render(request, 'techapp/dashboard.html')

class DailyStockDataView(APIView):
    def get(self, request):
        symbol = request.query_params.get('symbol')
        if symbol:
            stock_data = DailyStockData.objects.filter(symbol=symbol).order_by('-date').first()
        else:
            stock_data = DailyStockData.objects.all().order_by('-date')[:20]  # Limit to latest 20 entries
        serializer = DailyStockDataSerializer(stock_data, many=not symbol)
        return Response(serializer.data)

class DailyClosingPriceView(APIView):
    def get(self, request):
        # Get the latest closing prices for 20 tickers
        latest_data = (
            DailyStockData.objects
            .order_by('-date')[:20]  # Get the latest 20 entries
            .values('symbol', 'date', 'close')  # Select only the fields needed
        )
        
        if not latest_data:
            return Response({"error": "No data found in the database"}, status=404)
        
        return Response(list(latest_data))


class PriceChangePercentageView(APIView):
    def get(self, request):
        # Get the latest date
        latest_date = DailyStockData.objects.order_by('-date').values('date').first()
        if not latest_date:
            return Response({"error": "No data found in the database"}, status=404)

        latest_date = latest_date['date']

        # Define periods
        periods = {
            '24h': timedelta(days=1),
            '7d': timedelta(days=7),
            '30d': timedelta(days=30),
            '1y': timedelta(days=365)
        }

        results = {}

        # Get the latest unique symbols
        latest_symbols = DailyStockData.objects.filter(date=latest_date).values_list('symbol', flat=True).distinct()[:20]

        for symbol in latest_symbols:
            symbol_results = {}
            for period_label, period_delta in periods.items():
                start_date = latest_date - period_delta

                # Get the latest and past data for the symbol
                latest_data = DailyStockData.objects.filter(symbol=symbol, date=latest_date).first()
                past_data = DailyStockData.objects.filter(symbol=symbol, date__lte=start_date).order_by('-date').first()

                if latest_data and past_data:
                    price_change = (latest_data.close - past_data.close) / past_data.close * 100
                    symbol_results[period_label] = round(price_change, 2)
                else:
                    symbol_results[period_label] = None

            if symbol_results:
                results[symbol] = symbol_results

        if not results:
            return Response({"error": "No price change data available"}, status=404)

        return Response(results)
class TopGainersLosersView(APIView):
    def get(self, request):
        latest_date = DailyStockData.objects.order_by('-date').values('date').first()
        if not latest_date:
            return Response({"error": "No data found in the database"}, status=404)
        
        latest_date = latest_date['date']
        yesterday = latest_date - timedelta(days=1)
        
        subquery = DailyStockData.objects.filter(
            symbol=OuterRef('symbol'),
            date=yesterday
        ).values('close')[:1]
        
        price_changes = DailyStockData.objects.filter(date=latest_date).annotate(
            yesterday_close=Coalesce(Subquery(subquery), F('close')),
            change_percentage=ExpressionWrapper(
                (F('close') - F('yesterday_close')) / F('yesterday_close') * 100,
                output_field=FloatField()
            )
        ).order_by('-change_percentage')
        
        top_gainers = list(price_changes.values('symbol', 'change_percentage')[:5])
        top_losers = list(price_changes.values('symbol', 'change_percentage').reverse()[:5])
        
        return Response({
            "top_gainers": top_gainers,
            "top_losers": top_losers
        })


def update_metrics():
    latest_date = DailyStockData.objects.order_by('-date').values('date').first()
    if not latest_date:
        return

    latest_date = latest_date['date']

    periods = {
        '24h': timedelta(days=1),
        '7d': timedelta(days=7),
        '30d': timedelta(days=30),
        '1y': timedelta(days=365)
    }

    latest_symbols = DailyStockData.objects.filter(date=latest_date).values_list('symbol', flat=True).distinct()[:20]

    for symbol in latest_symbols:
        for period_label, period_delta in periods.items():
            start_date = latest_date - period_delta

            latest_data = DailyStockData.objects.filter(symbol=symbol, date=latest_date).first()
            past_data = DailyStockData.objects.filter(symbol=symbol, date__lte=start_date).order_by('-date').first()

            # Ensure both latest_data.close and past_data.close are not None
            if latest_data and past_data and latest_data.close is not None and past_data.close is not None:
                price_change = (latest_data.close - past_data.close) / past_data.close * 100
                STOCK_PRICE_CHANGE[period_label].labels(symbol=symbol).set(price_change)
            else:
                STOCK_PRICE_CHANGE[period_label].labels(symbol=symbol).set(float('nan'))  # Handle missing data with NaN

def metrics_updater():
    while True:
        update_metrics()
        time.sleep(60)  # Update every 60 seconds

# Start the metrics updater thread when the module is imported
updater_thread = threading.Thread(target=metrics_updater, daemon=True)
updater_thread.start()

def metrics_view(request):
    return HttpResponse(generate_latest(), content_type=CONTENT_TYPE_LATEST)