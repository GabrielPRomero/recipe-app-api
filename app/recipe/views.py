from rest_framework import viewsets, mixins
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated

from core.models import Tag, Ingredient, Recipe

from recipe import serializers

class BaseRecipeAttrViewSet(viewsets.GenericViewSet, mixins.ListModelMixin, mixins.CreateModelMixin):
    """Base viewset for user owned recipe attributes"""
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)
    
    def get_queryset(self):
        """return objects for the current authenticated user only"""
        return self.queryset.filter(user=self.request.user).order_by('-name')
    
    def perform_create(self, serializer):
        """create a new tag"""
        serializer.save(user=self.request.user)

    

class TagViewSet(BaseRecipeAttrViewSet):
    """manage tags in the db"""
    serializer_class = serializers.TagSerializer
    queryset = Tag.objects.all()
    
    
class IngredientViewSet(BaseRecipeAttrViewSet):
    """manage ingredients in the db"""
    serializer_class = serializers.IngredientSerializer
    queryset = Ingredient.objects.all()
    
class RecipeViewSet(viewsets.ModelViewSet):
    """manage recipes in the db"""
    serializer_class = serializers.RecipeSerializer
    queryset = Recipe.objects.all()
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)
    
    def get_queryset(self):
        """retrieve the recipes for the authenticated user"""
        return self.queryset.filter(user=self.request.user)
    
    def perform_create(self, serializer):
        """create a new recipe"""
        serializer.save(user=self.request.user)
        
   
 
    