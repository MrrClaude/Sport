from django import forms
from .models import Item ,Product

class ItemForm(forms.ModelForm):
    class Meta:
        model = Item
        fields = ['name', 'description']

class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['productName', 'categoryID','productDescript','price','availability','productImage']