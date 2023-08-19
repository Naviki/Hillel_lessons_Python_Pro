from sanic import Sanic, response
import httpx

app_buns = Sanic("buns_service")

ingredients_service_url = "http://localhost:8001/ingredients"


async def calculate_buns():
    async with httpx.AsyncClient() as client:
        ingredients_response = await client.get(ingredients_service_url)
        ingredients = ingredients_response.json()

    flour_amount = ingredients.get("flour", 0)
    sugar_amount = ingredients.get("sugar", 0)
    yeast_amount = ingredients.get("yeast", 0)

    buns_possible = min(flour_amount // 200, sugar_amount // 50, yeast_amount // 10)
    return buns_possible


@app_buns.route("/calculate_buns", methods=["GET"])
async def get_buns(_request):
    buns_count = await calculate_buns()
    return response.json({"buns_possible": buns_count})

if __name__ == "__main__":
    app_buns.run(host="0.0.0.0", port=8002)
