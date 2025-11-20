from fastapi import FastAPI, Request
from typing import Union
from pydantic import BaseModel

class Product(BaseModel):
    name: str
    price: float

app = FastAPI()

@app.get("/")
def hello_world():
    return {"message": "Hello, World!!"}

@app.get("/users/{user_id}")
def read_user(user_id: int, query_string: Union[str, None] = None):
    return {"user_id": user_id, "query_string": query_string}

@app.post("/user")
async def create_user(request: Request):
    body = await request.json()
    print('log:name', body["name"])
    return {"user": body}

@app.post("/product")
def create_product(product: Product):
    print('log:name', product.name)
    return {"product": product}

@app.put("/product/{product_id}")
def update_product(product_id: int, product: Product):
    return {"id": product_id, "product": product}

@app.delete("/product/{product_id}")
def delete_product(product_id: int):
    return {"message": f"Product with id {product_id} has been deleted"}