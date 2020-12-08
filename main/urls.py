from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('new/', views.new_recipe, name= 'new-recipe'),
    path('<str:username>/', views.profile, name='profile'),
    path('<str:username>/<int:recipe_id>/', views.recipe_view, name='recipe-view'),
    path('<str:username>/<int:recipe_id>/delete/', views.recipe_delete, name='recipe-delete'),
    path('<str:username>/<int:recipe_id>/edit/', views.recipe_edit, name='recipe-edit'),
    path('subscriptions', views.subscriptions, name='subscriptions'),
    path('favourites', views.favourites, name='favourites'),
    path('purchases', views.purchases_list, name='purchases'),
    path('purchases/<int:purchase_id>/delete', views.purchase_delete, name='purchase-delete'),
]