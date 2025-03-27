import os
import asyncio
import json
from typing import Optional
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
            async with self.engine.begin() as conn:
                await conn.execute(text("""
                    CREATE TABLE IF NOT EXISTS USERS (
                        user_id SERIAL PRIMARY KEY, 
                        nome VARCHAR(255) NOT NULL,
                        senha VARCHAR(255) NOT NULL,
                        status VARCHAR(255) NOT NULL,
                        lista_favoritos JSON
                    );
                """))

                await conn.execute(text("""
                    CREATE TABLE IF NOT EXISTS MESSAGES (
                        content_id SERIAL PRIMARY KEY, 
                        user_id INT,
                        content_message JSON,
                        role VARCHAR(255) NOT NULL,
                        FOREIGN KEY (user_id) REFERENCES USERS(user_id) ON DELETE CASCADE
                    );
                """)) # talvez tirar o role

        except Exception as e:
            print("❌ Erro ao criar tabelas:", e)

    async def add_data(self, target_table: str, data: dict):
        try:
            async with self.engine.begin() as conn:
                columns = ", ".join(data.keys())
                values = ", ".join([f":{key}" for key in data.keys()])
                query = text(f"""
                    INSERT INTO {target_table} ({columns}) 
                    VALUES ({values})
                """)
                await conn.execute(query, data)

        except Exception as e:
            print(f"❌ Erro ao inserir dados em {target_table}:", e)

    async def read_data(self, target_table: str, conditions: Optional[dict]=None):
        try:
            async with self.engine.begin() as conn:
                if conditions:
                    where_clause = " AND ".join([f"{key} = :{key}" for key in conditions])
                    query = text(f"SELECT * FROM {target_table} WHERE {where_clause}")
                    result = await conn.execute(query, conditions)
                else:
                    query = text(f"SELECT * FROM {target_table}")
                    result = await conn.execute(query)

                return result.fetchall()
            
        except Exception as e:
            print(f"❌ Erro ao ler dados de {target_table}:", e)
            return []

    async def update_data(self, target_table: str, conditions: dict, data: dict):
        try:
            async with self.engine.begin() as conn:
                set_clause = ", ".join([f"{key} = :{key}" for key in data])
                where_clause = " AND ".join([f"{key} = :cond_{key}" for key in conditions])
                query = text(f"""
                    UPDATE {target_table} 
                    SET {set_clause} 
                    WHERE {where_clause}
                """)

                params = {**data, **{f"cond_{k}": v for k, v in conditions.items()}}
                await conn.execute(query, params)

        except Exception as e:
            print(f"❌ Erro ao atualizar dados em {target_table}:", e)

    async def delete_data(self, target_table: str, conditions: dict):
        try:
            async with self.engine.begin() as conn:
                where_clause = " AND ".join([f"{key} = :{key}" for key in conditions])
                query = text(f"""
                    DELETE FROM {target_table} 
                    WHERE {where_clause}
                """)
                await conn.execute(query, conditions)

        except Exception as e:
            print(f"❌ Erro ao deletar dados de {target_table}:", e)

    async def async_main(self):
        try:
            await self.create_table()
            await self.engine.dispose()

        except Exception as e:
            print(f"❌ Erro: {e}")