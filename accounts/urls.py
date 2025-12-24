from django.urls import path
from . import views


urlpatterns = [
    # path('', views.home),
    # path('products/', views.products),
    # path('customer/', views.customer)
    path ('', views.indexSport, name='indexSport'),
    path ('aboutSport/', views.aboutSport, name='aboutSport'),
    path('blogsingleSport/<slug:slug>/', views.blogsingleSport, name='blogsingleSport'),
    path ('shopSport/', views.shopSport, name='shopSport'),
    path ('cartSport/', views.cartSport, name='cartSport'),
    path ('contactSport/', views.contactSport, name='contactSport'),
    path ('blogSport/', views.blogSport, name='blogSport'),
    path ('productsingleSport/<int:pk>/', views.productsingleSport, name='productsingleSport'),
    path('checkoutSport/', views.checkoutSport, name='checkoutSport'),
    path('create/', views.create_book, name='create_book'),
    path('book_list/', views.book_list, name='book_list'),
    path('update/<int:book_id>/', views.update_book, name='update_book'),
    path('delete/<int:book_id>/', views.delete_book, name='delete_book'),
    path('item_list/', views.item_list, name='item_list'),
    path('update_item/<int:pk>/', views.update_item, name='update_item'),  # Update view
    path('delete_item/<int:pk>/', views.delete_item, name='delete_item'),  # Delete view
    path('create_item/', views.create_item, name='create_item'),

    
    path('add_to_cart/<int:product_id>/', views.add_to_cart, name='add_to_cart'),
    path('cart/', views.view_cart, name='view_cart'),
    path('remove_from_cart/<str:product_id>/', views.remove_from_cart, name='remove_from_cart'),


    path('checkout_view/', views.checkout_view, name='checkout_view'),
    path('billing_add/', views.billing_add, name='billing_add'), 
    path("update_cart_quantity/", views.update_cart_quantity, name="update_cart_quantity"),
    path('billing_list/', views.billing_list, name='billing_list'),
    
]