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

async def test_create_table(db: Database):
    await db.create_table()

    print("✅ Tabela criada com sucesso!")

async def test_insert_data(db: Database):
    # adicionando dados em users

    data = {
        "nome" : "Maria",
        "senha" : "123456",
        "status" : "ativo",
        "lista_favoritos" : json.dumps({
            "cidades" : ["São Paulo", "Rio de Janeiro"],
            "restaurantes" : ["Outback", "McDonald's"]
        })
    }

    # quando adicionar em users, usar o read para pegar o id e colocar na messagees

    await db.add_data("users", data)

    print("✅ Dados inseridos com sucesso!")

    # adicionando dados em messages

    data = {
        "user_id" : 1,
        "content_message" : json.dumps([
            {
                "content" : "Olá, tudo bem?",
                "date" : "2021-09-30 15:00:00",
                "role" : "bot"
            },
            {
                "content" : "Sim, e você?",
                "date" : "2021-09-30 15:01:00",
                "role" : "user"
            }
        ]),
        "role" : "aaaa"
    }

    await db.add_data("messages", data)

    print("✅ Dados inseridos com sucesso!")

async def test_read_data(db: Database):
    # lendo dados de users
    # testar ler algo especifico dentro da lista de favoritos

    resultado = await db.read_data("users", {"nome": "Maria"})
    assert resultado, "❌ Usuário não encontrado após inserção"

    print("✅ Leitura ok:", resultado)

    # lendo dados de messages
    resultado = await db.read_data("messages", {"user_id": 1})
    assert resultado, "❌ Mensagem não encontrada após inserção"

    print("✅ Leitura ok:", resultado)

async def test_update_data(db: Database):
    # atualizando dados de users

    await db.update_data(
        "users",
        conditions={"nome": "Maria"},
        data={"status": "inativo"}
    )

    print("✅ Atualização feita com sucesso")

    atualizado = await db.read_data("users", {"nome": "Maria", "status": "inativo"})
    assert atualizado, "❌ Atualização não refletida"

    print("✅ Verificação de update ok")

    # atualizando dados de messages

    await db.update_data(
        "messages",
        conditions={"user_id": 1},
        data={"role": "bbbb"}
    )

    print("✅ Atualização feita com sucesso")

    atualizado = await db.read_data("messages", {"role" : "bbbb"})
    assert atualizado, "❌ Atualização não refletida"

    print("✅ Verificação de update ok")

async def test_delete_data(db: Database):
    # deletando dados de users
    await db.delete_data("users", {"nome": "Maria"})
    print("✅ Deleção feita com sucesso")

    
    resultado_final = await db.read_data("users", {"nome": "Maria"})
    assert not resultado_final, "❌ Usuário ainda existe após delete"

    print("✅ Verificação de delete ok")

    # deletando dados de messages
    await db.delete_data("messages", {"user_id": 1})
    print("✅ Deleção feita com sucesso")

    resultado_final = await db.read_data("messages", {"user_id": 1})
    assert not resultado_final, "❌ Mensagem ainda existe após delete"

    print("✅ Verificação de delete ok")

async def test_main():
    db = Database()

    # await test_create_table(db)
    # await test_insert_data(db)

    # await test_read_data(db)

    # await test_update_data(db)
    # await test_delete_data(db)

    # todos os testes deram sucesso

    # testar dar update numa lista de favoritos
    # testar dar update numa lista de mensagens
    # testar dar update num item especifico de uma lista
    # testar deletar um item especifico de uma lista

    # adicionar funções reais de add, update, read e delete
    # colocar a que ja estao como funções privadas '__'

if __name__ == "__main__":
    asyncio.run(test_main())

# if __name__ == "__main__":
#     db = Database()
#     asyncio.run(db.async_main())