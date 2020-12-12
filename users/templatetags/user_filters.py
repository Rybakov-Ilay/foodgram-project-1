from django import template
from api.models import Favorite, Subscribe, Purchase

register = template.Library()


@register.filter
def addclass(field, css):
    return field.as_widget(attrs={'class': css})


@register.filter
def favorite(recipe, user):
    """Проверяет, находится ли рецепт в избранном."""
    return Favorite.objects.filter(user=user, recipe=recipe).exists()


@register.filter
def subscribe(author, user):
    """Проверяет, находится ли рецепт в списке покупок."""
    return Subscribe.objects.filter(author=author, user=user).exists()


@register.filter
def purchase(recipe, user):
    """Проверяет, находится ли рецепт в списке покупок."""
    return Purchase.objects.filter(user=user, recipe=recipe).exists()
