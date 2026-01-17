from flask import Flask, request, jsonify
from flask_cors import CORS
import sys
import os

BASE_DIR = os.path.dirname(os.path.dirname(__file__))
sys.path.append(os.path.join(BASE_DIR, "database_rdbms"))

from engine import DatabaseEngine

app = Flask(__name__)
CORS(app)

db = DatabaseEngine()

# -------------------------------------------------
# SCHEMA INITIALIZATION
# -------------------------------------------------

db.execute("""
CREATE TABLE users (
  id INT PRIMARY,
  name TEXT UNIQUE,
  age INT
)
""")

db.execute("""
CREATE TABLE orders (
  id INT PRIMARY,
  user_id INT,
  product TEXT
)
""")

# -------------------------------------------------
# USERS CRUD
# -------------------------------------------------

@app.route("/users", methods=["GET"])
def get_users():
    return jsonify(db.execute("SELECT * FROM users"))

def get_next_id(table):
    rows = db.execute(f"SELECT * FROM {table}")
    return max([r["id"] for r in rows], default=0) + 1

@app.route("/users", methods=["POST"])
def create_user():
    data = request.json
    user_id = get_next_id("users")

    db.execute(
        f'INSERT INTO users VALUES ({user_id}, "{data["name"]}", {data["age"]})'
    )

    return jsonify({"status": "created", "id": user_id})

@app.route("/users/<int:user_id>", methods=["PUT"])
def update_user(user_id):
    data = request.json

    db.execute(
        f'UPDATE users SET name = "{data["name"]}" WHERE id = {user_id}'
    )
    db.execute(
        f'UPDATE users SET age = {data["age"]} WHERE id = {user_id}'
    )

    return jsonify({"status": "updated"})

@app.route("/users/<int:user_id>", methods=["DELETE"])
def delete_user(user_id):
    db.execute(f"DELETE FROM users WHERE id = {user_id}")
    return jsonify({"status": "deleted"})

# -------------------------------------------------
# ORDERS CRUD (needed for JOIN demo)
# -------------------------------------------------

@app.route("/orders", methods=["POST"])
def create_order():
    data = request.json
    order_id = get_next_id("orders")

    db.execute(
        f'''
        INSERT INTO orders VALUES
        ({order_id}, {data["user_id"]}, "{data["product"]}")
        '''
    )

    return jsonify({"status": "created", "id": order_id})

@app.route("/orders", methods=["GET"])
def get_orders():
    return jsonify(db.execute("SELECT * FROM orders"))

# -------------------------------------------------
# DYNAMIC JOIN ENDPOINT (THIS IS THE KEY PART)
# -------------------------------------------------

@app.route("/join", methods=["POST"])
def join_tables():
    data = request.json

    required_fields = [
        "left_table",
        "right_table",
        "left_column",
        "right_column",
    ]

    for field in required_fields:
        if field not in data or not data[field]:
            return jsonify({"error": f"Missing field: {field}"}), 400

    left_table = data["left_table"].strip()
    right_table = data["right_table"].strip()
    left_column = data["left_column"].strip()
    right_column = data["right_column"].strip()

    # Build SQL EXACTLY how the engine expects it
    query = (
        f"SELECT * FROM {left_table} "
        f"INNER JOIN {right_table} "
        f"ON {left_table}.{left_column} = {right_table}.{right_column};"
    )

    try:
        result = db.execute(query)
        return jsonify(result)
    except Exception as e:
        return jsonify({"error": str(e), "query": query}), 400


# -------------------------------------------------

if __name__ == "__main__":
    app.run(debug=True)
