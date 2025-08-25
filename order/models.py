# from django.db import models
# from wagtail.fields import RichTextField
# from Items.models import Items
# from wagtail.admin.panels import FieldPanel
# from wagtail.search import index

# from modelcluster.fields import ParentalKey
# from modelcluster.models import ClusterableModel
# from .mail import send_order_confirmation_email,send_order_processing_email


# class OrderItemDetails(models.Model):
    
    
#     invoice = ParentalKey(
#         'Order',
#         on_delete=models.CASCADE,
#         related_name='order_item_details'
#     )
#     items = models.ForeignKey(Items, on_delete=models.SET_NULL, null=True, blank=True, related_name="select_items_orders")
#     count = models.PositiveIntegerField()
    
    
    
#     panels = [
#         FieldPanel("items"),
#         FieldPanel("count"),
#     ]
#     def __str__(self):
#         return self.count

# class Order(index.Indexed, ClusterableModel):
#     STATUS_CHOICES = (
#         ('order_placed', 'order_placed'),
#         ('processing', 'processing'),
#         ('completed', 'completed'),
#     )
#     id = models.BigAutoField(primary_key=True)
    
#     full_name = models.TextField()
#     address = models.TextField()
#     town = models.TextField()
#     phone = models.TextField()
#     email = models.EmailField()
#     total_amount = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
#     status = models.CharField(choices=STATUS_CHOICES, default='order_placed')
#     created_at = models.DateTimeField(auto_now_add=True,null=True,blank=True)
#     updated_at = models.DateTimeField(auto_now_add=True,null=True,blank=True)
    


#     def save(self, *args, **kwargs):
#         is_new = self.pk is None  # Check if it's a new order
        
#         old_status = Order.objects.filter(pk=self.pk).first().status if not is_new else None
#         if not is_new:
#             if self.status != old_status:
#                 send_order_processing_email(self)
#                 print("hiii")
                
#         else :
#             send_order_confirmation_email(self)
#             print("pavi")
#         super().save(*args, **kwargs)