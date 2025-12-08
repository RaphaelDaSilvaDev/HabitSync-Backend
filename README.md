# 🚀 HabitSync Backend

![Python](https://img.shields.io/badge/Python-3.10%2B-blue)
![FastAPI](https://img.shields.io/badge/FastAPI-0.110+-009688)
![Docker](https://img.shields.io/badge/Docker-20.10-blue?logo=docker&logoColor=white)
![License](https://img.shields.io/badge/License-MIT-green)
![Status](https://img.shields.io/badge/Status-Em%20Desenvolvimento-yellow)

Backend do **HabitSync**, uma API moderna e escalável para gerenciamento de hábitos, metas e rotina diária.  
Construído com **FastAPI**, arquitetura limpa, autenticação JWT e integração com banco de dados relacional.

---

## ⚙️ Tecnologias Utilizadas

- **Python 3.14+**
- **FastAPI**
- **SQLAlchemy**
- **Alembic**
- **PostgreSQL**
- **Pydantic**
- **JWT Authentication**
- **Docker**

---

## 📦 Funcionalidades

- 🔐 Autenticação com JWT (Access + Refresh Token)  
- 👤 CRUD de usuários  
- 📅 Gerenciamento de hábitos  
- 📊 Registro diário e acompanhamento de progresso  
- 🕒 Histórico completo  
- 🧩 Arquitetura organizada em módulos (services, repositories, schemas, routers)

---

## 🚀 Como Rodar o Projeto

```bash
Clone o repositório

git clone https://github.com/RaphaelDaSilvaDev/HabitSync-Backend.git
cd HabitSync-Backend

Crie o arquivo .env usando o .env-example
```

### 🐳 Rodando com Docker

```bash
1️⃣ Faça o build da aplicação

docker compose up --build

2️⃣ Acesse a documentação interativa

http://127.0.0.1:8000/docs -> Swagger
http://127.0.0.1:8000/redoc -> Documentação

Isso irá:
Construir a imagem do backend (habitsync_app)
Subir um container PostgreSQL (habitsync_database)
Mapear as portas 8000 (API) e 5432 (Postgres)
```

### 🐍 Rodando localmente

```bash
1️⃣ Crie e ative o ambiente virtual

python -m venv venv
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate     # Windows

2️⃣ Instale as dependências

pip install -r requirements.txt

3️⃣ Configure as variáveis de ambiente

DATABASE_URL=postgresql://user:password@localhost:5432/habitsync
SECRET_KEY=sua_chave_super_secreta
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30

4️⃣ Execute o servidor

uvicorn app.main:app --reload

5️⃣ Acesse a documentação interativa

http://127.0.0.1:8000/docs -> Swagger
http://127.0.0.1:8000/redoc -> Documentação

* necessário criar o banco de dados e passar no .env
```
---
<div align="center">
Feito por Raphael da Silva 🚀 <br/>
</div>