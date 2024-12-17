<h1 align="center">✈️ Mape.ia</h1>

###

<p align="center">Uma aplicação web para planejamento de viagens.</p>

###

<h2 align="left">Estrutura do Diretório:</h2>

###

<h4 align="left">Project:</h4>

###

<h5 align="left">- frontend <br>-  backend API<br>- database <br>- scripts <br>- tests <br>- docker-compose.yml</h5>

###

<h2 align="left">Como Executar:</h2>

###

<h5 align="left">No windows, abra uma shell Git Bash antes de proceder Para preparar o ambiente de desenvolvimento no Linux, MacOS, BSD ou outros sistemas com o shell bash, execute:</h5>

```bash
git clone https://github.com/AndreFGard/dev-software-eq4
cd dev-software-eq4
bash install_tools.sh
```

###

<h2 align="left">Executar Frontend:</h2>

###

<h4 align="left">No Windows:</h4>

```bash
frontend_windows.sh
```

###

<h4 align="left">No Linux e MacOS:</h4>

```bash
cd frontend
npm run dev
```

###

<h2 align="left">Executar Backend:</h2>

```bash
fastapi run main.py
```

###

<h2 align="left">Passos tomados no desenvolvimento</h2>

###

<h5 align="left">Svelte puro com vite: npm create vite@latest -> svelte -> typescript</h5>

###







readme anterior:
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