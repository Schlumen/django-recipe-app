from .models import Recipe
from io import BytesIO
import matplotlib.pyplot as plt
import base64


def get_graph():
    buffer = BytesIO()
    plt.savefig(buffer, format="png")
    buffer.seek(0)
    image_png = buffer.getvalue()
    graph = base64.b64encode(image_png)
    graph = graph.decode("utf-8")
    buffer.close()
    return graph


def get_chart(chart_type, data, **kwargs):
    plt.switch_backend("AGG")
    plt.figure(figsize=(6, 4))

    if chart_type == "bar":
        plt.bar(data["name"], data["nr_ingredients"])
        plt.xlabel("Recipes")
        plt.ylabel("Number of Ingredients")
        plt.xticks(rotation=45)
    elif chart_type == "pie":
        labels = kwargs.get("labels")
        plt.pie(data["count"], labels=labels, autopct='%1.1f%%')
    elif chart_type == "plot":
        plt.plot(data["name"], data["cooking_time"])
        plt.xticks(rotation=45)
        plt.xlabel("Recipes")
        plt.ylabel("Cooking Time")
    else:
        print("unknown chart type")

    plt.tight_layout()
    chart = get_graph()
    return chart
