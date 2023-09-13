from django import forms


class RecipeSearch(forms.Form):
    recipe_name = forms.CharField(max_length=120)
