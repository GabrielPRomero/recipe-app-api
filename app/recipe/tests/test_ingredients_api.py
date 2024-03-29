from django.contrib.auth import get_user_model
from django.urls import reverse
from django.test import TestCase

from rest_framework import status
from rest_framework.test import APIClient

from core.models import Ingredient
from recipe.serializers import IngredientSerializer

INGREDIENT_URL = reverse('recipe:ingredient-list')


class PublicIngredientsApiTests(TestCase):
    """test publicly available ingredients api"""

    def setUp(self):
        self.client = APIClient()

    def test_login_required(self):
        """test that login is required"""
        res = self.client.get(INGREDIENT_URL)

        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


class PrivateIngredientsApiTests(TestCase):
    """test private ingredients api"""

    def setUp(self):
        self.user = get_user_model().objects.create_user(
            'test@test.com', 'testpass')
        self.client = APIClient()
        self.client.force_authenticate(self.user)
        
    def test_retrieve_ingredient_list(self):
        """test retrieving a list of ingredients"""
        Ingredient.objects.create(user=self.user, name='Kale')
        Ingredient.objects.create(user=self.user, name='Salt')

        res = self.client.get(INGREDIENT_URL)

        ingredients = Ingredient.objects.all().order_by('-name')
        serializer = IngredientSerializer(ingredients, many=True)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)
    
    def test_ingredients_limited_to_user(self):
        """test that ingredients returned are for the authenticated user"""
        user2 = get_user_model().objects.create_user(
            'testdjdj@test.com', 'testpass')
        Ingredient.objects.create(user=user2, name='Vinegar')
        
        ingredient = Ingredient.objects.create(user=self.user, name='Tumeric')
        
        res = self.client.get(INGREDIENT_URL)
        
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(len(res.data), 1)
        self.assertEqual(res.data[0]['name'], ingredient.name)
        
    def test_create_ingredient_successful(self):
        """test create a new ingredient"""
        payload = {'name': 'Cabbage'}
        self.client.post(INGREDIENT_URL, payload)

        exists = Ingredient.objects.filter(
            user=self.user,
            name=payload['name']
        ).exists()
        self.assertTrue(exists)
        
    def test_create_ingredient_invalid(self):
        """test creating invalid ingredient fails"""
        payload = {'name': ''}
        res = self.client.post(INGREDIENT_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
