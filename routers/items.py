from fastapi import APIRouter

router = APIRouter(
    prefix="/items",
    responses={404: {"description": "Not found"}}
)

test_db = {"items": [
    {
        "name": "Item 1",
        "price": 23.10
    },
    {
        "name": "Item 2",
        "price": 21.10
    },
    {
        "name": "Item 2",
        "price": 13.10
    },
]}

@router.get("/")
async def read_items():
    return test_db

@router.get("/{item_id}")
async def read_item():
    return "Reas {item_id} item"