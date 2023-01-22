from django.db import models
from django.contrib.auth.models import User

class Recipe(models.Model):

    name = models.CharField(max_length=50)

    description = models.TextField()

    author = models.ForeignKey(User, on_delete=models.CASCADE)

    created_at = models.DateTimeField(auto_now_add=True)

    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


class Ingredient(models.Model):

    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE)

    text = models.TextField(null=False)

    created_at = models.DateTimeField(auto_now_add=True)
    
    updated = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.text

class Favorite(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=False)

    recipe = models.TextField(null=False)

    label = models.TextField(null=False)

    share_link = models.TextField(null=False)

    created_at = models.DateTimeField(auto_now_add=True)
    
    updated = models.DateTimeField(auto_now=True)

class Instruction(models.Model):
    text = models.TextField(null=False)

    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE)

    created_at = models.DateTimeField(auto_now_add=True)
    
    updated = models.DateTimeField(auto_now=True)
