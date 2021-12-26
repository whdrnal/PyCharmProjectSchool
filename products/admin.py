
from django.contrib import admin
from .models import Product


class ProductAdmin(admin.ModelAdmin):
    search_fields = ['subject']


admin.site.register(Product, ProductAdmin)