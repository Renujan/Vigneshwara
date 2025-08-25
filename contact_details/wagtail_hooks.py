from wagtail.snippets.models import register_snippet
from wagtail.snippets.views.snippets import SnippetViewSet
from wagtail.admin.panels import FieldPanel
from .models import Contact


class ContactViewSet(SnippetViewSet):
    model = Contact
    icon = "comment"
    inspect_view_enabled = True
    add_to_admin_menu = True
    list_display = ("name","Message")
    list_export = ("name","email","created_at")
    
    
    list_filter = ("email", "name")
    search_fields = ("name", "email")
    panels = [
        FieldPanel('name'),
        FieldPanel('email'),
        FieldPanel('phone_number'),
        FieldPanel('Message'),
    ]


register_snippet(ContactViewSet)
