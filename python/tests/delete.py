from enum import Enum
from typing import Annotated

from fastapi import FastAPI, Query, Path, Cookie
from pydantic import BaseModel, Field, HttpUrl
from uuid import UUID

app = FastAPI()


class PossibleParams(int, Enum):
    val_1 = 10
    val_2 = 20


class Image(BaseModel):
    url: HttpUrl
    name: str


class Item(BaseModel):
    name: str
    price: float
    description: str | None = Field(
        default=None,
        title="The item description",
        max_length=300
    )
    tags: set[str] = set()
    image: Image | None = None


class Offer(BaseModel):
    name: str
    description: str | None = None
    price: float
    items: list[Item]


class User(BaseModel):
    username: str
    full_name: str | None = None


@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.get("/test-func/")
def test_func(a: PossibleParams) -> int:
    return a**2


@app.post("/create_item/")
def create_item(item: Item) -> Item:
    return item


@app.get("/items/{item_id}")
async def read_items(
        item_id: Annotated[UUID, Path(title="The ID of the item", ge=1)],
        q: Annotated[list[str] | None, Query(
            max_length=50,
            title="Some Title",
            description="Some Description",
            deprecated=True,
        )] = None,
        ads_id: Annotated[str | None, Cookie()] = None
):
    results = {"item_id": item_id}
    if q:
        results.update({"q": q})
    if ads_id:
        results.update({"ads_id": ads_id})
    return results


@app.put("/items/{item_id}")
async def update_item(
        item_id: int,
        item: Item,
        user: User,
):
    results = {
        "item_id": item_id,
        "item": item,
        "user": user
    }
    return results


@app.post("/offers/")
async def create_offer(offer: Offer):
    return offer

