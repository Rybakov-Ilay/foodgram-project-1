from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.core.paginator import Paginator
from .models import Recipe, User, Ingredient, IngredientValue
from api.models import Subscribe, Purchase, Favorite
from .forms import RecipeForm


def index(request):
    paginator = Paginator(Recipe.objects.all(), 6)
    page_number = request.GET.get('page')
    page = paginator.get_page(page_number)
    return render(request, 'index.html', {'page': page, 'paginator': paginator})


@login_required
def new_recipe(request):
    form = RecipeForm(request.POST or None, files=request.FILES or None)
    obj = []
    ing = None
    amount = None
    if request.method == 'POST' and form.is_valid():
        new_recipe = form.save(commit=False)
        new_recipe.author = request.user
        new_recipe.save()
        for key, value in form.data.items():
            # if 'nameIngredient' in key:
            if key.startswith('nameIngredient'):
                title = value
                ing = Ingredient.objects.get(title=title)
            if key.startswith('valueIngredient'):
                # elif 'valueIngredient' in key:
                amount = int(value)
        obj.append(IngredientValue(ingredient=ing, recipe=new_recipe, value=amount))
        IngredientValue.objects.bulk_create(obj)
        return redirect('index')
    return render(request, 'new_recipe.html', {'form': form})


@login_required
def recipe_edit(request, username, recipe_id):
    author = get_object_or_404(User, username=username)
    recipe = get_object_or_404(Recipe, pk=recipe_id)
    redirect_url = redirect('recipe-view', username=recipe.author, recipe_id=recipe.id)
    form = RecipeForm(request.POST or None, files=request.FILES or None, instance=recipe)
    if request.user != recipe.author:
        return redirect_url
    if request.method == 'POST' and form.is_valid():
        form.save()
        return redirect_url
    return render(request, 'new_recipe.html',
                  {'form': form, 'edit': True, 'author': author,
                   'recipe': recipe})


def recipe_delete(request, username, recipe_id):
    recipe = get_object_or_404(Recipe, id=recipe_id)
    if request.user == recipe.author:
        recipe.delete()
        return redirect('profile', username=username)
    return redirect('index')


def profile(request, username):
    author = get_object_or_404(User, username=username)
    recipes = author.recipes.all()
    paginator = Paginator(recipes, 6)
    page_number = request.GET.get('page')
    page = paginator.get_page(page_number)
    subscribe = Subscribe.objects.filter(user=request.user, author=author)
    return render(request, 'authorRecipe.html',
                  {'author': author, 'recipes': recipes,
                   'page': page, 'subscribe': subscribe,
                   'paginator': paginator})


def recipe_view(request, username, recipe_id):
    author = get_object_or_404(User, username=username)
    recipe = get_object_or_404(author.recipes, id=recipe_id)
    ingredients = get_object_or_404(recipe.ingredients)
    value = get_object_or_404(ingredients.ingredient_values)
    subscribe = Subscribe.objects.filter(user=request.user, author=author)
    purchase = Purchase.objects.filter(user=request.user, recipe=recipe)
    return render(request, 'singlePage.html',
                  {'author': author, 'recipe': recipe, 'ingredients': ingredients, 'value': value,
                   'subscribe': subscribe, 'purchase': purchase})


# def subscriptions(request):
#     user = request.user
#     author = user.follower.all().values_list('author', flat=True)
#     recipes = Recipe.objects.filter(author__in=author)
#     paginator = Paginator(author, 3)
#     page_number = request.GET.get('page')
#     page = paginator.get_page(page_number)
#     return render(request, 'myFollow.html',
#                   {'page': page, 'recipes': recipes, 'paginator': paginator, 'author': author})


def subscriptions(request):
    author = User.objects.prefetch_related('recipes').filter(following__user=request.user)
    paginator = Paginator(author, 6)
    page_number = request.GET.get('page')
    page = paginator.get_page(page_number)
    return render(request, 'myFollow.html', {'page': page, 'paginator': paginator, 'author': author})


def favourites(request):
    favourite = Favorite.objects.filter(user=request.user).all()
    paginator = Paginator(favourite, 6)
    page_number = request.GET.get('page')
    page = paginator.get_page(page_number)
    return render(request, 'favorite.html',
                  {'page': page, 'recipe': favourite, 'paginator': paginator})


def purchases_list(request):
    purchases = Purchase.objects.filter(user=request.user).all()
    return render(request, 'shopList.html', {'purchases': purchases})


def purchase_delete(request, purchase_id):
    purchase = get_object_or_404(Purchase, user=request.user, id=purchase_id)
    purchase.delete()
    return redirect('purchases')
