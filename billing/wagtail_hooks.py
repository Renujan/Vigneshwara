# billing/wagtail_hooks.py
from wagtail.snippets.views.snippets import SnippetViewSet
from wagtail.snippets.models import register_snippet
from .models import Bill


class BillViewSet(SnippetViewSet):
    model = Bill
    icon = "doc-full-inverse"
    inspect_view_enabled = True
    add_to_admin_menu = True

    list_display = ("id", "customer_name", "total_amount", "final_amount")
    list_export = ("id", "customer_name", "total_amount", "discount", "final_amount")
    list_filter = ("created_at",)
    search_fields = ("customer_name",)

register_snippet(BillViewSet)