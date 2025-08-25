# from wagtail.snippets.models import register_snippet
# from wagtail.snippets.views.snippets import SnippetViewSet
# from wagtail.admin.panels import FieldPanel,InlinePanel
# from .models import Order


# class OrderViewSet(SnippetViewSet):
#     model = Order
#     icon = "help"
#     inspect_view_enabled = True
#     add_to_admin_menu = True
#     list_display = ( "full_name","email","created_at","status")
#     list_export = ("full_name","email","created_at")
    
#     list_filter = ("email", "full_name")
#     search_fields = ( "full_name", "email")
#     panels = [
#         FieldPanel('full_name'),
#         FieldPanel('address'),
#         FieldPanel('town'),
#         FieldPanel('phone'),
#         FieldPanel('email'),
#         FieldPanel('total_amount'),
#         FieldPanel('status'),
#         InlinePanel("order_item_details", label="Order Items"),
#     ]


# register_snippet(OrderViewSet)
