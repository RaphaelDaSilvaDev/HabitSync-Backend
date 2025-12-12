# 📘 HabitSync API Documentation

Base URL:

```
{{base_url}}
```

Token (quando necessário):

```
Authorization: Bearer {{token}}
```

---

# 👤 User Routes

## ➕ Create User

**POST** `/user/create`

### Body

```json
{
  "username": "User",
  "email": "user@example.com",
  "password": "secret"
}
```

---

## 📝 Update User

**PATCH** `/user/update`
🔐 *Requer autenticação*

### Body

```json
{
  "username": "Username"
}
```

---

## 🔒 Deactivate User

**PUT** `/user/deactivate`
🔐 *Requer autenticação*

---

## 🔓 Activate User

**PUT** `/user/activate`
🔐 *Requer autenticação*

---

## 👀 Get Logged User

**GET** `/user`
🔐 *Requer autenticação*

---

## 👥 Get All Users (Admin Only)

**GET** `/user/all-users`
🔐 *Requer admin token*

---

# 🔐 Auth Routes

## 🔑 Login

**POST** `/auth/login`

### Body

```json
{
  "email": "admin@habitsync.com",
  "password": "admin"
}
```

---

## ♻️ Refresh Token

**GET** `/auth/refresh-token`
🔐 *Requer autenticação*

---

# 📅 Habit Routes

## 📋 Get All Habits by User

**GET** `/habit`
🔐 *Requer autenticação*

---

## 🔎 Get Habit by ID

**GET** `/habit/{id}`
🔐 *Requer autenticação*

Example:

```
/habit/1
```

---

## ✅ Get Completed Habits By Date

**GET** `/habit/completed?date=YYYY-MM-DD`
🔐 *Requer autenticação*

Example:

```
/habit/completed?date=2025-12-07
```

---

## ⏳ Upcoming Habits

**GET** `/habit/upcoming`
🔐 *Requer autenticação*

---

## ➕ Create Habit

**POST** `/habit/create`
🔐 *Requer autenticação*

### Body

```json
{
  "name": "Ler",
  "description": "Ler 50 páginas",
  "frequency": [1, 2, 3, 4, 5, 6, 7]
}
```

---

## ✔️ Mark Habit as Done

**POST** `/habit/mark-done/{id}`
🔐 *Requer autenticação*

Example:

```
/habit/mark-done/2
```

---

## ✏️ Update Habit

**PATCH** `/habit/{id}`
🔐 *Requer autenticação*

### Body

```json
{
  "frequency": [1, 4]
}
```

---

## 🗑️ Delete Habit

**DELETE** `/habit/delete/{id}`
🔐 *Requer autenticação*

Example:

```
/habit/delete/6
```

---

## ❌ Unmark Habit as Done

**DELETE** `/habit/unmark-done/{id}`
🔐 *Requer autenticação*

Example:

```
/habit/unmark-done/1
```

---
