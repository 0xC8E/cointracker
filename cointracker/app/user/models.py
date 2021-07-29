import sqlalchemy
import uuid

from cointracker.app.data import db

ID_LENGTH = 36
EMAIL_LENGTH = 150


users = sqlalchemy.Table(
    "users",
    db.meta,
    sqlalchemy.Column(
        "id", sqlalchemy.String(ID_LENGTH), primary_key=True, default=uuid.uuid4
    ),
    sqlalchemy.Column("email", sqlalchemy.String(EMAIL_LENGTH)),
)
