from typing import List
from pydantic import BaseModel

class Product(BaseModel):
    id: int
    name: str
    price: float
    category: str
    image: str

class Products(BaseModel):
    products: List[Product]