from os import environ
from asyncpg.connection import connect
from asyncpg import Connection
import asyncio


async def setup_database():
    connection: Connection = await connect(
        host=environ.get('DBHOST'),
        port=environ.get('DBPORT'),
        user=environ.get('DBUSER'),
        password=environ.get('DBPASS'),
        database=environ.get('DBNAME'),
    )
