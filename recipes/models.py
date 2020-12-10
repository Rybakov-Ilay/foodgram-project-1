from django.contrib.auth import get_user_model
from django.db import models

User = get_user_model()

INGREDIENT_CHOICES = (
    ('кг', 'кг'),
    ('г', 'г'),
    ('мл', 'мл'),
    ('л', 'л'),
    ('ч. л.', 'ч. л.'),
    ('ст. л.', 'ст. л.'),
    ('шт.', 'шт.'),
    ('по вкусу', 'по вкусу'),
    ('стакан', 'стакан'),
    ('батон', 'батон'),
    ('кусок', 'кусок'),
    ('бутылка', 'бутылка'),
    ('пакетик', 'пакетик'),
    ('пучок', 'пучок'),
    ('лист', 'лист'),
)


class Tag(models.Model):
    title = models.CharField(max_length=20)
    color = models.CharField(max_length=20)
    slug = models.SlugField(unique=True)

    def __str__(self):
        return self.title


class Ingredient(models.Model):
    title = models.CharField(max_length=50)
    dimension = models.CharField(choices=INGREDIENT_CHOICES, max_length=10)

    def __str__(self):
        return self.title


class Recipe(models.Model):
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='recipes')
    title = models.CharField(max_length=50, unique=True)
    tags = models.ManyToManyField(
        Tag, related_name='recipes_tag')
    ingredients = models.ManyToManyField(
        Ingredient, through='IngredientValue', related_name='recipe_ing')
    cooking_time = models.PositiveSmallIntegerField(help_text='в минутах')
    text = models.TextField()
    image = models.ImageField(upload_to='media/')
    pub_date = models.DateTimeField(
        'Дата добавления', auto_now_add=True, db_index=True
    )

    class Meta:
        ordering = ('-pub_date',)

    def __str__(self):
        return self.title


class IngredientValue(models.Model):
    ingredient = models.ForeignKey(Ingredient, related_name='ingredient_values', on_delete=models.CASCADE, )
    recipe = models.ForeignKey(Recipe, related_name='recipe_values', on_delete=models.CASCADE)
    value = models.PositiveSmallIntegerField()

    def __str__(self):
        return str(self.value)
