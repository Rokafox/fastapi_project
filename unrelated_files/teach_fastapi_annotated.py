from typing import Annotated

from fastapi import FastAPI, Query

app = FastAPI()

"""
FastAPI allows you to declare additional information and validation for your parameters.
q: str | None = None
is the same as:
q: Annotated[str | None] = None
Enforcing a maximum length for a query parameter, no longer than 50 characters:
"""

@app.get("/items/")
async def read_items(q: Annotated[str | None, Query(max_length=50)] = None):
    results = {"items": [{"item_id": "Foo"}, {"item_id": "Bar"}]}
    if q:
        results.update({"q": q})
    return results


"""
You can also add a parameter min_length:
q: Annotated[str | None, Query(min_length=3, max_length=50)] = None,
You can define a regular expression pattern that the parameter should match:
q: Annotated[str | None, Query(regex="^fixedquery$")] = None,

You can, of course, use default values other than None.
Let's say that you want to declare the q query parameter to have a min_length of 3, and to have a default value of "fixedquery":
async def read_items(q: Annotated[str, Query(min_length=3)] = "fixedquery"):

when you need to declare a value as required while using Query, you can simply not declare a default value:
async def read_items(q: Annotated[str, Query(min_length=3)]):
"""