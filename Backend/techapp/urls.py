# techapp/urls.py
from django.urls import path
from .views import StockKPIsView

urlpatterns = [
    path('stock-kpis/', StockKPIsView.as_view(), name='stock-kpis'),
]
