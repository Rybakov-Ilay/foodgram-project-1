from django.shortcuts import get_object_or_404
from rest_framework import filters, generics
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from main.models import Ingredient, Recipe, User

from .models import Favorite, Purchase, Subscribe
from .serializers import (FavoriteSerializer, IngredientSerializer,
                          PurchaseSerializer, SubscribeSerializer)


class CreateResponseMixin:
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            self.perform_create(serializer)
            return Response({'success': True})
        return Response({'success': False})


class IngredientAPIView(generics.ListAPIView):
    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['^title', ]


class FavoriteAdd(CreateResponseMixin, generics.CreateAPIView):
    queryset = Favorite.objects.all()
    serializer_class = FavoriteSerializer
    permission_classes = [IsAuthenticated]


class FavoriteDelete(APIView):
    permission_classes = [IsAuthenticated]

    def delete(self, request, id):
        recipe = get_object_or_404(Recipe, id=id)
        favorite = recipe.recipe_favorite.filter(user=request.user)
        if favorite.delete():
            return Response({'success': True})
        return Response({'success': False})


class PurchaseAdd(CreateResponseMixin, generics.CreateAPIView):
    queryset = Purchase.objects.all()
    serializer_class = PurchaseSerializer
    permission_classes = [IsAuthenticated]


class PurchaseDelete(APIView):

    def delete(self, request, id):
        recipe = get_object_or_404(Recipe, id=id)
        purchase = recipe.recipe_purchase.filter(user=request.user)
        if purchase.delete():
            return Response({'success': True})
        return Response({'success': False})


class SubscribeAdd(CreateResponseMixin, generics.CreateAPIView):
    queryset = Subscribe.objects.all()
    serializer_class = SubscribeSerializer
    permission_classes = [IsAuthenticated]


class SubscribeDelete(APIView):
    permission_classes = [IsAuthenticated]

    def delete(self, request, id):
        author = get_object_or_404(User, id=id)
        subscribe = author.following.filter(user=request.user)
        if subscribe.delete():
            return Response({'success': True})
        return Response({'success': False})
