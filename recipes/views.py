from django.shortcuts import render, redirect, HttpResponseRedirect
from .models import Recipe, Favorite, Ingredient, Instruction
from .forms import RecipeForm
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, JsonResponse
import requests
import json
import os

def getRecentRecipes(user):
    recipes = Recipe.objects.exclude(author=user).order_by('-created_at')[:5]
    return recipes

def getCounts(user):
        counts = {'my_recipes': 0, 'my_favorites': 0}
        if user.is_authenticated:
            counts['my_recipes'] = Recipe.objects.filter(author=user).count()
            counts['my_favorites'] = Favorite.objects.filter(user=user).count()
        return counts

def getFavorites(user):
    return Favorite.objects.filter(user=user).values_list('recipe', flat=True)
    

def home(request):
    user = request.user
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
        return  data['results']

    def callEdamamAPI():
        query = request.GET.get('q')

        if query:
            url = f"https://api.edamam.com/api/recipes/v2?type=public&q={query}&app_id={os.environ.get('EDAMAM_APP_ID')}&app_key={os.environ.get('EDAMAM_APP_KEY')}&imageSize=THUMBNAIL&random=true&field=uri&field=label&field=image&field=ingredients&field=shareAs"
        else:
            url = f"https://api.edamam.com/api/recipes/v2?type=public&app_id={os.environ.get('EDAMAM_APP_ID')}&app_key={os.environ.get('EDAMAM_APP_KEY')}&imageSize=THUMBNAIL&random=true&field=uri&field=label&field=image&field=ingredients&field=shareAs"
        response = requests.request("GET", url)
        data = response.json()
        recipes = data['hits']
        for recipe in recipes:
            str = recipe['recipe']['uri']
            start = str.find("recipe")
            recipe['recipe']['uri'] = str[start:]
        with open("/home/jacob/projects/django_recipe_book/static/mockEdamam.txt", 'w') as outfile:
            outfile.write(json.dumps(recipes))
        return recipes
    
    def getMockData():
        with open("/home/jacob/projects/django_recipe_book/static/mockEdamam.txt", 'r') as file:
            mock_data = json.load(file)
            return mock_data
    context = {'recipes': getMockData(), 'type': 'discover', 'counts': getCounts(user), 'recent_recipes': getRecentRecipes(user), 'favorites': getFavorites(user)}

    return render(request, 'recipes/home.html', context)

def recipe(request, pk):

    if 'recipe' not in pk:
        recipe = Recipe.objects.get(id=pk)
        recipe_dict = {
            'name': recipe.name,
            'description': recipe.description,
            'ingredients': Ingredient.objects.filter(recipe=recipe),
            'instructions': Instruction.objects.filter(recipe=recipe)
        }
        recipe = recipe_dict
        type = 'own'
    else:
        url = f"https://api.edamam.com/api/recipes/v2/{pk}?type=public&app_id={os.environ.get('EDAMAM_APP_ID')}&app_key={os.environ.get('EDAMAM_APP_KEY')}"
        response = requests.request("GET", url)
        data = response.json()
        recipe = data['recipe']
        type = ''
    recipe_id = pk
    context = {'recipe': recipe, 'recipe_id': recipe_id, 'type': type}
    return render(request, 'recipes/recipe.html', context)

@login_required(login_url='login')
def myRecipes(request):
    user = request.user
    recipes = Recipe.objects.filter(author=request.user)
    context = {'recipes': recipes, 'type': 'my-recipes', 'counts': getCounts(user), 'recent_recipes': getRecentRecipes(user), 'favorites': getFavorites(user)}
    return render(request, 'recipes/home.html', context)

@login_required(login_url='login')
def myFavorites(request):
    user = request.user
    favorites = Favorite.objects.filter(user=request.user)
    """ favorite_uris = []
    for favorite in favorites:
        print(favorite.recipe)
        favorite_uris.append(favorite.recipe)
    print(favorite_uris)
    recipes = []
    for uri in favorite_uris:
        url = f"https://api.edamam.com/api/recipes/v2/{uri}?type=public&app_id={os.environ.get('EDAMAM_APP_ID')}&app_key={os.environ.get('EDAMAM_APP_KEY')}"
        response = requests.request("GET", url)
        data = response.json()
        print(data)
        print('!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!')
        recipe = data['recipe']
        recipes.append(recipe) """
    context = {'recipes': favorites, 'type': 'my-favorites', 'counts': getCounts(user), 'recent_recipes': getRecentRecipes(user), 'favorites': getFavorites(user)}
    return render(request, 'recipes/home.html', context)

@login_required(login_url='login')
def add_to_favorites(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        user = request.user
        recipe = data['recipe']
        label = data['label']
        share = data['share']
        favorite, created = Favorite.objects.get_or_create(user=user, recipe=recipe, label=label, share_link=share)
        if not created:
            favorite.delete()
        return JsonResponse({'status': 'success'}, status=201)
    return JsonResponse({'status': 'error'}, status=400)

@login_required(login_url='login')
def createRecipe(request):
    if request.method == 'POST':
        data = request.POST
        name = data.get('name')
        description = data.get('description')
        if request.user.is_authenticated and name and description:
            recipe = Recipe.objects.create(name=name, description=description, author=request.user)
            return redirect('add-ingredient', pk=recipe.id)
    context = {'type': 'create-recipe', 'counts': getCounts(request.user)}
    return render(request, 'recipes/create_recipe.html', context)

@login_required(login_url='login')
def addIngredient(request, pk):
    recipe = Recipe.objects.get(id=pk)
    if request.method == 'POST':
        ingredient = request.POST.get('ingredient')
        Ingredient.objects.create(text=ingredient, recipe=recipe)
        return redirect('add-ingredient', pk=recipe.id)
    context = {'ingredients': Ingredient.objects.filter(recipe=recipe), 'recipe_id': pk}
    return render(request, 'recipes/add_ingredients.html', context)

@login_required(login_url='login')
def addInstruction(request, pk):
    recipe = Recipe.objects.get(id=pk)
    if request.method == 'POST':
        instruction = request.POST.get('instruction')
        Instruction.objects.create(text=instruction, recipe=recipe)
        return redirect('add-instruction', pk=recipe.id)
    context = {'instructions': Instruction.objects.filter(recipe=recipe)}
    return render(request, 'recipes/add_instructions.html', context)


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

def goBack(request):
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
