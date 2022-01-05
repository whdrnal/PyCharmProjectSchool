from django.contrib import admin
from .models import Product, ProductReal


class ProductAdmin(admin.ModelAdmin):
    search_fields = ['subject']


admin.site.register(Product, ProductAdmin,)
admin.site.register(ProductReal),

