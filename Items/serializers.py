from rest_framework import serializers
from .models import Item, ItemExtraImage

class ItemExtraImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ItemExtraImage
        fields = ['id', 'image']

class ItemSerializer(serializers.ModelSerializer):
    brand = serializers.CharField(source='brand.name')
    category = serializers.CharField(source='category.name')
    item_extra_images = ItemExtraImageSerializer(many=True, read_only=True)

    class Meta:
        model = Item
        fields = [
            'id',
            'name',
            'brand',
            'category',
            'description',
            'features',
            'price',
            'discount_percentage',
            'is_new',
            'in_stock',
            'image',
            'item_extra_images'
        ]

from rest_framework import serializers
from .models import Brand, BrandExtraImages

class BrandExtraImagesSerializer(serializers.ModelSerializer):
    class Meta:
        model = BrandExtraImages
        fields = ['id', 'photo']

class BrandSerializer(serializers.ModelSerializer):
    brand_extra_images = BrandExtraImagesSerializer(many=True, read_only=True)

    class Meta:
        model = Brand
        fields = [
            'id',
            'name',
            'description',
            'rating',
            'photo',
            'brand_extra_images'
        ]