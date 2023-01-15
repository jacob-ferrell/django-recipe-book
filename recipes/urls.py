
from django.urls import path, include
from . import views
from authentication.views import loginPage, logoutUser

urlpatterns = [

    path('', views.home, name='home'),
    path('recipe/<str:pk>/', views.recipe, name='recipe'),
    path('create-recipe/', views.createRecipe, name='create-recipe'),
    path('update-recipe/<str:pk>/', views.updateRecipe, name='update-recipe'),
    path('delete-recipe/<str:pk>/', views.deleteRecipe, name='delete-recipe')
]
