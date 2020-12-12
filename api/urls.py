from django.urls import path

from . import views

urlpatterns = [
    path('ingredients/', views.IngredientAPIView.as_view(),
         name='api-ingredients'),
    path('favorites/', views.FavoriteAdd.as_view(), name='api-favorites'),
    path('favorites/<int:id>/', views.FavoriteDelete.as_view(),
         name='api-favorites-delete'),
    path('purchases/', views.PurchaseAdd.as_view(), name='api-purchases'),
    path('purchases/<int:id>/', views.PurchaseDelete.as_view(),
         name='api-purchases-delete'),
    path('subscriptions/', views.SubscribeAdd.as_view(),
         name='api-subscription'),
    path('subscriptions/<int:id>/', views.SubscribeDelete.as_view(),
         name='api-subscription-delete'),
]
