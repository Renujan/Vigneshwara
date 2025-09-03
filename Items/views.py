

from rest_framework import views
from rest_framework.response import Response
from .models import Item,Brand,Stock
from .serializers import ItemSerializer,BrandSerializer,StockSerializer
from rest_framework import generics

class ItemListView(views.APIView):
    def get(self, request):
        items = Item.objects.all()
        serializer = ItemSerializer(items, many=True)
        return Response(serializer.data)
    
from rest_framework import generics
from .models import Category
from .serializers import CategorySerializer

class CategoryListView(generics.ListAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    
class BrandListView(views.APIView):
    def get(self, request):
        brands = Brand.objects.all()
        serializer = BrandSerializer(brands, many=True)
        return Response(serializer.data)
    
######################################################
class StockListView(generics.ListCreateAPIView):
    queryset = Stock.objects.all()
    serializer_class = StockSerializer

class StockDetailView(generics.RetrieveUpdateAPIView):
    queryset = Stock.objects.all()
    serializer_class = StockSerializer
