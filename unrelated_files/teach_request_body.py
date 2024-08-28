from fastapi import FastAPI
from pydantic import BaseModel

"""
When you need to send data from a client (let's say, a browser) to your API, you send it as a request body.
A request body is data sent by the client to your API. A response body is the data your API sends to the client.
Your API almost always has to send a response body. But clients don't necessarily need to send request bodies all the time, 
sometimes they only request a path, maybe with some query parameters, but don't send a body.
To declare a request body, you use Pydantic models with all their power and benefits.
To send data, you should use one of: POST (the more common), PUT, DELETE or PATCH.
"""


class Item(BaseModel):
    name: str
    description: str | None = None
    price: float
    tax: float | None = None
    
    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "name": "Foo",
                    "description": "A very nice Item",
                    "price": 35.4,
                    "tax": 3.2,
                }
            ]
        }
    }


app = FastAPI()


@app.put("/items/{item_id}")
async def update_item(item_id: int, item: Item, q: str | None = None):
    result = {"item_id": item_id, **item.model_dump()}
    if q:
        result.update({"q": q})
    return result

"""
Test this endpoint with API docs: http://127.0.0.1:8000/docs 
You can try sending a request with a JSON body like:
{
  "name": "dog",
  "description": "animal",
  "price": 30,
  "tax": 77
}
"""