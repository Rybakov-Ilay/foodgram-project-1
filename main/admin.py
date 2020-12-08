from django.contrib import admin

from .models import Ingredient, Recipe, IngredientValue


class IngredientAdmin(admin.ModelAdmin):
    list_display = ('title', 'dimension')
    search_fields = ('title',)
    empty_value_display = '-empty-'


class RecipeAdmin(admin.ModelAdmin):
    list_display = ('author', 'title', 'text', 'pub_date',)
    search_fields = ('author', 'title',)
    empty_value_display = '-empty-'

class IngredientValueAdmin(admin.ModelAdmin):
    list_display = ('ingredient', 'recipe', 'value',)
    empty_value_display = '-empty-'

admin.site.register(Ingredient, IngredientAdmin)
admin.site.register(Recipe, RecipeAdmin)
admin.site.register(IngredientValue, IngredientValueAdmin)