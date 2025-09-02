# billing/models.py
from django.db import models
from modelcluster.fields import ParentalKey
from modelcluster.models import ClusterableModel
from wagtail.admin.panels import FieldPanel, InlinePanel
from wagtail.snippets.models import register_snippet
from wagtail.snippets.views.snippets import SnippetViewSet
from Items.models import Item   # ✅ import from your Items app


# billing/models.py
from django.db import models
from modelcluster.fields import ParentalKey
from modelcluster.models import ClusterableModel
from wagtail.admin.panels import FieldPanel, InlinePanel
from Items.models import Item



# billing/models.py
from django.db import models
from modelcluster.fields import ParentalKey
from modelcluster.models import ClusterableModel
from wagtail.admin.panels import FieldPanel, InlinePanel
from Items.models import Item
from django.core.exceptions import ValidationError

class Bill(ClusterableModel):
    """
    A Bill can contain many items.
    """
    customer_name = models.CharField(max_length=200, blank=True, null=True)
    contact_number = models.CharField(max_length=20, blank=True, null=True)  # 📞
    address = models.TextField(blank=True, null=True)  # 🏠
    created_at = models.DateTimeField(auto_now_add=True)

    total_amount = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        default=0.00,
        editable=False
    )
    discount = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0.00,
        help_text="Discount amount admin can enter"
    )
    final_amount = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        default=0.00,
        editable=False,
        help_text="Total after discount"
    )

    panels = [
        FieldPanel("customer_name"),
        FieldPanel("contact_number"),
        FieldPanel("address"),
        InlinePanel("bill_items", label="Bill Items"),
        FieldPanel("total_amount", read_only=True),
        FieldPanel("discount"),
        FieldPanel("final_amount", read_only=True),
    ]

    def __str__(self):
        return f"Bill #{self.id} - {self.customer_name or 'No Name'}"

    def calculate_total(self):
        """Sum of all BillItems subtotal"""
        return sum([item.subtotal for item in self.bill_items.all()])

    def calculate_final(self):
        """Final amount after discount"""
        return max(self.total_amount - self.discount, 0)  # ❌ prevent negative

    def save(self, *args, **kwargs):
        # ✅ Update total_amount first
        self.total_amount = self.calculate_total()
        # ✅ Update final_amount after discount
        self.final_amount = self.calculate_final()
        super().save(*args, **kwargs)

from django.core.exceptions import ValidationError
from django.core.exceptions import ValidationError
from django.core.exceptions import ValidationError
from modelcluster.fields import ParentalKey
from django.db import models
from wagtail.admin.panels import FieldPanel
from Items.models import Item

class BillItem(models.Model):
    bill = ParentalKey("Bill", on_delete=models.CASCADE, related_name="bill_items")
    item = models.ForeignKey(Item, on_delete=models.CASCADE, related_name="+")
    quantity = models.PositiveIntegerField(default=1)

    panels = [
        FieldPanel("item"),
        FieldPanel("quantity"),
    ]

    def __str__(self):
        return f"{self.item.name} × {self.quantity}"

    @property
    def subtotal(self):
        return self.item.price * self.quantity

    # ✅ Validation (runs in Wagtail admin before saving)
    def clean(self):
        if hasattr(self.item, "stock") and self.quantity > self.item.stock.quantity:
            raise ValidationError({
                "quantity": f"❌ Not enough stock for {self.item.name}. "
                            f"Available: {self.item.stock.quantity}"
            })

    def save(self, *args, **kwargs):
        is_new = self._state.adding
        super().save(*args, **kwargs)

        # ✅ Reduce stock only when creating a new BillItem
        if is_new and hasattr(self.item, "stock"):
            self.item.stock.reduce_stock(self.quantity)

        # ✅ Update Bill totals
        self.bill.total_amount = self.bill.calculate_total()

        # ✅ Calculate final_amount after discount (discount is editable in Bill)
        if hasattr(self.bill, "discount"):
            self.bill.final_amount = max(self.bill.total_amount - self.bill.discount, 0)
        else:
            self.bill.final_amount = self.bill.total_amount

        # Save the Bill fields
        self.bill.save(update_fields=["total_amount", "final_amount"])
