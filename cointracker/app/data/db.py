import sqlalchemy
import databases

DATABASE_URI = "postgres://postgres:postgres@localhost:5432"


def init():
    engine = sqlalchemy.create_engine(
        DATABASE_URI,
    )
    meta.create_all(engine)


meta = sqlalchemy.MetaData()
conn = databases.Database(DATABASE_URI)
