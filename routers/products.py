import requests
from fastapi import APIRouter

router = APIRouter(
    prefix="/products",
    responses={404: {"description": "Not found"}}
)

test_db = {
    "products": [
        {
            "id": 1,
            "name": "Shirt",
            "price": 23.10,
            "category": "Men",
            "image" : ""
        },
        {
            "id": 2,
            "name": "Shirt",
            "price": 21.10,
            "category": "Women",
            "image": ""
        },
        {
            "id": 3,
            "name": "Item 2",
            "price": 13.10,
            "category": "Women",
            "image": ""
        }
    ]
}

@router.get("/")
async def read_products():
    return test_db["products"]

@router.get("/{product_id}")
async def read_product(product_id: int):
    return [product for product in test_db["products"] if product["id"] == product_id][0]