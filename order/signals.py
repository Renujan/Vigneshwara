# from django.db.models.signals import post_save
# from django.dispatch import receiver
# from .models import Order,OrderItemDetails
# from .mail import send_order_confirmation_email

# @receiver(post_save, sender=Order)
# def send_order_email_after_save(sender, instance, created, **kwargs):
#     if created:
#         # ✅ Delay email sending after related OrderItemDetails are saved
#         from threading import Timer

#         def send_later():
#             send_order_confirmation_email(instance)

#         # 🕒 Delay for 1 second to wait for OrderItemDetails to be created
#         Timer(1.0, send_later).start()
