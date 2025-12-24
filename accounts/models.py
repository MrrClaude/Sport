from django.db import models
from ckeditor_uploader.fields import RichTextUploadingField
from django.utils import timezone
# Create your models here.
class Customer(models.Model):
    name = models.CharField(max_length=200, null=True)
    phone = models.CharField(max_length=200, null=True)
    email = models.CharField(max_length=200, null=True)
    date_created = models.DateTimeField(auto_now_add=True, null=True)
    def __str__(self):
        return self.name
    
class ImageType(models.Model): 
    ImageTypeName = models.CharField(max_length=200, null=True) 
    ImageTypeDate = models.DateTimeField(auto_now_add=True, null=True) 
    def str(self):          
        return f'{self.id}-{self.ImageTypeName}'

class Category(models.Model):
    categoryName = models.CharField(max_length=200, null=True)
    categoryImage = models.ImageField(upload_to='images/Categories/',null=True,blank=True)
    def __str__(self):         
        return f'{self.id} - {self.categoryName}'
    
class Image(models.Model): 
    ImageName = models.CharField(max_length=200, null=True) 
    ImageURL = models.ImageField(upload_to='images/',null=True,blank=True) 
    ImageLink = models.CharField(max_length=200, null=True) 
    ImageTypeID = models.ForeignKey(ImageType, on_delete=models.CASCADE, null=True) 
    Active = models.CharField(max_length=200, null=True) 
    ImageDate = models.DateTimeField(auto_now_add=True, null=True) 
    def __str__(self):          
        return f'{self.ImageTypeID} {self.ImageName}'
        
class Size(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name
class Product(models.Model):
    productName = models.CharField(max_length=200, null=True)
    categoryID = models.ForeignKey(Category, on_delete=models.CASCADE, null=True)
    price = models.DecimalField(max_digits=10, decimal_places=2, null=True)
    productDescript =  RichTextUploadingField(null=True)
    weight = models.CharField(max_length=200, null=True)
    availability = models.CharField(max_length=200, null=True)
    shipping = models.CharField(max_length=200, null=True)
    productImage = models.ImageField(upload_to='images/Products/',null=True,blank=True)
    productDate = models.DateTimeField(auto_now_add=True, null=True)
    sizes = models.ManyToManyField(Size, blank=True)
    def __str__(self):         
        return f'{self.id} - {self.productName}-{self.categoryID.categoryName}'
    

    
class ProductDetail(models.Model):
    productDetailName = models.CharField(max_length=200, null=True)
    productID = models.ForeignKey(Product, on_delete=models.CASCADE, null=True)
    Description =  RichTextUploadingField(null=True)
    Information = RichTextUploadingField(null=True)
    Reviews = RichTextUploadingField(null=True)
    productDetailDate = models.DateTimeField (auto_now_add=True, null=True)
    def __str__(self):         
        return f'{self.id} - {self.productDetailName}-{self.productID.productName}'

class ProductDetailImage(models.Model):
    productDetailImageName = models.CharField(max_length=200, null=True)
    productID = models.ForeignKey(Product, on_delete=models.CASCADE, null=True)
    productDetailImage = models.ImageField(upload_to='images/productDetail/',null=True,blank=True)
    imageDate = models.DateTimeField(auto_now_add=True, null=True)
    def __str__(self):         
        return f'{self.id} - {self.productDetailImageName}-{self.productID.productName}'
    
class HomeSlider(models.Model):
    title = models.CharField(max_length=255)
    subtitle = models.CharField(max_length=255, blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    button_text = models.CharField(max_length=50, default="Discover Now")
    button_link = models.CharField(max_length=255, default="#")

    image = models.ImageField(upload_to="slider/")  # background or main image

    def __str__(self):
        return self.title
    
from django.db import models

class DealOfTheMonth(models.Model):
    title = models.CharField(max_length=255, default="Deal of the Month")
    subtitle = models.CharField(max_length=255, blank=True, null=True)
    main_product_name = models.CharField(max_length=255)
    original_price = models.DecimalField(max_digits=10, decimal_places=2)
    sale_price = models.DecimalField(max_digits=10, decimal_places=2)
    main_image = models.ImageField(upload_to="deals/")
    thumbnail_images = models.ManyToManyField('DealThumbnail', blank=True)
    timer_end = models.DateTimeField(blank=True, null=True)  # optional for countdown

    def __str__(self):
        return self.main_product_name


class DealThumbnail(models.Model):
    image = models.ImageField(upload_to="deal_thumbnails/")

    def __str__(self):
        return self.image.name
    
class Book(models.Model):
    title = models.CharField(max_length=200)
    author = models.CharField(max_length=100)
    published_date = models.DateField()
    def __str__(self):
        return self.title
    
class Item(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        		return self.name
    
class BillingDetail(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    country = models.CharField(max_length=100)
    address = models.CharField(max_length=255)
    town = models.CharField(max_length=100)
    postcode = models.CharField(max_length=20)
    phone = models.CharField(max_length=20)
    email = models.EmailField()
    qr_code_image = models.ImageField(upload_to='qrcodes/', null=True, blank=True)
    total = models.FloatField()

    def __str__(self):
        return f"{self.first_name} {self.last_name}"


class PaymentMethods(models.Model):
    name = models.CharField(max_length=100)

    payment_link = models.URLField()

    def __str__(self):
        return self.name
    
class BlogPost(models.Model):
    title = models.CharField(max_length=255)
    content = models.TextField()
    singleContent=models.TextField(null=True)
    image = models.ImageField(upload_to='blog_images/')
    author = models.CharField(max_length=100, default='Admin')
    created_at = models.DateTimeField(default=timezone.now)
    slug = models.SlugField(unique=True)

    def __str__(self):
        return self.title   


    


    
    
