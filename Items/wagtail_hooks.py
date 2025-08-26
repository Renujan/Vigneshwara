from wagtail.snippets.models import register_snippet
from wagtail.snippets.views.snippets import SnippetViewSet
from wagtail.admin.panels import FieldPanel,InlinePanel
from .models import Brand,Item,Category,Stock
from django.contrib import messages
from django.db import models


# class ItemsViewSet(SnippetViewSet):
#     model = Items
#     icon = "help"
#     inspect_view_enabled = True
#     add_to_admin_menu = True
#     list_display = ("name","status")
#     list_export = ("name","price","color","status","description","created_at")
    
#     list_filter = ("name", "color","status","created_at")
#     search_fields = ("name")
#     panels = [
#         FieldPanel('name'),
#         FieldPanel('price'),
#         FieldPanel('discount'),
#         FieldPanel('color'),
#         FieldPanel('category'),
#         FieldPanel('addional_info'),
#         FieldPanel('status'),
#         FieldPanel('description'),
#         FieldPanel('photo'),
#         InlinePanel("item_extra_images", label="Extra Photos"),
#     ]


# register_snippet(ItemsViewSet)

class BrandViewSet(SnippetViewSet):
    model = Brand
    icon = "help"
    inspect_view_enabled = True
    add_to_admin_menu = True
    list_display = ("name","description","rating")
    list_export = ("name", "description", "rating", "photo")
    
    list_filter = ("rating", "name", "description")
    search_fields = ("name")
    panels = [
        FieldPanel('name'),
        FieldPanel('description'),
        FieldPanel('rating'),
        FieldPanel('photo'),
        InlinePanel("brand_extra_images", label="Extra Photos"),
    ]


register_snippet(BrandViewSet)

class ItemViewSet(SnippetViewSet):
    model = Item
    icon = "help"
    inspect_view_enabled = True
    add_to_admin_menu = True
    list_display = ("name","brand","price","in_stock")
    list_export = ("name","brand","price","in_stock")
    
    list_filter = ("name","brand","price","in_stock")
    search_fields = ("name","brand","price","in_stock")
    panels = [
        FieldPanel('name'),
        FieldPanel('brand'),
        FieldPanel('category'),
        FieldPanel('description'),
        FieldPanel('features'),
        FieldPanel('price'),
        FieldPanel('discount_percentage'),
        FieldPanel('is_new'),
        FieldPanel('in_stock'),
        FieldPanel('image'),
        InlinePanel("item_extra_images", label="Extra Photos"),
    ]


register_snippet(ItemViewSet)


class CategoryViewSet(SnippetViewSet):
    model = Category
    icon = "help"
    inspect_view_enabled = True
    add_to_admin_menu = True
    list_display = ("name","description")
    list_export = ("name","description")
    
    list_filter = ("name",)
    search_fields = ("name",)
    panels = [
        FieldPanel('name'),
        FieldPanel('description'),
    ]


register_snippet(CategoryViewSet)



class StockViewSet(SnippetViewSet):
    model = Stock
    icon = "folder-open-inverse"
    inspect_view_enabled = True
    add_to_admin_menu = True
    list_display = ("item", "quantity", "reorder_level", "last_updated")
    list_export = ("item", "quantity", "reorder_level", "last_updated")
    list_filter = ("item",)
    search_fields = ("item__name",)

    panels = [
        FieldPanel("item"),
        FieldPanel("quantity"),
        FieldPanel("reorder_level"),
    ]

register_snippet(StockViewSet)


# ✅ WARNINGS ON DASHBOARD@hooks.register("construct_main_menu")
def check_low_stock(request, menu_items):
    if request.user.is_superuser or request.user.is_staff:
        low_stock_items = Stock.objects.filter(quantity__lte=models.F("reorder_level"))
        if low_stock_items.exists():
            item_names = ", ".join([s.item.name for s in low_stock_items])
            messages.warning(
                request,
                f"⚠️ Low stock alert! Please reorder: {item_names}"
            )
