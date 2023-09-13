from django.db import models
from users.models import User
from django.shortcuts import reverse

# Create your models here.


class Recipe(models.Model):
    name = models.CharField(max_length=120)
    ingredients = models.CharField(max_length=512)
    cooking_time = models.IntegerField()
    description = models.TextField()
    creator = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    pic = models.ImageField(upload_to="recipes", default="no_image.jpg")

    def __str__(self):
        return f"Recipe: {self.name}"

    def get_absolute_url(self):
        return reverse("recipes:detail", kwargs={"pk": self.pk})

    def calculate_difficulty(self):
        num_of_ingredients = len(self.return_ingredients_as_list())

        if self.cooking_time < 10 and num_of_ingredients < 4:
            return "Easy"
        elif self.cooking_time < 10 and num_of_ingredients >= 4:
            return "Medium"
        elif self.cooking_time >= 10 and num_of_ingredients < 4:
            return "Intermediate"
        elif self.cooking_time >= 10 and num_of_ingredients >= 4:
            return "Hard"

    def return_ingredients_as_list(self):
        if self.ingredients == "":
            return []
        return self.ingredients.split(", ")

    def return_number_of_ingredients(self):
        return len(self.return_ingredients_as_list())
