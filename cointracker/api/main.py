import typing
from fastapi import FastAPI

from ..app.data import db
from ..app.address import models

app = FastAPI()


@app.on_event("startup")
async def startup():
    db.init()
    await db.conn.connect()


@app.on_event("shutdown")
async def shutdown():
    await db.conn.disconnect()


@app.get("/addresses/", response_model=typing.List[models.Address])
async def root():
    query = models.addresses.select()
    result = await db.conn.fetch_all(query)
    return result


@app.get("/addresses/{address}/")
async def root(address):
    return {"message": "Hello World"}


@app.get("/addresses/{address}/")
async def root(address):
    return {"message": "Hello World"}
