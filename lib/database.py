from typing import NamedTuple
from typing import Union, Any, List, Tuple
import asyncpg
import os
from pymongo import MongoClient, DESCENDING

import setting

MONGO_URL = setting.MONGO

User = NamedTuple('User', [('id', int), ('point', int), ('name', str)])



# user_id = 653785595075887104
# data = db.find_one({"user_id":user_id})
# print(data["point"])







class Database:
    """CREATE TABLE users (user_id bigint, point integer, name strings, PRIMARY KEY(user_id))"""

    def __init__(self, bot: Any):
        self.bot = bot
        self.conn: Union[asyncpg.Connection, None] = None
        self.db = None

    async def check_database(self) -> None:
        conn = self.conn or await self.setup()
        try:
            await conn.execute("select 'users'::regclass")
        except asyncpg.exceptions.UndefinedColumnError:
            await conn.execute("CREATE TABLE users (user_id bigint, point INT, name VARCHAR(45), PRIMARY KEY(user_id))")

    async def setup(self) -> asyncpg.Connection:
        client = MongoClient(MONGO_URL)
        self.db = client.users.user_id
        return self.db
        # self.conn = await asyncpg.connect(
        #     host = 'localhost',
        #     port = 5432,
        #     user=os.environ['POSTGRES_USER'],
        #     password=os.environ['POSTGRES_PASSWORD'],
        #     database=os.environ['POSTGRES_DB'],
        #     loop=self.bot.loop,
        # )
        # return self.conn

    # async def close(self) -> None:
    #     if self.dbt is not None:
    #         await self.db.close()
        # if self.conn is not None:
        #     await self.conn.close()

    async def get_user(self, user) -> Union[None, User]:
        db = self.db or await self.setup()
        data = db.find_one({"user_id":user.id})
        if not data:
            return None
        return User(data["user_id"], data["point"], data["name"])
        # conn = self.client or await self.setup()
        # data = await conn.fetch(f"SELECT * FROM users WHERE user_id={user.id}")
        # if not data:
        #     return None
        # target = list(data[0])
        # return User(target[0], target[1], target[2])


    async def get_user_rankings(self) -> List[Tuple[User, int]]:
        db = self.db or await self.setup()
        users_data = db.find(filter={"point":-1},sort=('point',DESCENDING)).limit(10)
        return [(User(user_data["user_id"], user_data["point"], user_data["name"])) for user_data in users_data]
        # conn = self.conn or await self.setup()
        # users_data = await conn.fetch("SELECT *, RANK() OVER(ORDER BY point DESC) AS rank FROM users LIMIT 10")
        # return [(User(user_data[0], user_data[1], user_data[2]), user_data[3]) for user_data in users_data]

    async def get_user_ranking(self, id: int) -> int:
        conn = self.conn or await self.setup()
        return await conn.fetchval(f"SELECT (SELECT COUNT(*) FROM users AS u WHERE u.point > users.point) + 1 FROM users WHERE user_id={id}")

    async def first_user(self, user) -> Union[None, User]:
        db = self.db or await self.setup()
        post = {"name":user.name,"user_id":user.id,"point": 0}
        db.insert_one(post)
        # conn = self.conn or await self.setup()
        # await conn.execute(f"INSERT INTO users (user_id, point, name) VALUES ({user.id}, 0, '{user.name}')")

    async def create_user(self, user) -> Union[None, User]:
        db = self.db or await self.setup()
        post = {"name":user.name,"user_id":user.id,"point": 1}
        db.insert_one(post)
        return await self.get_user(user)
        # conn = self.conn or await self.setup()
        # await conn.execute(f"INSERT INTO users (user_id, point, name) VALUES ({user.id}, 1, '{user.name}')")
        # return await self.get_user(user)

    async def add_point(self, user) -> Union[None, User]:
        db = self.db or await self.setup()
        data = db.find_one({"user_id":user.id})
        if not data:
            await self.create_user(user)
            return
        db.update_one({"user_id":user.id}, {"$set": {"point": data["point"] + 1}})
        return

        # conn = self.conn or await self.setup()
        # data = await conn.fetch(f"SELECT * FROM users WHERE user_id={user.id}")
        # if not data:
        #     await self.create_user(user)
        #     return
        # await conn.execute(f"UPDATE users SET point = point + 1 WHERE user_id = {user.id}")
        # return

    async def reset(self):
        client = MongoClient(MONGO_URL)
        db = client.users
        db.drop_collection(db.user_id)

        # conn = self.conn or await self.setup()
        # await conn.execute("drop table users")
        # await conn.execute("CREATE TABLE users (user_id bigint, point INT, name VARCHAR(45), PRIMARY KEY(user_id))")


    # async def update_user(self, user_id: int, point: int) -> Union[None, User]:
    #     conn = self.conn or await self.setup()
    #     await conn.execute(f"UPDATE users SET point = {point} WHERE user_id = {user_id}")
    #     return await self.get_user(user_id)
