from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('new/', views.new_recipe, name='new-recipe'),
    path('shopping_list/', views.download_purchases, name='shopping-list'),
    path('subscriptions/', views.subscriptions, name='subscriptions'),
    path('favorites/', views.favorites, name='favorites'),
    path('purchases/', views.get_purchases, name='purchases'),
    path('purchases/<int:purchase_id>/delete', views.purchase_delete,
         name='purchase-delete'),
    path('<str:username>/', views.profile, name='profile'),
    path('<str:username>/<int:recipe_id>/', views.recipe_view,
         name='recipe-view'),
    path('<str:username>/<int:recipe_id>/delete/', views.recipe_delete,
         name='recipe-delete'),
    path('<str:username>/<int:recipe_id>/edit/', views.recipe_edit,
         name='recipe-edit'),
]
