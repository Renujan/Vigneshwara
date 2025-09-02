from wagtail.snippets.views.snippets import SnippetViewSet
from wagtail.snippets.models import register_snippet
from wagtail import hooks
from wagtail.snippets.widgets import SnippetListingButton
from django.urls import reverse, path
from .models import Bill
from . import views
import logging

logger = logging.getLogger(__name__)

class BillViewSet(SnippetViewSet):
    model = Bill
    icon = "doc-full-inverse"
    inspect_view_enabled = True
    add_to_admin_menu = True
    menu_label = "Bills"
    menu_order = 300

    list_display = ("id", "customer_name", "total_amount", "final_amount")
    list_export = ("id", "customer_name", "total_amount", "discount", "final_amount")
    list_filter = ("created_at",)
    search_fields = ("customer_name",)

    def get_urlpatterns(self):
        patterns = super().get_urlpatterns()
        # Add custom URL for PDF download
        custom_patterns = [
            path('download-pdf/<int:pk>/', views.download_bill_pdf, name='download_bill_pdf'),
        ]
        return patterns + custom_patterns

@hooks.register('register_snippet_listing_buttons')
def add_download_bill_button(snippet, user, next_url=None):
    if isinstance(snippet, Bill):
        try:
            # Use the correct URL pattern name - Wagtail uses app_label_model format
            url = reverse('billing_bill:download_bill_pdf', kwargs={'pk': snippet.pk})
        except Exception as e:
            logger.error(f"Reverse error: {str(e)}")
            # Fallback URL using the standard Wagtail admin pattern
            url = f"/admin/snippets/billing/bill/download-pdf/{snippet.pk}/"
        return [
            SnippetListingButton(
                label='Download Bill',
                url=url,
                priority=90,
                icon_name='download',
            )
        ]
    return []

register_snippet(BillViewSet)