import sqlalchemy as s
import pydantic

from ...app.data import db
from ...app.user import models as user

ID_LENGTH = 150

addresses = s.Table(
    "addresses",
    db.meta,
    s.Column("id", s.String(ID_LENGTH), primary_key=True),
    s.Column(
        "user_id", s.String(user.ID_LENGTH), s.ForeignKey("users.id"), nullable=False
    ),
)


class Address(pydantic.BaseModel):
    id: str
    user_id: str
