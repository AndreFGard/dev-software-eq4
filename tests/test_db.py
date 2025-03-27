from database.connection import Database
import asyncio

async def test_create_table(db: Database):
    await db.create_table()

    print("✅ Tabela criada com sucesso!")

async def test_insert_data(db: Database):
    # adicionando dados em usuarios

    data = {
        "nome" : "Maria",
        "senha" : "123456",
        "status" : "ativo",
        "lista_favoritos" : {
            "cidades" : ["São Paulo", "Rio de Janeiro"],
            "restaurantes" : ["Outback", "McDonald's"]
        }
    }

    await db.add_data("usuarios", data)

    print("✅ Dados inseridos com sucesso!")

    # adicionando dados em mensagens

    data = {
        "user_id" : 1,
        "content_message" : [
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
        ],
        "role" : "aaaa"
    }

    await db.add_data("mensagens", data)

    print("✅ Dados inseridos com sucesso!")

async def test_read_data(db: Database):
    # lendo dados de usuarios

    resultado = await db.read_data("users", {"nome": "Maria"})
    assert resultado, "❌ Usuário não encontrado após inserção"

    print("✅ Leitura ok:", resultado)

    # lendo dados de mensagens
    resultado = await db.read_data("messages", {"user_id": 1})
    assert resultado, "❌ Mensagem não encontrada após inserção"

    print("✅ Leitura ok:", resultado)

async def test_update_data(db: Database):
    # atualizando dados de usuarios

    await db.update_data(
        "users",
        conditions={"nome": "Maria"},
        data={"status": "inativo"}
    )

    print("✅ Atualização feita com sucesso")

    atualizado = await db.read_data("users", {"status": "inativo"})
    assert atualizado, "❌ Atualização não refletida"

    print("✅ Verificação de update ok")

    # atualizando dados de mensagens

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
    # deletando dados de usuarios
    await db.delete_data("users", {"nome": "Maria"})
    print("✅ Deleção feita com sucesso")

    
    resultado_final = await db.read_data("users", {"nome": "Maria"})
    assert not resultado_final, "❌ Usuário ainda existe após delete"

    print("✅ Verificação de delete ok")

    # deletando dados de mensagens
    await db.delete_data("messages", {"user_id": 1})
    print("✅ Deleção feita com sucesso")

    resultado_final = await db.read_data("messages", {"user_id": 1})
    assert not resultado_final, "❌ Mensagem ainda existe após delete"

    print("✅ Verificação de delete ok")

async def test_main():
    db = Database()

    await test_create_table(db)

if __name__ == "__main__":
    asyncio.run(test_main())