from django.urls import path
from .import views
urlpatterns=[
    path('addingcart/<int:id>/',views.Add_to_Shopping_cart,name='Add_to_cart'),
    path('cart_details/',views.cart_details,name="cart_details"),
    path('cart_delete/<int:id>/',views.cart_delete,name="cart_delete"),
    path('ordercart/',views.OrderCart,name='order_cart')
]