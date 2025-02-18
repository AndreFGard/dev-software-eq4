import os
import asyncio
from sqlalchemy import text
from dotenv import load_dotenv
from urllib.parse import urlparse
from sqlalchemy.ext.asyncio import create_async_engine

load_dotenv()

tmpPostgres = urlparse(os.getenv("DATABASE_URL"))

engine = create_async_engine(
    f"postgresql+asyncpg://{tmpPostgres.username}:{tmpPostgres.password}@{tmpPostgres.hostname}{tmpPostgres.path}", 
    echo=True
)

async def create_table():
    pass

async def add_data(target_table : str, data : dict):
    try:
        async with engine.connect() as conn:
            columns = ", ".join(data.keys())
            values = ", ".join([f":{key}" for key in data.keys()])
            query = text(
                f"""
                    INSERT INTO {target_table} ({columns}) VALUES ({values})
                """
            )

            await conn.execute(query)
            await conn.commit()

    except Exception as e:
        print(e)

async def read_data(target_table : str, conditions : dict):
    try:
        async with engine.connect() as conn:
            where_clause = " AND ".join([f"{key} = :{key}" for key in conditions.keys()])
            query = text(
                f"""
                    SELECT * FROM {target_table} WHERE {where_clause}
                """
            )
            result = await conn.execute(query, conditions or {})
            return result.fetchall()
        
    except Exception as e:
        print(e)

async def update_data(target_table : str, conditions : dict, data : dict):
    try:
        async with engine.connect() as conn:
            where_clause = " AND ".join([f"{key} = :{key}" for key in conditions.keys()])
            data_string = ", ".join([f"{key} = :{key}" for key in data.keys()])
            query = text(
                f"""
                    UPDATE {target_table} SET {data_string} WHERE {where_clause}
                """
            )
            params = {**conditions, **data}
            await conn.execute(query, params)
            await conn.commit()
    except Exception as e:
        print(e)

async def delete_data(yable_table : str, conditions : dict):
    try:
        async with engine.connect() as conn:
            where_clause = " AND ".join([f"{key} = :{key}" for key in conditions.keys()])
            query = text(
                f"""
                    DELETE FROM {yable_table} WHERE {where_clause}
                """
            )
            await conn.execute(query, conditions or {})
            await conn.commit()
    except Exception as e:
        print(e)

async def async_main():
    try:
        async with engine.connect() as conn:
            result = await conn.execute(text("select 'hello world'"))
            print(result.fetchall())

        await engine.dispose()

    except Exception as e:
        print(e)

asyncio.run(async_main())