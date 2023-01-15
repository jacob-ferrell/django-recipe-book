from django.shortcuts import render, redirect
from .models import Recipe
from .forms import RecipeForm
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
import requests
import json
import os


def home(request):
    def callTastyAPI():
        url = "https://tasty.p.rapidapi.com/recipes/list"

        querystring = {"from":"0","size":"5","tags":"under_30_minutes"}

        headers = {
            "X-RapidAPI-Key": os.environ.get('TASTY_API_KEY'),
            "X-RapidAPI-Host": "tasty.p.rapidapi.com"
        }

        response = requests.request("GET", url, headers=headers, params=querystring)
        if response.status_code != 200:
            return render(request, HttpResponse('Failed to fetch data from the Tasty API'))
        data = response.json()
        print(data)
        return  data['results']

    def callEdamamAPI():
        query = 'chicken'
        url = f"https://api.edamam.com/api/recipes/v2?type=public&q={query}&app_id={os.environ.get('EDAMAM_APP_ID')}&app_key={os.environ.get('EDAMAM_APP_KEY')}&imageSize=THUMBNAIL&random=true&field=label&field=image&field=ingredients"
        response = requests.request("GET", url)
        data = response.json()
        print(data)
        return data['hits']
    
    def getMockData():
        with open('/home/jacob/projects/django_recipe_book/static/recipeData.txt', 'r') as file:
            mock_data = json.load(file)
            return mock_data['results']

    """ if not request.user.is_authenticated:
        return redirect('login')
    recipes = Recipe.objects.filter(author=request.user) """
    context = {'recipes': callEdamamAPI()}

    return render(request, 'recipes/home.html', context)

def recipe(request, pk):
    recipe = Recipe.objects.get(id=pk)
    context = {'recipe': recipe}
    return render(request, 'recipes/recipe.html', context)

@login_required(login_url='login')
def createRecipe(request):
    form = RecipeForm
    if request.method == 'POST':
        form = RecipeForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('home')
    context = {'form': form}
    return render(request, 'recipes/recipe_form.html', context)

@login_required(login_url='login')
def updateRecipe(request, pk):
    recipe = Recipe.objects.get(id=pk)
    form = RecipeForm(instance=recipe)
    if request.user != recipe.author:
        return HttpResponse('You are attempting to edit a recipe you did not create!')
    if request.method == 'POST':
        form = RecipeForm(request.POST, instance=recipe)
        if form.is_valid():
            form.save()
            return redirect('home')
    context = {'form': form}
    return render(request, 'recipes/recipe_form.html', context)

@login_required(login_url='login')
def deleteRecipe(request, pk):
    recipe = Recipe.objects.get(id=pk)
    if request.user != recipe.author:
        return HttpResponse('You are attempting to delete a recipe you did not create!')
    if request.method == 'POST':
        recipe.delete()
        return redirect('home')
    return render(request, 'recipes/delete.html', {'obj': recipe})

