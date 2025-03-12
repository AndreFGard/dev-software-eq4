import os
import asyncio
from sqlalchemy import text
from dotenv import load_dotenv
from urllib.parse import urlparse
from sqlalchemy.ext.asyncio import create_async_engine

load_dotenv()

tmpPostgres = urlparse(os.getenv("DATABASE_URL"))

class Database:
    def __init__(self):
        self.engine = create_async_engine(
            f"postgresql+asyncpg://{tmpPostgres.username}:{tmpPostgres.password}@{tmpPostgres.hostname}{tmpPostgres.path}", 
            echo=True
        )

    async def create_table(self):
        try:
            async with self.engine.connect() as conn:
                query = text(
                    """
                        CREATE TABLE IF NOT EXISTS MESSAGES (
                            content_id SERIAL PRIMARY KEY, 
                            user_id INT,
                            content_message JSON,
                            role VARCHAR(255) NOT NULL,
                            FOREIGN KEY (user_id) REFERENCES USERS(user_id) ON DELETE CASCADE
                        );

                        CREATE TABLE IF NOT EXISTS USERS (
                            user_id SERIAL PRIMARY KEY, 
                            nome VARCHAR(255) NOT NULL,
                            senha VARCHAR(255) NOT NULL,
                            status VARCHAR(255) NOT NULL,
                            lista_favoritos JSON
                        );
                    """
                )

                await conn.execute(query)
                await conn.commit()
        except Exception as e:
            assert e

    async def add_data(self, target_table : str, data : dict):
        try:
            async with self.engine.connect() as conn:
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
            assert e

    async def read_data(self,target_table : str, conditions : dict):
        try:
            async with self.engine.connect() as conn:
                where_clause = " AND ".join([f"{key} = :{key}" for key in conditions.keys()])
                query = text(
                    f"""
                        SELECT * FROM {target_table} WHERE {where_clause}
                    """
                )
                result = await conn.execute(query, conditions or {})
                return result.fetchall()
            
        except Exception as e:
            assert e

    async def update_data(self, target_table : str, conditions : dict, data : dict):
        try:
            async with self.engine.connect() as conn:
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
            assert e

    async def delete_data(self, target_table : str, conditions : dict):
        try:
            async with self.engine.connect() as conn:
                where_clause = " AND ".join([f"{key} = :{key}" for key in conditions.keys()])
                query = text(
                    f"""
                        DELETE FROM {target_table} WHERE {where_clause}
                    """
                )
                await conn.execute(query, conditions or {})
                await conn.commit()
        except Exception as e:
            assert e

    async def async_main(self):
        try:
            await self.create_table()
            await self.engine.dispose()

        except Exception as e:
            assert e

if __name__ == "__main__":
    db = Database()
    asyncio.run(db.async_main())
