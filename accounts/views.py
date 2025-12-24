from django.shortcuts import render ,redirect
from .forms import ItemForm ,ProductForm
from .models import *
from django.db.models import Count
from django.shortcuts import get_object_or_404
from django.core.paginator import Paginator
from django.db.models import Min, Max
from .models import *
from django.http import HttpResponse ,JsonResponse
# Create your views here.
def indexSport(request):
    sliders = HomeSlider.objects.all()
    deal = DealOfTheMonth.objects.last()
    categories = Category.objects.all()

   
    products = Product.objects.all()  

    # Get category filter from GET
    category_id = request.GET.get('category')
    if category_id:
        products = products.filter(categoryID__id=category_id)

    # Get search query
    search_query = request.GET.get('q')
    if search_query:
        products = products.filter(
            productName__icontains=search_query
        ) | products.filter(
            categoryID__categoryName__icontains=search_query
        )

    # Store total count before limiting
    total_products = products.count()

    # Get product count limit from GET parameter
    count = request.GET.get('count', '8')  # Default to 8
    
    if count != 'all':
        try:
            limit = int(count)
            products = products[:limit]
        except ValueError:
            products = products[:8]  # Default to 8 if invalid

    context = {
        "sliders": sliders,
        "deal": deal,
        "categories": categories,

        "ObjDTProduct": products,
        
        "category_id": category_id,
        "search_query": search_query,
        "total_products": total_products,  # Total before limiting
    }

    return render(request, "sports/index.html", context)


def search_suggestions(request):
    """
    AJAX endpoint for autocomplete suggestions
    """
    print("=== Search Suggestions Called ===")
    
    query = request.GET.get('q', '').strip()
    category_id = request.GET.get('category', '')
    
    print(f"Query: {query}")
    print(f"Category ID: {category_id}")
    
    suggestions = []
    
    if len(query) >= 1:
        # Filter products by name
        products_by_name = Product.objects.filter(productName__icontains=query)
        
        # Filter products by category name
        products_by_category = Product.objects.filter(categoryID__categoryName__icontains=query)
        
        # Combine both querysets
        all_products = (products_by_name | products_by_category).distinct()
        
        # Apply category filter if provided
        if category_id:
            all_products = all_products.filter(categoryID__id=category_id)
        
        # Limit to 10 products
        all_products = all_products[:10]
        
        print(f"Found {all_products.count()} products")
        
        # Format product suggestions
        for product in all_products:
            suggestions.append({
                'name': product.productName,
                'category': product.categoryID.categoryName,
                'type': 'product'
            })
        
        # Also add matching category names
        categories = Category.objects.filter(categoryName__icontains=query)[:5]
        
        print(f"Found {categories.count()} categories")
        
        for category in categories:
            suggestions.append({
                'name': category.categoryName,
                'category': '',
                'type': 'category'
            })
    
    print(f"Total suggestions: {len(suggestions)}")
    print(f"Returning JSON: {suggestions}")
    
    return JsonResponse({'suggestions': suggestions})

def aboutSport(request):
    bgImage = Image.objects.filter(id=4).first()
    Imagenike = Image.objects.filter(id=8).first()
    Imageaddidas = Image.objects.filter(id=10).first()
    Imagepuma = Image.objects.filter(id=9).first()
    
    context = {
        'objbgimage': bgImage,
        'bgnikeimage': Imagenike,
        'bgaddidasimage': Imageaddidas,
        'bgpumaimage': Imagepuma,
    }
    return render(request, "sports/about.html", context)

def cartSport(request):
    bgImage=Image.objects.get(id=1)
    return render(request, "sports/cart.html",{'objbgimage':bgImage})
def contactSport(request):
    bgImage=Image.objects.filter(id=6).first()
    mapImage=Image.objects.filter(id=11).first()
    return render(request, "sports/contact.html",{'objbgimage':bgImage,'objmapImage':mapImage})
def blogSport(request):
    bgImage = Image.objects.get(id=5)  # Hero image
    posts = BlogPost.objects.all().order_by('-created_at') 
    categories = Category.objects.annotate(product_count=Count('product'))
    return render(request, "sports/blog.html", {
        'objbgimage': bgImage,
        'posts': posts,
        'categories': categories,
    })
def blogsingleSport(request, slug):
    bgImage = Image.objects.get(id=5)  # Hero image
    post = BlogPost.objects.get(slug=slug)
    categories = Category.objects.annotate(product_count=Count('product'))
    return render(request, "sports/blog-single.html", {
        'objbgimage': bgImage,
        'post': post,
        'categories': categories,
    })

def shopSport(request):
    products = Product.objects.all()
    categories = Category.objects.all()
    bgimage=Image.objects.get(id=1)

    # Get filter parameters
    price_from = request.GET.get('price_from')
    price_to = request.GET.get('price_to')
    category_id = request.GET.get('category')
    sort = request.GET.get('sort')
    search_query = request.GET.get('q')  # Search query
    count = request.GET.get('count', '12')  # Product count per page, default 12

    # ==========================
    # Filter by category
    # ==========================
    if category_id:
        products = products.filter(categoryID__id=category_id)

    # ==========================
    # Filter by search query
    # ==========================
    if search_query:
        products = products.filter(
            productName__icontains=search_query
        ) | products.filter(
            categoryID__categoryName__icontains=search_query
        )

    # ==========================
    # Filter by price
    # ==========================
    if price_from:
        products = products.filter(price__gte=price_from)
    if price_to:
        products = products.filter(price__lte=price_to)

    # ==========================
    # Sorting
    # ==========================
    if sort == 'price_asc':
        products = products.order_by('price')
    elif sort == 'price_desc':
        products = products.order_by('-price')

    # ==========================
    # Get price range for filter UI
    # ==========================
    min_price = Product.objects.order_by('price').first().price if Product.objects.exists() else 0
    max_price = Product.objects.order_by('-price').first().price if Product.objects.exists() else 1000

    # ==========================
    # Determine products per page
    # ==========================
    if count == 'all':
        per_page = products.count() or 12  # Show all products
    else:
        try:
            per_page = int(count)
        except ValueError:
            per_page = 12  # Default to 12 if invalid

    # ================================
    # Pagination
    # ================================
    paginator = Paginator(products, per_page)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'categories': categories,
        'page_obj': page_obj,
        'price_from': price_from,
        'price_to': price_to,
        'sort': sort,
        'category_id': category_id,
        'min_price': min_price,
        'max_price': max_price,
        'objbgimage':bgimage,
    }

    return render(request, "sports/shop.html", context)





def productsingleSport(request, pk):
    # Get the product (must exist)
    product = get_object_or_404(Product, id=pk)

    # Try to get product detail, but allow missing
    product_detail = ProductDetail.objects.filter(productID=pk).first()

    # Get sizes
    sizes = product.sizes.all() 

    context = {
        'ObjProductDetail': product,
        'ObjDTProductDetailInfo': product_detail,  # could be None
        'sizes': sizes, 
    }

    return render(request, "sports/product-single.html", context)
def checkoutSport(request):
    
    return render(request, "sports/checkout.html")

def create_book(request):
    if request.method == "POST":
        title = request.POST['title']
        author = request.POST['author']
        published_date = request.POST['published_date']
        Book.objects.create(title=title, author=author, published_date=published_date)
        return redirect('book_list')
    return render(request, 'sports/create_book.html')

def book_list(request):
    books = Book.objects.all()
    return render(request, 'sports/book_list.html', {'books': books})

def update_book(request, book_id):
    book = get_object_or_404(Book, id=book_id)
    if request.method == "POST":
        book.title = request.POST['title']
        book.author = request.POST['author']
        book.published_date = request.POST['published_date']
        book.save()
        return redirect('book_list')
    return render(request, 'sports/update_book.html', {'book': book})

def delete_book(request, book_id):
    book = get_object_or_404(Book, id=book_id)
    if request.method == "POST":
        book.delete()
        return redirect('book_list')
    return render(request, 'sports/delete_book.html', {'book': book})

def create_item(request):
    if request.method == 'POST':
        form = ItemForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('item_list')  # Redirect to the list view
    else:
        form = ItemForm()
    return render(request, 'sports/create_item.html', {'form': form})

def item_list(request):
    items = Item.objects.all()
    return render(request, 'sports/item_list.html', {'items': items})

def create_item(request):
    if request.method == 'POST':
        form = ItemForm(request.POST)
        if form.is_valid():
            form.save()
            # return redirect('item_list')  # Redirect to the list view
    else:
        form = ItemForm()
    return render(request, 'sports/create_item.html', {'ProductForm': form})


def update_item(request, pk):
    item = get_object_or_404(Item, pk=pk)
    if request.method == 'POST':
        form = ItemForm(request.POST, instance=item)
        if form.is_valid():
            form.save()
            return redirect('item_list')  # Redirect to the list view
    else:
        form = ItemForm(instance=item)
    return render(request, 'sports/update_item.html', {'form': form, 'item': item})

def delete_item(request, pk):
    item = get_object_or_404(Item, pk=pk)
    if request.method == 'POST':
        item.delete()
        return redirect('item_list')  # Redirect to the list view after deletion
    return render(request, 'sports/delete_item.html', {'item': item})


def add_to_cart(request, product_id):
    # Get the selected size from query string
    selected_size_id = request.GET.get('size')  
    product = Product.objects.get(id=product_id)
    quantity = int(request.GET.get("qty", 1))  # Use the quantity from the page
    size_name = ''

    if selected_size_id:
        try:
            size = product.sizes.get(id=selected_size_id)
            size_name = size.name
        except Size.DoesNotExist:
            size_name = ''
    else:
        # Default to SMALL if it exists
        small_size = product.sizes.filter(name__iexact='S').first()
        if small_size:
            selected_size_id = small_size.id
            size_name = small_size.name
        else:
            # Fallback if no size available
            selected_size_id = None
            size_name = ''

    # Unique key for cart to handle same product with different sizes
    key = f"{product_id}_{selected_size_id}" if selected_size_id else str(product_id)

    cart = request.session.get('cart', {})

    if key in cart:
        # Add the selected quantity instead of always +1
        cart[key]['quantity'] += quantity
        cart[key]['total'] = cart[key]['quantity'] * cart[key]['price']
    else:
        cart[key] = {
            'productName': product.productName,
            'size': size_name,
            'price': float(product.price),
            'quantity': quantity,  # Use selected quantity
            'total': float(product.price) * quantity,  # Correct total
            'image': product.productImage.url if product.productImage else '',
        }

    request.session['cart'] = cart
    return redirect('view_cart')




def view_cart(request):
    cart = request.session.get('cart', {})
    bgImage=Image.objects.get(id=2)
    # recompute totals
    for item in cart.values():
        item['total'] = item['price'] * item['quantity']

    total_price = sum(item['total'] for item in cart.values())

    request.session['cart'] = cart

    return render(request, 'sports/cart.html', {
        'cart': cart,
        'total_price': total_price,
        'objbgImage': bgImage,
    })


def remove_from_cart(request, product_id):
    cart = request.session.get('cart', {})
    cart.pop(str(product_id), None)
    request.session['cart'] = cart
    return redirect('view_cart')

def checkout_view(request):
    cart = request.session.get('cart', {})

    bgImage = Image.objects.filter(id=3).first()  # safe

    total_price = sum(
        item.get('total', 0) for item in cart.values()
    )

    payment_methods = PaymentMethods.objects.all()

    return render(request, 'sports/checkout.html', {
        'cart': cart,
        'total_price': total_price,
        'payment_methods': payment_methods,
        'objbgImage': bgImage,
    })


def update_cart_quantity(request):
    product_id = request.POST.get('product_id')
    new_quantity = int(request.POST.get('quantity', 1))

    cart = request.session.get('cart', {})

    if product_id in cart:
        cart[product_id]['quantity'] = new_quantity
        cart[product_id]['total'] = new_quantity * cart[product_id]['price']

    request.session['cart'] = cart

    # Calculate new subtotal
    total_price = sum(item['total'] for item in cart.values())

    return JsonResponse({
        'status': 'success',
        'new_total': cart[product_id]['total'],
        'cart_total': total_price
    })

def billing_add(request):
    cart = request.session.get('cart', {})
    total_price = sum(item['total'] for item in cart.values())

    if request.method == "POST":
        data = request.POST
        qr_image = request.FILES.get('qr_code_image')

        billing = BillingDetail(
            first_name=data['first_name'],
            last_name=data['last_name'],
            country=data['country'],
            address=data['address'],
            town=data['town'],
            postcode=data['postcode'],
            phone=data['phone'],
            email=data['email'],
            qr_code_image=qr_image,
            total=data['total']
        )
        billing.save()
        return redirect('billing_list')
    
    return render(request, 'sports/checkout.html', {
        'cart': cart,
        'total_price': total_price,
    })

def billing_list(request):
    billings = BillingDetail.objects.all()
    return render(request, 'sports/BillingList.html', {'billings': billings})








