from rest_framework import serializers
from .models import Item, ItemExtraImage, Stock, Brand, BrandExtraImages

class ItemExtraImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ItemExtraImage
        fields = ['id', 'image']

class StockSerializer(serializers.ModelSerializer):
    item_name = serializers.CharField(source="item.name", read_only=True)

    class Meta:
        model = Stock
        fields = ["id", "item", "item_name", "quantity", "reorder_level", "last_updated", "needs_reorder"]

class ItemSerializer(serializers.ModelSerializer):
    brand = serializers.CharField(source='brand.name')
    category = serializers.CharField(source='category.name')
    item_extra_images = ItemExtraImageSerializer(many=True, read_only=True)
    stock = StockSerializer(read_only=True)   # ✅ new field

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
            'item_extra_images',
            'stock'
        ]
# Serializer for BrandExtraImages
class BrandExtraImagesSerializer(serializers.ModelSerializer):
    photo = serializers.SerializerMethodField()

    class Meta:
        model = BrandExtraImages
        fields = ['id', 'photo']

    def get_photo(self, obj):
        if obj.photo:  # obj.photo is a Wagtail Image
            # Use obj.photo.file.url to get the actual image URL
            return obj.photo.file.url
        return None

# Serializer for Brand
class BrandSerializer(serializers.ModelSerializer):
    brand_extra_images = BrandExtraImagesSerializer(many=True, read_only=True)
    photo = serializers.SerializerMethodField()

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

    def get_photo(self, obj):
        if obj.photo:
            return obj.photo.file.url
        return None
