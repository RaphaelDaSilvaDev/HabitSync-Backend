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
- **PyTest**
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

## 🚏 API Endpoints

| Grupo | Descrição |
|-------|-----------|
| Auth  | Login, registro, refresh token |
| User  | CRUD de usuários |
| Habit | CRUD de hábitos do usuário |

Documentação completa das rotas:  
➡️ Veja em [`docs/API.md`](docs/API.md)  
➡️ Ou acesse a documentação interativa do FastAPI em `/docs`

---

## 🧪 Cobertura de Testes

| Arquivo                                | Stmts | Miss | Cover |
|----------------------------------------|-------|------|-------|
| app/exceptions/api_exception.py        | 17    | 0    | 100%  |
| app/exceptions/handlers.py             | 11    | 0    | 100%  |
| app/exceptions/middleware.py           | 17    | 7    | 59%   |
| app/main.py                            | 15    | 0    | 100%  |
| app/models/day.py                      | 15    | 1    | 93%   |
| app/models/habit.py                    | 20    | 0    | 100%  |
| app/models/habit_conclution.py         | 11    | 0    | 100%  |
| app/models/habit_day.py                | 3     | 0    | 100%  |
| app/models/user.py                     | 22    | 0    | 100%  |
| app/routers/auth_routes.py             | 23    | 0    | 100%  |
| app/routers/habit_routes.py            | 50    | 0    | 100%  |
| app/routers/user_routes.py             | 37    | 0    | 100%  |
| app/schemas/authenticate_schema.py     | 9     | 0    | 100%  |
| app/schemas/error_schema.py            | 4     | 0    | 100%  |
| app/schemas/habit_schema.py            | 26    | 0    | 100%  |
| app/schemas/response.py                | 11    | 0    | 100%  |
| app/schemas/token_schema.py            | 3     | 0    | 100%  |
| app/schemas/user_schema.py             | 24    | 0    | 100%  |
| app/services/auth_service.py           | 25    | 0    | 100%  |
| app/services/habit_service.py          | 108   | 0    | 100%  |
| app/services/user_service.py           | 56    | 0    | 100%  |
| app/utils/database.py                  | 13    | 2    | 85%   |
| app/utils/security.py                  | 38    | 0    | 100%  |
| **TOTAL**                              | **564** | **10** | **98%** |


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
Rodar as migrations no banco
Mapear as portas 8000 (API) e 5432 (Postgres)

http://127.0.0.1:8000/docs -> Swagger
http://127.0.0.1:8000/redoc -> Documentação
```
---
<div align="center">
Feito por Raphael da Silva 🚀 <br/>
</div>