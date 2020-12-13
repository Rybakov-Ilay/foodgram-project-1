import csv

from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, redirect, render

from api.models import Favorite, Purchase
from foodgram.settings import OBJECTS_PER_PAGE

from .forms import RecipeForm
from .models import Ingredient, IngredientValue, Recipe, Tag, User


def index(request):
    if 'filters' in request.GET:
        filters = request.GET.getlist('filters')

        recipes = Recipe.objects.filter(tags__slug__in=filters).distinct()
    else:
        recipes = Recipe.objects.all()

    tags = Tag.objects.all()
    paginator = Paginator(recipes, OBJECTS_PER_PAGE)
    page_number = request.GET.get('page')
    page = paginator.get_page(page_number)
    return render(request, 'index.html',
                  {'page': page, 'paginator': paginator, 'tags': tags,
                   'index': True})


def create_ingredient(form, recipe):
    obj = []
    for key, value in form.data.items():
        if 'nameIngredient' in key:
            title = value
        elif 'valueIngredient' in key:
            amount = value
            ingredient = get_object_or_404(Ingredient, title=title)
            obj.append(IngredientValue(ingredient=ingredient, recipe=recipe,
                                       value=amount))
    IngredientValue.objects.bulk_create(obj)


@login_required
def new_recipe(request):
    form = RecipeForm(request.POST or None, files=request.FILES or None)
    if form.is_valid():
        recipe = form.save(commit=False)
        recipe.author = request.user
        recipe.save()
        create_ingredient(form, recipe)
        form.save_m2m()
        return redirect('index')
    return render(request, 'new_recipe.html',
                  {'form': form, 'new_recipe': True})


@login_required
def recipe_edit(request, username, recipe_id):
    author = get_object_or_404(User, username=username)
    recipe = get_object_or_404(Recipe, pk=recipe_id)
    redirect_url = redirect('recipe-view', username=recipe.author,
                            recipe_id=recipe.id)
    ingredient = IngredientValue.objects.filter(recipe=recipe)
    form = RecipeForm(request.POST or None, files=request.FILES or None,
                      instance=recipe)
    if request.user != recipe.author:
        return redirect_url
    if form.is_valid():
        recipe.ingredients.clear()
        recipe.values.all().delete()
        create_ingredient(form, recipe)
        form.save()
        return redirect_url
    return render(request, 'new_recipe.html',
                  {'form': form, 'edit': True, 'author': author,
                   'recipe': recipe, 'ingredients': ingredient})


@login_required
def recipe_delete(request, username, recipe_id):
    recipe = get_object_or_404(Recipe, id=recipe_id)
    if request.user == recipe.author:
        recipe.delete()
        return redirect('profile', username=username)
    return redirect('index')


def recipe_view(request, username, recipe_id):
    author = get_object_or_404(User, username=username)
    recipe = get_object_or_404(author.recipes, id=recipe_id)
    tags = recipe.tags.all()
    ingredients = recipe.values.all()
    return render(request, 'single_recipe_page.html',
                  {'author': author, 'recipe': recipe,
                   'ingredients': ingredients, 'tags': tags})


def profile(request, username):
    author = get_object_or_404(User, username=username)
    if 'filters' in request.GET:
        filters = request.GET.getlist('filters')
        recipes = author.recipes.filter(tags__slug__in=filters).distinct()
    else:
        recipes = author.recipes.all()
    tags = Tag.objects.all()
    paginator = Paginator(recipes, OBJECTS_PER_PAGE)
    page_number = request.GET.get('page')
    page = paginator.get_page(page_number)
    return render(request, 'profile_page.html',
                  {'author': author, 'recipes': recipes,
                   'page': page, 'paginator': paginator, 'tags': tags})


@login_required
def subscriptions(request):
    author = User.objects.prefetch_related('recipes').filter(
        following__user=request.user)
    paginator = Paginator(author, OBJECTS_PER_PAGE)
    page_number = request.GET.get('page')
    page = paginator.get_page(page_number)
    return render(request, 'follow.html',
                  {'page': page, 'paginator': paginator, 'author': author,
                   'subscriptions': True})


@login_required
def favorites(request):
    if 'filters' in request.GET:
        filters = request.GET.getlist('filters')
        favorite = request.user.favorites.all().filter(
            recipe__tags__slug__in=filters)

    else:
        favorite = request.user.favorites.all()

    tags = Tag.objects.all()
    paginator = Paginator(favorite, OBJECTS_PER_PAGE)
    page_number = request.GET.get('page')
    page = paginator.get_page(page_number)
    return render(request, 'favorite.html',
                  {'page': page, 'recipes': favorite, 'paginator': paginator,
                   'tags': tags, favorites: True})


@login_required
def get_purchases(request):
    user = request.user
    purchases = user.purchases.all()
    return render(request, 'purchase.html',
                  {'purchases': purchases, 'purchases_page': True})


@login_required
def purchase_delete(request, purchase_id):
    purchase = get_object_or_404(Purchase, user=request.user, id=purchase_id)
    purchase.delete()
    return redirect('purchases')


@login_required
def download_purchases(request):
    recipes = Recipe.objects.filter(purchases__user=request.user)

    ingredients_for_purchase: dict = {}

    for recipe in recipes:
        ingredients = recipe.ingredients.values_list('title', 'dimension')
        value = recipe.values.values_list('value', flat=True)

        for item in range(len(ingredients)):
            title: str = ingredients[item][0]
            dimension: str = ingredients[item][1]
            amount: int = value[item]

            if title in ingredients_for_purchase:
                ingredients_for_purchase[title] = [
                    ingredients_for_purchase[title][0] + amount, dimension]
            else:
                ingredients_for_purchase[title] = [amount, dimension]

    response = HttpResponse(content_type='txt/csv')
    response['Content-Disposition'] = 'attachment; filename="shop_list.txt"'
    document = csv.writer(response)

    for key, value in ingredients_for_purchase.items():
        document.writerow([f'{key} ({value[1]}) - {value[0]}'])

    return response
