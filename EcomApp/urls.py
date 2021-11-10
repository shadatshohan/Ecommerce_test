from django.contrib import admin
from django.urls import path,include
from django.conf import settings 
from django.conf.urls.static import static
from .import views
urlpatterns = [
    path('',views.home,name='home'),
    path('product/<int:id>/',views.product_single,name='product_single'),
    path('product/<int:id>/<slug:slug>/',views.category_product,name='category_product'),
    path('about/',views.about,name='about'),
    path('contact/',views.contact,name='contact_dat'),
    path('search/',views.SearchView,name='SearchView')
]