# ✈️ Mape.ia

# Estrutura do diretório
- Esboço da estrutura

```
project/
|── frontend/ # interface do usuário
|── backend/ # aplicação do servidor, API
|── database/ # arquivos relacionados ao banco de dados
|── scripts/ # scripts de inicialização e deploy
|── tests/ # testes do projeto
|── docker-compose.yml # opcional, configuração do ambiente
```

## Como executar:
No windows, abra uma shell Git Bash antes de proceder
Para preparar o ambiente de desenvolvimento no Linux, MacOS, BSD ou outros sistemas com o shell **bash**, execute:
```bash
git clone https://github.com/AndreFGard/dev-software-eq4
cd dev-software-eq4
bash install_tools.sh
```

### Executar frontend
Depois Para executar o frontend, execute
- No Windows: ``bash frontend_windows.sh``
- No Linux e MacOS:
```bash
cd frontend
npm run dev
```


### Executar backend:
```bash
fastapi run main.py
```


### Passos tomados no desenvolvimento
- Svelte puro com vite: npm create vite@latest ->  svelte -> typescript
