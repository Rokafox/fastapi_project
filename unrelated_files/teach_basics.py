from fastapi import FastAPI
from enum import Enum

app = FastAPI()


# Basic example
@app.get("/") # Can use any HTTP method (get, post, put, delete, etc.)
async def root(): # Path operation function
    return {"message": "Hello World"}
"""
You can return a dict, list, singular values as str, int, etc.
You can also return Pydantic models (you'll see more about that later).
There are many other objects and models that will be automatically converted to JSON (including ORMs, etc). 
Try using your favorite ones, it's highly probable that they are already supported.
"""

# Path Parameters example
@app.get("/dogs/{dog_id}")
async def read_item(dog_id):
    return {"dog_id": dog_id}

# Enum is a class in Python for creating enumerations, which are a set of symbolic names (members) bound to unique, constant values.
class ModelName(str, Enum):
    alexnet = "alexnet"
    resnet = "resnet"
    lenet = "lenet"

@app.get("/models/{model_name}")
async def get_model(model_name: ModelName):
    if model_name is ModelName.alexnet:
        return {"model_name": model_name, "message": "Deep Learning FTW!"}

    if model_name.value == "lenet":
        return {"model_name": model_name, "message": "LeCNN all the images"}

    return {"model_name": model_name, "message": "Have some residuals"}


@app.get("/files/{file_path:path}")
# In this case, the name of the parameter is file_path, and the last part, :path, tells it that the parameter should match any path.
async def read_file(file_path: str):
    return {"file_path": file_path}


# Query Parameters example
fake_items_db = [{"item_name": "Foo"}, {"item_name": "Bar"}, {"item_name": "Baz"}, {"item_name": "Qux"}, {"item_name": "Quux"}]
@app.get("/items/")
async def read_item(skip: int = 0, limit: int = 10):
    return fake_items_db[skip : skip + limit]



"""
Multiple path and query parameters example with optional query parameters 

If we need additional validation for optional parameters, see here: https://fastapi.tiangolo.com/tutorial/query-params-str-validations/
In the same way that you can declare more validations and metadata for query parameters with Query, 
you can declare the same type of validations and metadata for path parameters with Path.
see here: https://fastapi.tiangolo.com/tutorial/path-params-numeric-validations/
"""
@app.get("/users/{user_id}/items/{item_id}")
async def read_user_item(
    user_id: int, item_id: str, q: str | None = None, short: bool = False 
):
    item = {"item_id": item_id, "owner_id": user_id}
    if q:
        item.update({"q": q})
    if not short:
        item.update(
            {"description": "This is an amazing item that has a long description"}
        )
    return item


# Required query parameters example
# In previous example, q and short are optional query parameters. If you want to make them required, you can remove the default values.
@app.get("/coyote/{coyote_id}")
async def read_user_item(coyote_id: str, needy: str):
    item = {"coyote_id": coyote_id, "needy": needy}
    return item
