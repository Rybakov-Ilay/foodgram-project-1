from django import forms

from .models import Ingredient, Recipe


class RecipeForm(forms.ModelForm):
    class Meta:
        model = Recipe
        fields = [
            'title',
            'breakfast',
            'lunch',
            'dinner',
            'cooking_time',
            'text',
            'image',

        ]


class IngredientForm(forms.ModelForm):
    class Meta:
        model = Ingredient
        fields = '__all__'


