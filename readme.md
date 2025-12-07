# 🚀 HabitSync Backend

![Python](https://img.shields.io/badge/Python-3.10%2B-blue)
![FastAPI](https://img.shields.io/badge/FastAPI-0.110+-009688)
![License](https://img.shields.io/badge/License-MIT-green)
![Status](https://img.shields.io/badge/Status-Em%20Desenvolvimento-yellow)

Backend do **HabitSync**, uma API moderna e escalável para gerenciamento de hábitos, metas e rotina diária.  
Construído com **FastAPI**, arquitetura limpa, autenticação JWT e integração com banco de dados relacional.

---

## ⚙️ Tecnologias Utilizadas

- **Python 3.10+**
- **FastAPI**
- **SQLAlchemy**
- **Alembic (migrations)**
- **Pydantic**
- **JWT Authentication**

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

### 1️⃣ Clone o repositório

```bash
1️⃣ Clone o repositório

git clone https://github.com/RaphaelDaSilvaDev/HabitSync-Backend.git
cd HabitSync-Backend

2️⃣ Crie e ative o ambiente virtual

python -m venv venv
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate     # Windows

3️⃣ Instale as dependências

pip install -r requirements.txt

4️⃣ Configure as variáveis de ambiente

DATABASE_URL=postgresql://user:password@localhost:5432/habitsync
SECRET_KEY=sua_chave_super_secreta
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30

5️⃣ Execute o servidor

uvicorn app.main:app --reload

6️⃣ Acesse a documentação interativa

http://127.0.0.1:8000/docs
