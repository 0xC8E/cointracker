import datetime
import decimal
import sqlalchemy as s
import pydantic
from sqlalchemy import func as f


from ...app.data import db
from ...app.address import models as address

ID_LENGTH = 150
TYPE_LENGTH = 30
PRECISION = 200
SCALE = 100

transactions = s.Table(
    "transactions",
    db.meta,
    s.Column("id", s.String(ID_LENGTH), primary_key=True),
    s.Column(
        "address_id",
        s.String(address.ID_LENGTH),
        s.ForeignKey("addresses.id"),
        nullable=False,
    ),
    s.Column("transaction_type", s.String(TYPE_LENGTH), nullable=False),
    s.Column("amount", s.DECIMAL(precision=PRECISION, scale=SCALE), nullable=False),
    s.Column(
        "created_at",
        s.DateTime(timezone=True),
        nullable=False,
        default=f.now(),
    ),
    s.Column(
        "updated_at",
        s.DateTime(timezone=True),
        nullable=False,
        default=f.now(),
        onupdate=f.now(),
    ),
)


class Transaction(pydantic.BaseModel):
    id: str
    address_id: str
    transaction_type: str
    amount: decimal.Decimal
    created_at: datetime.datetime
    updated_at: datetime.datetime
