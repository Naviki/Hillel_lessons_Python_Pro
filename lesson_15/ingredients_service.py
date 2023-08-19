from sanic import Sanic, response

app_ingredients = Sanic("ingredients_service")

ingredients_data = {
    "flour": 1000,
    "sugar": 500,
    "yeast": 100,
}


@app_ingredients.route("/ingredients", methods=["GET"])
async def get_ingredients(_request):
    return response.json(ingredients_data)

if __name__ == "__main__":
    app_ingredients.run(host="0.0.0.0", port=8001)
