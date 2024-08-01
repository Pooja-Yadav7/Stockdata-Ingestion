# urls.py
from django.urls import path
from .views import DailyStockDataView, DailyClosingPriceView, PriceChangePercentageView, TopGainersLosersView

urlpatterns = [
    path('api/daily-stock-data/', DailyStockDataView.as_view(), name='daily_stock_data'),
    path('api/daily-closing-price/', DailyClosingPriceView.as_view(), name='daily_closing_price'),
    path('api/price-change-percentage/', PriceChangePercentageView.as_view(), name='price_change_percentage'),
    path('api/top-gainers-losers/', TopGainersLosersView.as_view(), name='top_gainers_losers'),
]