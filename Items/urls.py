from django.urls import path
from .views import *

urlpatterns = [
    path('items/', ItemListView.as_view(), name='item-list'),
    path('brands/', BrandListView.as_view(), name='brand-list'),
    path('stocks/', StockListView.as_view(), name='stock-list'),
    path('stocks/<int:pk>/', StockDetailView.as_view(), name='stock-detail'),
]