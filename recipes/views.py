from django.shortcuts import render
from django.views.generic import ListView, DetailView
from django.contrib.auth.decorators import login_required
from .models import Recipe
from .forms import RecipeSearch
from .utils import get_chart
from django.contrib.auth.mixins import LoginRequiredMixin
import pandas as pd

# Create your views here.


def home(request):
    return render(request, "recipes/recipes_home.html")


@login_required
def search(request):
    form = RecipeSearch(request.POST or None)
    recipes = None
    recipes_df = None
    chart1 = None
    chart2 = None
    chart3 = None

    if request.method == "POST":
        recipe_name = request.POST.get("recipe_name")
        qs = Recipe.objects.filter(name__icontains=recipe_name)

        if qs:
            recipes = qs
            recipes_df = pd.DataFrame(qs.values())

            # Chart 1
            chart1 = get_chart("plot", recipes_df)

            # Chart 2
            chart2_data = {
                "difficulty": ["Easy", "Medium", "Intermediate", "Hard"],
                "count": [0, 0, 0, 0]  # Initialize counts to zero
            }

            for recipe in recipes:
                difficulty = recipe.calculate_difficulty()
                if difficulty in chart2_data["difficulty"]:
                    index = chart2_data["difficulty"].index(difficulty)
                    chart2_data["count"][index] += 1

            # Filter out labels and counts with a count of 0
            filtered_labels = []
            filtered_counts = []
            for label, count in zip(chart2_data["difficulty"], chart2_data["count"]):
                if count > 0:
                    filtered_labels.append(label)
                    filtered_counts.append(count)

            # Create a new dictionary with filtered data
            filtered_chart2_data = {
                "difficulty": filtered_labels,
                "count": filtered_counts,
            }

            chart2 = get_chart("pie", filtered_chart2_data,
                               labels=filtered_labels)

            # Calculate data for Chart 3
            chart3_data = {
                # List of recipe names
                "name": [recipe.name for recipe in recipes],
                # List of ingredient counts
                "nr_ingredients": [recipe.return_number_of_ingredients() for recipe in recipes]
            }

            chart3 = get_chart("bar", chart3_data)

    context = {
        "form": form,
        "recipes": recipes,
        "chart1": chart1,
        "chart2": chart2,
        "chart3": chart3
    }

    return render(request, "recipes/search.html", context)


class RecipeListView(LoginRequiredMixin, ListView):
    model = Recipe
    template_name = "recipes/main.html"


class RecipeDetailView(LoginRequiredMixin, DetailView):
    model = Recipe
    template_name = "recipes/detail.html"
