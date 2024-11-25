from django.contrib import admin
from django.utils.html import format_html
from django.urls import reverse
from .models import Product,Cart,Customer,OrderPlaced

# Register your models here.
@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display = ['id','user','name','locality','city','state','zipcode']


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['id','title','selling_price','discounted_price','brand','description','category','product_img']

@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    list_display = ['id','user','product','quantity']

@admin.register(OrderPlaced)
class OrderPlacedAdmin(admin.ModelAdmin):
    list_display = ['id','user','product','quantity','customer','ordered_date','status']

# def customer_info(self,obj):
#     link = reverse('admin:app_customer_change', args= [obj.customer.pk])
#     return format_html('<a href = "{}">{}</a>',link,obj.customer.name) 

# def product_info(self,obj):
#     link = reverse('admin:app_product_change', args= [obj.product.pk])
#     return format_html('<a href = "{}">{}</a>',link,obj.customer.name)

    

    



