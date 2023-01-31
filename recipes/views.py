from django.shortcuts import render, redirect, HttpResponseRedirect
from .models import Recipe, Favorite, Ingredient, Instruction
from .forms import RecipeForm
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, JsonResponse
from django.conf import settings
import requests
import json
import os
from django.core.files import File
from PIL import Image

def getRecentRecipes(user):
    if not user.is_authenticated:
        return Recipe.objects.all().order_by('-created_at')[:5]
    return Recipe.objects.exclude(author=user).order_by('-created_at')[:5]

def getCounts(user):
        counts = {'my_recipes': 0, 'my_favorites': 0}
        if user.is_authenticated:
            counts['my_recipes'] = Recipe.objects.filter(author=user).count()
            counts['my_favorites'] = Favorite.objects.filter(user=user).count()
        return counts

def getFavorites(user):
    if not user.is_authenticated:
        return []
    return Favorite.objects.filter(user=user).values_list('recipe', flat=True)
    

def home(request):
    if not request.user.is_authenticated:
        return redirect('login')
    user = request.user

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
    context = {'recipes': callEdamamAPI(), 'type': 'discover', 'counts': getCounts(user), 'recent_recipes': getRecentRecipes(user), 'favorites': getFavorites(user)}

    return render(request, 'recipes/home.html', context)

def recipe(request, pk):
    is_favorite = False
    if 'recipe' not in pk:
        recipe = Recipe.objects.get(id=pk)
        recipe_dict = {
            'name': recipe.name,
            'description': recipe.description,
            'author': recipe.author,
            'ingredients': Ingredient.objects.filter(recipe=recipe),
            'instructions': Instruction.objects.filter(recipe=recipe),
            'image': recipe.recipe_image.url
        }
        recipe = recipe_dict
        type = 'own'
    else:
        url = f"https://api.edamam.com/api/recipes/v2/{pk}?type=public&app_id={os.environ.get('EDAMAM_APP_ID')}&app_key={os.environ.get('EDAMAM_APP_KEY')}"
        response = requests.request("GET", url)
        data = response.json()
        recipe = data['recipe']
        print(recipe)
        type = ''
        is_favorite = pk in getFavorites(request.user)
    recipe_id = pk
    context = {'recipe': recipe, 'recipe_id': recipe_id, 'type': type, 'is_favorite': is_favorite}
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
    context = {'recipes': favorites, 'type': 'my-favorites', 'counts': getCounts(user), 'recent_recipes': getRecentRecipes(user), 'favorites': getFavorites(user)}
    return render(request, 'recipes/home.html', context)

def saveImage(url, id):
    image_folder = os.path.join(settings.MEDIA_ROOT, 'images')
    image = Image.open(url)
    image_path = os.path.join(image_folder, f'{id}.jpg')
    image.save(image_path)
    return image_path
    

@login_required(login_url='login')
def add_to_favorites(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        user = request.user
        recipe = data['recipe']
        label = data['label']
        share = data['share']
        added = True
        favorite, created = Favorite.objects.get_or_create(user=user, recipe=recipe, label=label, share_link=share)
        if not created:
            favorite.delete()
            added = False
        return JsonResponse({'status': 'success', 'added': added}, status=201)
    return JsonResponse({'status': 'error'}, status=400)

@login_required(login_url='login')
def createRecipe(request):
    if request.method == 'POST':
        data = request.POST
        name = data.get('name')
        description = data.get('description')
        if request.user.is_authenticated and name and description:
            image = request.FILES.get('image')
            recipe = Recipe.objects.create(name=name, description=description, author=request.user, recipe_image=image)
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
        return redirect('my-recipes')
    return render(request, 'recipes/delete.html', {'obj': recipe})

def goBack(request):
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

@login_required(login_url='login')
def editItem(request, delete=False):
    data = json.loads(request.body)
    print(data)
    print(delete)
    user = request.user
    pk = int(data['pk'])

    if data['type'] == 'ingredient': 
        ingredient = Ingredient.objects.get(id=pk)
        recipe = Recipe.objects.get(id=ingredient.recipe.id)
        item = ingredient

    else: 
        instruction =  Instruction.objects.get(id=pk)
        recipe = Recipe.objects.get(id=instruction.recipe.id)
        item = instruction

    if recipe.author != user:
        return JsonResponse({'status': 'failed', 'message': 'Current user is not the creator of this recipe'}, status = 400)
    
    if request.method != 'POST':
        return JsonResponse({'status': 'failed', 'message': 'Invalid request method'}, status = 400)
    if not delete:
        item.text = data['text']
        item.save()
    else:
        item.delete()
    return JsonResponse({'status': 'success' }, status = 201)

@login_required(login_url='login')
def deleteItem(request):
    return editItem(request, True)




