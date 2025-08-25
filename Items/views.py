

from rest_framework import views
from rest_framework.response import Response
from .models import Item
from .serializers import ItemSerializer

class ItemListView(views.APIView):
    def get(self, request):
        items = Item.objects.all()
        serializer = ItemSerializer(items, many=True)
        return Response(serializer.data)
    
from rest_framework import views
from rest_framework.response import Response
from .models import Brand
from .serializers import BrandSerializer

class BrandListView(views.APIView):
    def get(self, request):
        brands = Brand.objects.all()
        serializer = BrandSerializer(brands, many=True)
        return Response(serializer.data)