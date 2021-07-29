import asyncio
import decimal
import random
import uuid

from cointracker.app.data import db
from cointracker.app.address import models as address
from cointracker.app.user import models as user
from cointracker.app.transaction import models as transaction

btc_addresses = [
    "34xp4vRoCGJym3xR7yCVPFHoCNxv4Twseo",
    "bc1qgdjqv0av3q56jvd82tkdjpy7gdp9ut8tlqmgrpmv24sq90ecnvqqjwvw97	",
    "1P5ZEDWTKTFGxQjZphgWPQUpe554WKDfHQ	",
    "37XuVSEpWW4trkfmvWzegTHQt7BdktSKUs	",
    "38UmuUqPCrFmQo4khkomQwZ4VbY2nZMJ67	",
    "1FeexV6bAHb8ybZjqQMjJrcCrHGW9sb6uF	",
    "35hK24tcLEWcgNA4JxpvbkNkoAcDGqQPsP	",
    "3LYJfcfHPXYJreMsASk2jkn69LWEYKzexb	",
    "bc1qa5wkgaew2dkv56kfvj49j0av5nml45x9ek9hz6	",
    "3Kzh9qAqVWQhEsfQz7zEQL1EuSx5tyNLNS	",
    "3LQeSjqS5aXJVCDGSHPR88QvjheTwrhP8N	",
    "1LdRcdxfbSnmCYYNdeYpUnztiYzVfBEQeC	",
    "1AC4fMwgY8j9onSbXEWeH6Zan8QGMSdmtA	",
    "1LruNZjwamWJXThX2Y8C2d47QqhAkkc5os	",
    "3Gpex6g5FPmYWm26myFq7dW12ntd8zMcCY	",
    "385cR5DM96n1HvBDMzLHPYcw89fZAXULJP	",
    "bc1q5shngj24323nsrmxv99st02na6srekfctt30ch	",
    "36KAwNUR8VeLpUfGwdk7LEN6F4yvoRWMjn	",
    "3D8qAoMkZ8F1b42btt2Mn5TyN7sWfa434A	",
    "bc1q7ydrtdn8z62xhslqyqtyt38mm4e2c4h3mxjkug	",
    "3EBpAZUAW5Tzyd2FhmmUZnYgftxJkKSLmJ	",
    "3LCGsSmfr24demGvriN4e3ft8wEcDuHFqh	",
    "12XqeqZRVkBDgmPLVY4ZC6Y4ruUUEug8Fx	",
    "3FHNBLobJnbCTFTVakh5TXmEneyf5PT61B	",
    "12ib7dApVFvg82TXKycWBNpN8kFyiAN1dr	",
    "bc1q5pucatprjrqltdp58f92mhqkfuvwpa43vhsjwpxlryude0plzyhqjkqazp	",
    "12tkqA9xSoowkzoERHMWNKsTey55YEBqkv	",
    "17MWdxfjPYP2PYhdy885QtihfbW181r1rn	",
    "3FpYfDGJSdkMAvZvCrwPHDqdmGqUkTsJys	",
    "19D5J8c59P2bAkWKvxSYw8scD3KUNWoZ1C",
]


async def clear_data():
    await db.conn.execute(transaction.transactions.delete())
    await db.conn.execute(address.addresses.delete())
    await db.conn.execute(user.users.delete())


async def insert_data():
    for a in btc_addresses:
        uid = uuid.uuid4()
        u_query = user.users.insert().values(
            id=str(uid), email=f"{uid.hex}@example.com"
        )
        a_query = address.addresses.insert().values(id=a, user_id=str(uid))
        await db.conn.execute(u_query)
        await db.conn.execute(a_query)

        transaction_queries = []
        for _ in range(10):
            amount = decimal.Decimal(random.randrange(150, 400)) / 100
            transaction_type = random.choice(["in", "out"])
            t_query = transaction.transactions.insert().values(
                id=str(uuid.uuid4()),
                address_id=a,
                transaction_type=transaction_type,
                amount=amount,
            )
            transaction_queries.append(db.conn.execute(t_query))

        await asyncio.gather(*tuple(transaction_queries))


async def run():
    db.init()
    await db.conn.connect()
    await clear_data()
    await insert_data()
    await db.conn.disconnect()


asyncio.run(run())
