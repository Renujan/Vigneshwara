# from django.db import models
# from wagtail.fields import RichTextField
# from Items.models import Items


# class Enquire(models.Model):
#     id = models.BigAutoField(primary_key=True)
#     items = models.ForeignKey(Items, on_delete=models.SET_NULL, null=True, blank=True, related_name="select_items")
#     name = models.TextField()
#     email = models.EmailField()
#     subject = models.TextField()
#     Message = models.TextField()
#     created_at = models.DateTimeField(auto_now_add=True,null=True,blank=True)
#     updated_at = models.DateTimeField(auto_now_add=True,null=True,blank=True)


#     def __str__(self):
#         return self.subject
