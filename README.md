<h1 align="center">✈️ Mape.ia</h1>

###

<p align="center">Uma aplicação web para planejamento de viagens.</p>

###

<h2 align="left">Estrutura do Diretório:</h2>

###

<h4 align="left">Componentes do projeto:</h4>

###

<h5 align="left">- frontend <br>-  backend API<br>- database <br>- scripts <br>- Dockerfile</h5>

###

<h2 align="left">Como Executar:</h2>

###

No windows, abra uma shell Git Bash antes de proceder.

Requirementos:
- python 3.12 [atenção especial para o MacOS](https://www.python.org/downloads/)
- pip
- node
- uma chave de api do groq.com

Todos exceto o python serão instalados automaticamente no passo seguinte.

Para preparar o ambiente de desenvolvimento no Linux, MacOS, BSD ou outros sistemas com o shell bash, execute:

```bash
git clone https://github.com/AndreFGard/dev-software-eq4
cd dev-software-eq4
bash install_tools.sh
```

###

<h2 align="left">Executar Frontend:</h2>

###

<h4 align="left">No Windows:</h4>
Usando um shell gitbash,

```bash
bash frontend_windows.sh
```

###

<h4 align="left">No Linux e MacOS:</h4>

```bash
cd frontend
npm run dev
```

###

<h2 align="left">Executar Backend:</h2>
configure a env var OPENAI_KEY para a sua chave de api do groq.com
```bash
fastapi run main.py
```

###

<h2 align="left">Passos tomados no desenvolvimento</h2>

- Determinação das tecnologias:
    - Foi escolhido FastAPI como backend e o Svelte.js como framework frontend, com o uso do pydantic e do typescript, respectivamente, para facilitar a validação de tipos e o desenvolvimento do projeto.


