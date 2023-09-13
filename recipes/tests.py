from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from .models import Recipe
from .forms import RecipeSearch

# Create your tests here.


class RecipeModelTest(TestCase):
    def setUpTestData():
        Recipe.objects.create(name="Test Recipe", ingredients="Water, Ice",
                              cooking_time=5, description="Very awesome recipe description.")

    def test_return_string(self):
        recipe = Recipe.objects.get(id=1)
        self.assertEqual(recipe.__str__(), "Recipe: Test Recipe")

    def test_description(self):
        recipe = Recipe.objects.get(id=1)
        self.assertEqual(recipe.description,
                         "Very awesome recipe description.")

    def test_name_max_length(self):
        recipe = Recipe.objects.get(name="Test Recipe")
        max_length = recipe._meta.get_field('name').max_length
        self.assertEqual(max_length, 120)

    def test_ingredients_max_length(self):
        recipe = Recipe.objects.get(name="Test Recipe")
        max_length = recipe._meta.get_field('ingredients').max_length
        self.assertEqual(max_length, 512)

    def test_creator_null_true(self):
        recipe = Recipe.objects.get(name="Test Recipe")
        allow_null = recipe._meta.get_field("creator").null
        self.assertTrue(allow_null)

    def test_get_absolute_url(self):
        recipe = Recipe.objects.get(id=1)
        self.assertEqual(recipe.get_absolute_url(), "/recipes/list/1")


class RecipeFormTest(TestCase):
    def test_recipe_search_form_valid(self):
        form_data = {'recipe_name': 'Test Recipe'}
        form = RecipeSearch(data=form_data)
        self.assertTrue(form.is_valid())


class RecipeViewAccessTest(TestCase):
    def test_recipe_list_view_requires_login(self):
        url = reverse('recipes:list')
        response = self.client.get(url)
        # 302 is the HTTP status code for redirection (login required)
        self.assertEqual(response.status_code, 302)

    def test_recipe_search_view_requires_login(self):
        url = reverse('recipes:search')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 302)
