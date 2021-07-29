import fastapi
import sqlalchemy
import typing


from ..app.data import db
from ..app.address import models as address
from ..app.transaction import models as transaction

app = fastapi.FastAPI()


@app.on_event("startup")
async def startup():
    db.init()
    await db.conn.connect()


@app.on_event("shutdown")
async def shutdown():
    await db.conn.disconnect()


@app.get("/addresses/", response_model=typing.List[address.Address])
async def list_addresses():
    query = address.addresses.select()
    result = await db.conn.fetch_all(query)
    return result


@app.post("/addresses/", response_model=address.Address, status_code=201)
async def create_address(address_request: address.AddressRequest = fastapi.Body(...)):
    query = (
        address.addresses.insert()
        .values(
            id=address_request.id,
            user_id=address_request.user_id,
        )
        .returning(sqlalchemy.text("*"))
    )
    created_address = await db.conn.fetch_one(query)

    return created_address


@app.get("/addresses/{address_id}/", response_model=address.Address)
async def get_address(address_id):
    query = address.addresses.select().where(address.addresses.c.id == address_id)
    result = await db.conn.fetch_one(query)
    return result


@app.get(
    "/addresses/{address_id}/transactions/",
    response_model=typing.List[transaction.Transaction],
)
async def get_transactions(address_id):
    query = transaction.transactions.select().where(
        transaction.transactions.c.address_id == address_id
    )
    result = await db.conn.fetch_all(query)
    return result
