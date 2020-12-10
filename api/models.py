from django.db import models
from recipes.models import Recipe, User


class Favorite(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='favorites')
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE, related_name='recipe_favorite')


class Subscribe(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='following')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='follower')


class Purchase(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='purchases')
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE, related_name='recipe_purchase')
