from django.contrib import admin
from .models import Review, Category, ConfirmCode, Product, Tag

# Register your models here.
admin.site.register(Category)
admin.site.register(Product)
admin.site.register(Tag)
admin.site.register(Review)
admin.site.register(ConfirmCode)

