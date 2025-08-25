from django.db import models

from django.db import models
from django.utils.timezone import now
from wagtail.admin.panels import FieldPanel
from wagtail.fields import RichTextField
from wagtail.snippets.models import register_snippet
from wagtail.snippets.views.snippets import SnippetViewSet
from datetime import timedelta
from django.core.exceptions import ValidationError
import re
from django.conf import settings
from .mailer import send_email

class EmailSender(models.Model):
    id = models.BigAutoField(primary_key=True)
    subject = models.CharField(
        max_length=255,
        help_text="Emails auto-delete after 40 days."
    )
    message = RichTextField()
    created_at = models.DateTimeField(auto_now_add=True)
    send_email_now = models.BooleanField(
        default=False,
        help_text="Check this box to send the email immediately upon saving"
    )
    to_recipients = models.TextField(
        help_text="Enter 'To' email addresses separated by commas (e.g., email1@example.com, email2@example.com)",
        blank=True
    )
    cc_recipients = models.TextField(
        help_text="Enter 'CC' email addresses separated by commas (e.g., email3@example.com, email4@example.com)",
        blank=True
    )
    bcc_recipients = models.TextField(
        help_text="Enter 'BCC' email addresses separated by commas (e.g., email5@example.com, email6@example.com)",
        blank=True
    )

    

    def clean(self):
        """Validate email addresses format for to, cc, and bcc fields"""
        if self.send_email_now:
            if not settings.ENABLE_EMAIL:
                raise ValidationError({
                    "send_email_now": "Mailer is disabled, enable it in settings"
                })
            if not self.to_recipients:
                raise ValidationError({
                    "to_recipients": "At least one 'To' recipient is required when sending an email"
                })

        # Validate email formats for all recipient fields
        email_pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        recipient_fields = [
            (self.to_recipients, "to_recipients"),
            (self.cc_recipients, "cc_recipients"),
            (self.bcc_recipients, "bcc_recipients")
        ]

        for field_value, field_name in recipient_fields:
            if field_value:
                email_list = [email.strip() for email in field_value.split(',') if email.strip()]
                for email in email_list:
                    if not re.match(email_pattern, email):
                        raise ValidationError({
                            field_name: f"Invalid email address format: {email}"
                        })

    def save(self, *args, **kwargs):
        # Delete emails older than 40 days
        EmailSender.objects.filter(created_at__lte=now() - timedelta(days=40)).delete()

        # Only send email if send_email_now is True
        if self.send_email_now:
            self.send_email_now = False  # Reset to prevent re-sending

            # Prepare recipient lists
            to_list = (
                [email.strip() for email in self.to_recipients.split(',') if email.strip()]
                if self.to_recipients else []
            )
            cc_list = (
                [email.strip() for email in self.cc_recipients.split(',') if email.strip()]
                if self.cc_recipients else []
            )
            bcc_list = (
                [email.strip() for email in self.bcc_recipients.split(',') if email.strip()]
                if self.bcc_recipients else []
            )

            # Send email with to, cc, and bcc
            send_email(
                subject=self.subject,
                rich_text_content=self.message,
                use_thread=True,
                to=to_list,
                cc=cc_list,
                bcc=bcc_list
            )

        super().save(*args, **kwargs)

    def __str__(self):
        return self.subject

    class Meta:
        verbose_name = "Mailer"
        verbose_name_plural = "Mailer"




