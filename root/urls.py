from django.urls import path
from . import views

urlpatterns=[
	path('',views.store,name="store"),
	path('cart/',views.cart,name="cart"),
	path('checkout/',views.checkout,name="checkout"),
	path('search/',views.search,name="search"),
	path('add_to_cart/<int:product_id>/', views.add_to_cart, name='add_to_cart'),
	path('view/<int:product_id>/',views.view,name='view'),
	path('login/',views.login_view,name='login'),
	path('register/',views.registerUser,name='register'),
	path('logout/',views.custom_logout,name='logout'),
	path('increment_quantity/<int:order_item_id>/', views.increment_quantity, name='increment_quantity'),
    	path('decrement_quantity/<int:order_item_id>/', views.decrement_quantity, name='decrement_quantity'),
]
