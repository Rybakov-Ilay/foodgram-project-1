from django.contrib.auth import get_user_model
from django.db import models

User = get_user_model()


class Tag(models.Model):
    title = models.CharField(max_length=20, verbose_name='Название')
    color = models.CharField(max_length=20, verbose_name='Цвет')
    slug = models.SlugField(unique=True, verbose_name='Адрес')

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Тег'
        verbose_name_plural = 'Теги'


class Ingredient(models.Model):
    KILOGRAM = 'кг'
    GRAM = 'г'
    MILLILITERS = 'мл'
    LITERS = 'л'
    TEA_SPOON = 'ч. л.'
    TABLESPOON = 'ст. л.'
    ITEM = 'шт.'
    TASTE = 'по вкусу'
    GLASS = 'стакан'
    LOAF = 'батон'
    PEACE = 'кусок'
    BOTTLE = 'бутылка'
    SACHET = 'пакетик'
    BUNCH = 'пучок'
    LEAF = 'лист'

    INGREDIENT_CHOICES = [
        (KILOGRAM, 'кг'),
        (GRAM, 'г'),
        (MILLILITERS, 'мл'),
        (LITERS, 'л'),
        (TEA_SPOON, 'ч. л.'),
        (TABLESPOON, 'ст. л.'),
        (ITEM, 'шт.'),
        (TASTE, 'по вкусу'),
        (GLASS, 'стакан'),
        (LOAF, 'батон'),
        (PEACE, 'кусок'),
        (BOTTLE, 'бутылка'),
        (SACHET, 'пакетик'),
        (BUNCH, 'пучок'),
        (LEAF, 'лист'),
    ]

    title = models.CharField(max_length=50, verbose_name='Название')
    dimension = models.CharField(choices=INGREDIENT_CHOICES, max_length=10,
                                 verbose_name='Единица измерения')

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Ингредиент'
        verbose_name_plural = 'Ингредиенты'


class Recipe(models.Model):
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='recipes', verbose_name='Автор')
    title = models.CharField(max_length=50, unique=True,
                             verbose_name='Название')
    tags = models.ManyToManyField(
        Tag, related_name='recipes', verbose_name='Теги')
    ingredients = models.ManyToManyField(
        Ingredient, through='IngredientValue', related_name='recipes',
        verbose_name='Ингридиенты')
    cooking_time = models.PositiveSmallIntegerField(
        verbose_name='Время приготовления', help_text='в минутах')
    text = models.TextField(verbose_name='Описание рецепта')
    image = models.ImageField(upload_to='media/', verbose_name='Изображение')
    pub_date = models.DateTimeField(
        'Дата добавления', auto_now_add=True, db_index=True
    )

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Рецепт'
        verbose_name_plural = 'Рецепты'
        ordering = ('-pub_date',)


class IngredientValue(models.Model):
    ingredient = models.ForeignKey(Ingredient, related_name='values',
                                   on_delete=models.CASCADE,
                                   verbose_name='Ингридиент')
    recipe = models.ForeignKey(Recipe, related_name='values',
                               on_delete=models.CASCADE, verbose_name='Рецерт')
    value = models.PositiveSmallIntegerField(verbose_name='Количество')

    def __str__(self):
        return str(self.value)

    class Meta:
        verbose_name = 'Количество ингридиента'
        verbose_name_plural = 'Количество игридиентов'
