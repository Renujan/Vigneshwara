# from rest_framework import serializers
# from rest_framework.views import APIView
# from rest_framework.response import Response
# from rest_framework import status
# from .models import Order, OrderItemDetails, Items

# class OrderItemDetailsSerializer(serializers.ModelSerializer):
#     items = serializers.PrimaryKeyRelatedField(queryset=Items.objects.all(), required=True)

#     class Meta:
#         model = OrderItemDetails
#         fields = ['items', 'count']

#     def validate(self, data):
#         if data['count'] <= 0:
#             raise serializers.ValidationError({"count": "Quantity must be greater than zero."})
#         return data

# class OrderSerializer(serializers.ModelSerializer):
#     items = OrderItemDetailsSerializer(many=True, source='order_item_details')

#     class Meta:
#         model = Order
#         fields = ['id', 'full_name', 'address', 'town', 'phone', 'email', 'items', 'total_amount', 'created_at', 'updated_at']
#         read_only_fields = ['id', 'total_amount', 'created_at', 'updated_at']

#     def validate(self, data):
#         required_fields = ['full_name', 'address', 'town', 'phone', 'email']
#         for field in required_fields:
#             if not data.get(field):
#                 raise serializers.ValidationError({field: f"{field.replace('_', ' ').title()} is required."})
#         if not data.get('order_item_details'):
#             raise serializers.ValidationError({"items": "At least one item is required."})
#         return data
#     def create(self, validated_data):
#         items_data = validated_data.pop('order_item_details')

#         total_amount = 0
#         for item_data in items_data:
#             item = item_data['items']
#             count = item_data['count']

#             discount = item.discount or 0  # 🎯 percentage discount
#             item_price = item.price * (1 - (discount / 100))  # 🎉 apply % discount

#             total_amount += item_price * count

#         order = Order.objects.create(total_amount=total_amount, **validated_data)

#         for item_data in items_data:
#             OrderItemDetails.objects.create(invoice=order, **item_data)

#         return order

# class OrderCreateView(APIView):
#     def post(self, request, *args, **kwargs):
#         serializer = OrderSerializer(data=request.data)
#         if serializer.is_valid():
#             order = serializer.save()
#             return Response(serializer.data, status=status.HTTP_201_CREATED)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)