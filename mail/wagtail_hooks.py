from wagtail.snippets.models import register_snippet
from wagtail.snippets.views.snippets import SnippetViewSet
from wagtail.admin.panels import FieldPanel,InlinePanel
from .models import EmailSender


class MailViewSet(SnippetViewSet):
    model = EmailSender
    icon = 'mail'
    add_to_admin_menu = True
    list_display = ('subject', 'to_recipients', 'cc_recipients', 'bcc_recipients', 'created_at', 'send_email_now')
    inspect_view_enabled = True
    list_filter = ('created_at', 'send_email_now')
    search_fields = ('subject', 'to_recipients', 'cc_recipients', 'bcc_recipients')
    panels = [
        FieldPanel("subject"),
        FieldPanel("message"),
        FieldPanel("to_recipients"),
        FieldPanel("cc_recipients"),
        FieldPanel("bcc_recipients"),
        FieldPanel("send_email_now"),
    ]


register_snippet(MailViewSet)
