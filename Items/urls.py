from django.urls import path
from .views import *

urlpatterns = [
    path('items/', ItemListView.as_view(), name='item-list'),#show all items from db
    path('items/<int:pk>/', ItemDetailView.as_view(), name='item-detail'),
    path('brands/', BrandListView.as_view(), name='brand-list'),#show all brands
    path('stocks/', StockListView.as_view(), name='stock-list'),#`show all stocks
    path('stocks/<int:pk>/', StockDetailView.as_view(), name='stock-detail'),#show, update stock by id
    path('categories/', CategoryListView.as_view(), name='category-list'),#show all categories
]