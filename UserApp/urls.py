from django.urls import path
from .import views
urlpatterns=[
     path('logout/',views.user_logout,name='user_logout'),
     path('login/',views.user_login,name='user_login'),
     path('register/',views.user_register,name='user_register'),
     path('profile/',views.userprofile,name="userprofile"),
     path('user_update/',views.user_update,name="user_update"),
     path('user_password/',views.user_password,name='user_password')
]