from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.core.paginator import Paginator
from django.http import HttpResponse
from .models import Recipe, User, Ingredient, IngredientValue, Tag
from api.models import Purchase, Favorite
from .forms import RecipeForm
import csv


def index(request):
    if 'filters' in request.GET:
        filters = request.GET.getlist('filters')

        recipes = Recipe.objects.filter(tags__slug__in=filters).distinct()
    else:
        recipes = Recipe.objects.all()

    tags = Tag.objects.all()
    paginator = Paginator(recipes, 6)
    page_number = request.GET.get('page')
    page = paginator.get_page(page_number)
    return render(request, 'index.html', {'page': page, 'paginator': paginator, 'tags': tags})


def create_ingredient(form, recipe):
    obj = []
    for key, value in form.data.items():
        if 'nameIngredient' in key:
            title = value
        elif 'valueIngredient' in key:
            amount = value
            ingredient = Ingredient.objects.get(title=title)
            obj.append(IngredientValue(ingredient=ingredient, recipe=recipe, value=amount))
    IngredientValue.objects.bulk_create(obj)


@login_required
def new_recipe(request):
    form = RecipeForm(request.POST or None, files=request.FILES or None)
    if request.method == 'POST' and form.is_valid():
        recipe = form.save(commit=False)
        recipe.author = request.user
        recipe.save()
        create_ingredient(form, recipe)
        form.save_m2m()
        return redirect('index')
    return render(request, 'new_recipe.html', {'form': form})


@login_required
def recipe_edit(request, username, recipe_id):
    author = get_object_or_404(User, username=username)
    recipe = get_object_or_404(Recipe, pk=recipe_id)
    redirect_url = redirect('recipe-view', username=recipe.author, recipe_id=recipe.id)
    ingredient = IngredientValue.objects.filter(recipe=recipe)
    form = RecipeForm(request.POST or None, files=request.FILES or None, instance=recipe)
    if request.user != recipe.author:
        return redirect_url
    if request.method == 'POST' and form.is_valid():
        recipe.ingredients.clear()
        recipe.recipe_values.all().delete()
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
    ingredients = recipe.recipe_values.all()
    return render(request, 'single_recipe_page.html',
                  {'author': author, 'recipe': recipe, 'ingredients': ingredients, 'tags': tags})


def profile(request, username):
    author = get_object_or_404(User, username=username)
    if 'filters' in request.GET:
        filters = request.GET.getlist('filters')
        recipes = author.recipes.filter(tags__slug__in=filters).distinct()
    else:
        recipes = author.recipes.all()
    tags = Tag.objects.all()
    paginator = Paginator(recipes, 6)
    page_number = request.GET.get('page')
    page = paginator.get_page(page_number)
    return render(request, 'profile_page.html',
                  {'author': author, 'recipes': recipes,
                   'page': page, 'paginator': paginator, 'tags': tags})


@login_required
def subscriptions(request):
    author = User.objects.prefetch_related('recipes').filter(following__user=request.user)
    paginator = Paginator(author, 6)
    page_number = request.GET.get('page')
    page = paginator.get_page(page_number)
    return render(request, 'follow.html', {'page': page, 'paginator': paginator, 'author': author})


@login_required
def favourites(request):
    if 'filters' in request.GET:
        filters = request.GET.getlist('filters')
        favourite = Favorite.objects.select_related('user').filter(recipe__tags__slug__in=filters)

    else:
        favourite = Favorite.objects.select_related('user').all()
    tags = Tag.objects.all()
    paginator = Paginator(favourite, 6)
    page_number = request.GET.get('page')
    page = paginator.get_page(page_number)
    return render(request, 'favorite.html',
                  {'page': page, 'recipes': favourite, 'paginator': paginator, 'tags': tags})


@login_required
def purchases_list(request):
    purchases = request.user.purchases.all()
    return render(request, 'purchase.html', {'purchases': purchases})


@login_required
def purchase_delete(request, purchase_id):
    purchase = get_object_or_404(Purchase, user=request.user, id=purchase_id)
    purchase.delete()
    return redirect('purchases')


@login_required
def download_shopping_list(request):
    recipes = Recipe.objects.filter(recipe_purchase__user=request.user)

    ingredients_list: dict = {}

    for recipe in recipes:
        ingredients = recipe.ingredients.values_list('title', 'dimension')
        value = recipe.recipe_values.values_list('value', flat=True)

        for pos in range(len(ingredients)):
            title: str = ingredients[pos][0]
            dimension: str = ingredients[pos][1]
            amount: int = value[pos]

            if title in ingredients_list.keys():
                ingredients_list[title] = [ingredients_list[title][0] + amount, dimension]
            else:
                ingredients_list[title] = [amount, dimension]

    response = HttpResponse(content_type='txt/csv')
    response['Content-Disposition'] = 'attachment; filename="shop_list.txt"'
    document = csv.writer(response)

    for key, value in ingredients_list.items():
        document.writerow([f'{key} ({value[1]}) - {value[0]}'])

    return response


def page_not_found(request, exception):
    return render(request, 'includes/404.html', {'path': request.path}, status=404)


def server_error(request):
    return render(request, 'includes/500.html', status=500)
