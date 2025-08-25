# import wagtail
# from rest_framework import serializers  
# from .models import Items, ItemExtraImages

# # Serializer for ItemExtraImages
# class ItemExtraImagesSerializer(serializers.ModelSerializer):
#     photo = serializers.SerializerMethodField()

#     def get_photo(self, obj):
#         if obj.photo:
#             # Use a specific rendition (e.g., max-800x600)
#             rendition = obj.photo.get_rendition('max-800x600')
#             return rendition.url if rendition else None
#         return None

#     class Meta:
#         model = ItemExtraImages
#         fields = ['id', 'photo']

# # Serializer for Items
# class ItemsSerializer(serializers.ModelSerializer):
#     item_extra_images = ItemExtraImagesSerializer(many=True, read_only=True)
#     photo = serializers.SerializerMethodField()
#     discounted_price = serializers.SerializerMethodField()

#     def get_photo(self, obj):
#         if obj.photo:
#             rendition = obj.photo.get_rendition('max-800x600')
#             return rendition.url if rendition else None
#         return None

#     def get_discounted_price(self, obj):
#         if obj.discount and obj.price:
#             discount_percentage = obj.discount / 100
#             return obj.price - (obj.price * discount_percentage)
#         return obj.price

#     class Meta:
#         model = Items
#         fields = [
#             'id',
#             'name',
#             'price',
#             'discount',
#             'color',
#             'category',
#             'status',
#             'description',
#             'addional_info',
#             'photo',
#             'item_extra_images',
#             'created_at',
#             'updated_at',
#             'discounted_price'
#         ]