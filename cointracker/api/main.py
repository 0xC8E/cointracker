import typing
from fastapi import FastAPI

from ..app.data import db
from ..app.address import models as address
from ..app.transaction import models as transaction

app = FastAPI()


@app.on_event("startup")
async def startup():
    db.init()
    await db.conn.connect()


@app.on_event("shutdown")
async def shutdown():
    await db.conn.disconnect()


@app.get("/addresses/", response_model=typing.List[address.Address])
async def root():
    query = address.addresses.select()
    result = await db.conn.fetch_all(query)
    return result


@app.get("/addresses/{address_id}/", response_model=address.Address)
async def root(address_id):
    query = address.addresses.select().where(address.addresses.c.id == address_id)
    result = await db.conn.fetch_one(query)
    return result


@app.get(
    "/addresses/{address_id}/transactions/",
    response_model=typing.List[transaction.Transaction],
)
async def root(address_id):
    query = transaction.transactions.select().where(
        transaction.transactions.c.address_id == address_id
    )
    result = await db.conn.fetch_all(query)
    return result
