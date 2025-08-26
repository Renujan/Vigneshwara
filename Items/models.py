from django.db import models
from wagtail.fields import RichTextField
from wagtail.admin.panels import FieldPanel
from wagtail.search import index
from modelcluster.fields import ParentalKey
from modelcluster.models import ClusterableModel
from wagtail.images.models import Image



class Category(models.Model):
    id = models.BigAutoField(primary_key=True)
    name = models.CharField(max_length=200)
    description = models.TextField(null=True, blank=True)
    

    def __str__(self):
        return self.name

class Brand(index.Indexed, ClusterableModel):
    id = models.BigAutoField(primary_key=True)
    name = models.TextField()
    description = models.TextField()  # fixed typo: discription -> description
    rating = models.PositiveIntegerField()
    photo = models.ForeignKey(
        Image,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+'
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    panels = [
        FieldPanel("name"),
        FieldPanel("description"),
        FieldPanel("rating"),
        FieldPanel("photo"),
    ]

    def __str__(self):
        return self.name
    

class BrandExtraImages(models.Model):
    brand = ParentalKey(
        'Brand',
        on_delete=models.CASCADE,
        related_name='brand_extra_images'
    )
    photo = models.ForeignKey(
        Image,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+'
    )
    panels = [
        FieldPanel("photo"),
    ]

    def __str__(self):
        return f"Extra Image for {self.brand.name}"
    

class Item(index.Indexed, ClusterableModel):
    name = models.CharField(max_length=200)
    brand = models.ForeignKey(
        Brand,
        on_delete=models.CASCADE,
        related_name="items"
    )
    category = models.ForeignKey(
        Category,
        on_delete=models.CASCADE,
        related_name="items"
    )
    description = models.TextField()
    features = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    discount_percentage = models.PositiveIntegerField(null=True, blank=True)
    is_new = models.BooleanField(default=False)
    in_stock = models.BooleanField(default=True)
    image = models.ImageField(upload_to="items/", null=True, blank=True)

    def __str__(self):
        return self.name


class ItemExtraImage(models.Model):
    item = ParentalKey(
        'Item',
        on_delete=models.CASCADE,
        related_name='item_extra_images'
    )
    image = models.ForeignKey(
        Image,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+'
    )
    panels = [
        FieldPanel("image"),  # ✅ must match the field name
    ]

    def __str__(self):
        return f"Extra Image for {self.item.name}"


class Stock(models.Model):
    item = models.OneToOneField(
        Item,
        on_delete=models.CASCADE,
        related_name="stock"
    )
    quantity = models.PositiveIntegerField(default=0)
    reorder_level = models.PositiveIntegerField(default=10)  # alert if below
    last_updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.item.name} - {self.quantity} in stock"

    def add_stock(self, qty):
        self.quantity += qty
        self.save()

    def reduce_stock(self, qty):
        if qty > self.quantity:
            raise ValueError("Not enough stock available")
        self.quantity -= qty
        self.save()

    @property
    def needs_reorder(self):
        return self.quantity <= self.reorder_level



