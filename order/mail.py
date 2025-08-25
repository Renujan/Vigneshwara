# from mail.mailer import send_email
# from django.db import models
# from wagtail.fields import RichTextField
# from Items.models import Items
# from wagtail.admin.panels import FieldPanel


# def send_order_confirmation_email(order):
#     items = order.order_item_details.select_related("items").all()
    

#     # 🧾 Build the HTML rows for each product
#     product_rows = ""
#     for item in items:
#         item_price = item.items.price - (item.items.discount or 0)
#         total_price = item.count * item_price
#         product_rows += f"""
#             <tr>
#                 <td>{item.items.name}</td>
#                 <td>{item.count}</td>
#                 <td>₹{item_price:.2f}</td>
#                 <td>₹{total_price:.2f}</td>
#             </tr>
#         """

#     # 📧 Email Subject
#     subject = "🛒 Order Confirmation - JuristJewels"

#     # 📨 Email Content with styled HTML table
#     message = f"""
#     <html>
#     <head>
#         <style>
#             table {{
#                 border-collapse: collapse;
#                 width: 100%;
#                 margin-top: 20px;
#             }}
#             th, td {{
#                 border: 1px solid #ddd;
#                 padding: 8px;
#                 text-align: center;
#             }}
#             th {{
#                 background-color: #f2f2f2;
#                 font-weight: bold;
#             }}
#             h2 {{
#                 color: #4CAF50;
#             }}
#         </style>
#     </head>
#     <body>
#         <p>Dear <strong>{order.full_name}</strong>,</p>
#         <p>Thank you for your order! 🎉</p>

#         <h2>📋 Order Details</h2>
#         <ul>
#             <li><strong>Full Name:</strong> {order.full_name}</li>
#             <li><strong>Phone:</strong> {order.phone}</li>
#             <li><strong>Email:</strong> {order.email}</li>
#             <li><strong>Address:</strong> {order.address}, {order.town}</li>
#             <li><strong>Order Status:</strong> {order.status}</li>
#         </ul>

#         <h3 style="margin-top:20px;">🧾 Total Amount: <strong>₹{order.total_amount:.2f}</strong></h3>

#         <p>We will process your order shortly. 📦<br>
#         Thank you for shopping with <strong>JuristJewels</strong> 💎</p>

#         <p>Warm regards,<br>JuristJewels Team</p>
#     </body>
#     </html>
#     """

#     # ✅ Send Email
#     send_email(
#         subject=subject,
#         rich_text_content=message,
#         to=[order.email],
#         use_thread=True,
#     )



# def send_order_processing_email(order):
#     items = order.order_item_details.select_related("items").all()
    

#     # 🧾 Build the HTML rows for each product
#     product_rows = ""
#     for item in items:
#         item_price = item.items.price - (item.items.discount or 0)
#         total_price = item.count * item_price
#         product_rows += f"""
#             <tr>
#                 <td>{item.items.name}</td>
#                 <td>{item.count}</td>
#                 <td>₹{item_price:.2f}</td>
#                 <td>₹{total_price:.2f}</td>
#             </tr>
#         """

#     # 📧 Email Subject
#     subject = "🛒 order status has been changed- Vishthavaa-Jewellery"

#     # 📨 Email Content with styled HTML table
#     message = f"""
#     <html>
#     <head>
#         <style>
#             table {{
#                 border-collapse: collapse;
#                 width: 100%;
#                 margin-top: 20px;
#             }}
#             th, td {{
#                 border: 1px solid #ddd;
#                 padding: 8px;
#                 text-align: center;
#             }}
#             th {{
#                 background-color: #f2f2f2;
#                 font-weight: bold;
#             }}
#             h2 {{
#                 color: #4CAF50;
#             }}
#         </style>
#     </head>
#     <body>
#         <p>Dear <strong>{order.full_name}</strong>,</p>
#         <p>Thank you for your order! 🎉</p>

#         <h2>📋 Order Details</h2>
#         <ul>
#             <li><strong>Full Name:</strong> {order.full_name}</li>
#             <li><strong>Phone:</strong> {order.phone}</li>
#             <li><strong>Email:</strong> {order.email}</li>
#             <li><strong>Address:</strong> {order.address}, {order.town}</li>
#             <li><strong>Order Status:</strong> {order.status}</li>
#         </ul>

#         <h3 style="margin-top:20px;">🧾 Total Amount: <strong>₹{order.total_amount:.2f}</strong></h3>

#         <p>We will process your order shortly. 📦<br>
#         Thank you for shopping with <strong>JuristJewels</strong> 💎</p>

#         <p>Warm regards,<br>JuristJewels Team</p>
#     </body>
#     </html>
#     """

#     # ✅ Send Email
#     send_email(
#         subject=subject,
#         rich_text_content=message,
#         to=[order.email],
#         use_thread=True,
#     )
