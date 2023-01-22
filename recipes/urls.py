
from django.urls import path, include
from . import views
from authentication.views import loginPage, logoutUser

urlpatterns = [

    path('', views.home, name='home'),
    path('my-recipes/', views.myRecipes, name='my-recipes'),
    path('my-favorites/', views.myFavorites, name='my-favorites'),
    path('add-to-favorites/', views.add_to_favorites, name='add-to-favorites'),
    path('recipe/<str:pk>/', views.recipe, name='recipe'),
    path('create-recipe/', views.createRecipe, name='create-recipe'),
    path('update-recipe/<str:pk>/', views.updateRecipe, name='update-recipe'),
    path('delete-recipe/<str:pk>/', views.deleteRecipe, name='delete-recipe'),
    path('go-back/', views.goBack, name='go-back'),
    path('add-ingredient/<str:pk>/', views.addIngredient, name='add-ingredient'),
    path('add-instruction/<str:pk>/', views.addInstruction, name='add-instruction'),
]
