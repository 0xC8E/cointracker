import sqlalchemy as s

from ...app.data import db
from ...app.user import user

ID_LENGTH = 150

addresses = s.Table('addresses', db.meta,
    s.Column('id', s.String(ID_LENGTH), primary_key=True),
    s.Column('user_id', s.String(user.ID_LENGTH), s.ForeignKey("users.id"), nullable=False),
)