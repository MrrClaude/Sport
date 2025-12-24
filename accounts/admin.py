from django.contrib import admin
from .models import *
from django.utils.html import format_html

# Register your models here.
admin.site.site_header = "ACLEDA University of Business"
admin.site.site_title = "ACLEDA University of Business Admin Panel"
admin.site.index_title = "ACLEDA University of Business Admin Panel"

admin.site.register(Customer)
admin.site.register(Category)
admin.site.register(Product)
admin.site.register(ProductDetail)
admin.site.register(ProductDetailImage)
admin.site.register(Image)
admin.site.register(ImageType)
admin.site.register(HomeSlider)
admin.site.register(DealOfTheMonth)
admin.site.register(DealThumbnail)
admin.site.register(Book)
admin.site.register(Item)
admin.site.register(Size)
admin.site.register(PaymentMethods)
admin.site.register(BillingDetail)
admin.site.register(BlogPost)
