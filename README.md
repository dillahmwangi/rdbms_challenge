# Pesapal Junior Dev Challenge – Custom RDBMS

## Overview

This project is a complete implementation of a **simple relational database management system (RDBMS)** built from scratch, together with a **web application** that demonstrates how the database can be used in practice.

The goal of the challenge is not to build a production-grade database, but to clearly demonstrate:

* Understanding of core database concepts
* Ability to design systems from first principles
* Clear thinking, correctness, and determination

This repository contains:

1. A **custom SQL-like database engine** (Python)
2. An **interactive REPL** for executing SQL commands
3. A **backend API** that exposes the database to the web
4. A **React frontend** that demonstrates CRUD operations and SQL JOINs

---

## Features Implemented

### 1. Custom Database Engine

The database engine supports the following:

* Table creation with column definitions
* Column data types (`INT`, `TEXT`)
* Primary key constraints
* Unique column constraints
* CRUD operations:

  * `INSERT`
  * `SELECT`
  * `UPDATE`
  * `DELETE`
* Basic indexing for faster lookups
* `WHERE` filtering
* `INNER JOIN` between tables

The engine parses SQL-like commands and executes them against in-memory data structures.

---

### 2. SQL-like Interface (REPL)

An interactive REPL allows users to run SQL commands directly:

```sql
CREATE TABLE users (id INT PRIMARY, name TEXT UNIQUE, age INT);
INSERT INTO users VALUES (1, "Mwangi", 22);
SELECT * FROM users;
UPDATE users SET age = 23 WHERE id = 1;
DELETE FROM users WHERE id = 1;
```

This interface closely mirrors real SQL syntax while remaining simple and readable.

---

### 3. INNER JOIN Support

The engine supports basic INNER JOIN queries using table-qualified column names:

```sql
SELECT * FROM users
INNER JOIN orders
ON users.id = orders.user_id;
```

Internally, the engine:

* Parses the JOIN clause
* Matches rows based on join keys
* Produces a combined result set with prefixed column names

This demonstrates understanding of relational joins without relying on an external database.

---

### 4. Backend API (Flask)

A lightweight Flask API exposes the database engine to the frontend.

Key endpoints:

* `GET /users` – Fetch all users
* `POST /users` – Create a new user
* `PUT /users/<id>` – Update a user
* `DELETE /users/<id>` – Delete a user
* `POST /join` – Execute a dynamic INNER JOIN

Example JOIN request payload:

```json
{
  "left_table": "users",
  "right_table": "orders",
  "left_column": "id",
  "right_column": "user_id"
}
```

The API dynamically builds an SQL query and executes it through the custom engine.

---

### 5. Frontend (React)

The React frontend serves as a **demonstration UI**, not a full production system.

It showcases:

* Creating users
* Viewing users in a structured table
* Updating and deleting records
* Executing dynamic SQL INNER JOINs
* Displaying JOIN results in tabular form
* Previewing the generated SQL query

The frontend communicates exclusively with the backend API and does not use any external database.

---

## Project Structure

```
pesapal_challenge/
│
├── database_rdbms/
│   ├── engine.py        # Database execution engine
│   ├── table.py         # Table implementation
│   ├── parser.py        # SQL parser
│   └── repl.py          # Interactive REPL
│
├── backend_api/
│   └── app.py           # Flask API
│
├── web_app/
│   ├── src/
│   │   ├── App.js       # React UI
│   │   └── api.js       # API calls
│   └── package.json
│
└── README.md
```

---

## How to Run the Project

### 1. Run the Database REPL

```bash
cd database_rdbms
python repl.py
```

---

### 2. Run the Backend API

```bash
cd backend_api
python app.py
```

The API runs on:

http://127.0.0.1:5000
```



### 3. Run the Frontend

```bash
cd web_app
npm install
npm start
```

The frontend runs on:

```
http://localhost:3000
```

---

## Design Decisions

* **No external database**: All data storage is handled by the custom engine
* **SQL-first interface**: The engine prioritizes SQL-like syntax over ORM-style APIs
* **Clarity over completeness**: The system focuses on correctness and readability
* **Dynamic JOIN execution**: Joins are not hardcoded and are built from user input

---

## Limitations (By Design)

This project intentionally omits:

* Disk persistence
* Query optimization beyond basic indexing
* Advanced SQL features (GROUP BY, ORDER BY, subqueries)
* Authentication and authorization

These were excluded to keep the focus on core database principles.

---

## Why This Meets the Challenge Requirements

✔ Custom RDBMS implementation
✔ SQL-like interface
✔ CRUD operations
✔ Primary and unique key constraints
✔ Indexing
✔ JOIN support
✔ Interactive REPL
✔ Web application demonstrating database usage

---

## Attribution

This project was implemented as part of the **Pesapal Junior Dev Challenge ’26**.

AI tools were used for guidance and iteration, but all system design, logic, and integration decisions were made deliberately by the author.



