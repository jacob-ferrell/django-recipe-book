from django.urls import path
from . import views

urlpatterns = [
    path('login/', views.loginPage, name="login"),
    path('logout/', views.logoutUser, name='logout'),
    path('signup/', views.registerUser, name='signup'),
    path('login-guest/', views.loginGuest, name='login-guest')
]