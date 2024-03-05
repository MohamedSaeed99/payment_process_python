import requests
from fastapi import APIRouter

router = APIRouter(
    prefix="/products",
    responses={404: {"description": "Not found"}}
)

@router.get("/")
async def read_items():
    return requests.get('https://fakestoreapi.com/products').json()

@router.get("/{item_id}")
async def read_item(item_id: int):
    return requests.get(f'https://fakestoreapi.com/products/{item_id}').json()