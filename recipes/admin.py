from django.contrib import admin
from .models import Recipe, Ingredient, Favorite, Instruction

admin.site.register(Recipe)
admin.site.register(Ingredient)
admin.site.register(Favorite)
admin.site.register(Instruction)
