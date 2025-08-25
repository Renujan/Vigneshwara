# from rest_framework import serializers
# from rest_framework.views import APIView
# from rest_framework.response import Response
# from rest_framework import status
# from .models import Enquire, Items

# class EnquireSerializer(serializers.ModelSerializer):
#     items = serializers.PrimaryKeyRelatedField(queryset=Items.objects.all(), required=False, allow_null=True)

#     class Meta:
#         model = Enquire
#         fields = ['id', 'items', 'name', 'email', 'subject', 'Message', 'created_at', 'updated_at']
#         read_only_fields = ['id', 'created_at', 'updated_at']

#     def validate(self, data):
#         # Ensure required fields are not empty
#         required_fields = ['name', 'email', 'subject', 'Message']
#         for field in required_fields:
#             if not data.get(field):
#                 raise serializers.ValidationError({field: f"{field.capitalize()} is required."})
#         return data

# class EnquireCreateView(APIView):
#     def post(self, request, *args, **kwargs):
#         serializer = EnquireSerializer(data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data, status=status.HTTP_201_CREATED)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)