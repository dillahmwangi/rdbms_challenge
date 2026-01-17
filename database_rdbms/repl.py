from engine import DatabaseEngine

db = DatabaseEngine()

while True:
    query = input("db> ")
    if query.lower() == "exit":
        break
    print(db.execute(query))
