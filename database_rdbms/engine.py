from table import Table
from parser import parse

class DatabaseEngine:
    def __init__(self):
        self.tables = {}

    def execute(self, query):
        query = query.strip()
        if query.endswith(";"):
             query = query[:-1]

        command = parse(query)

        if command[0] == "CREATE":
            _, name, columns, primary_key, unique_columns = command
            self.tables[name] = Table(
                name, columns, primary_key, unique_columns
            )
            return "Table created"

        if command[0] == "INSERT":
            _, name, values = command
            self.tables[name].insert(values)
            return "Row inserted"

        if command[0] == "SELECT_ALL":
            _, name = command
            return self.tables[name].select_all()

        if command[0] == "SELECT_WHERE":
            _, name, column, value = command
            return self.tables[name].select_where(column, value)
        
        if command[0] == "DELETE":
            _, name, column, value = command
            count = self.tables[name].delete_where(column, value)
            return f"{count} row(s) deleted"
        
        if command[0] == "UPDATE":
            _, name, where_col, where_val, set_col, set_val = command
            count = self.tables[name].update_where(
                where_col, where_val, set_col, set_val
            )
            return f"{count} row(s) updated"
        
        if command[0] == "JOIN":
            _, left, right, left_col, right_col = command
            return self.inner_join(left, right, left_col, right_col)




    def create_table(self, name, columns, primary_key=None, unique_columns=None):
        self.tables[name] = Table(
            name,
            columns,
            primary_key=primary_key,
            unique_columns=unique_columns
        )


    def insert(self, table_name, values):
        self.tables[table_name].insert(values)

    def select(self, table_name):
        return self.tables[table_name].select_all()
    
    
    def inner_join(self, left_table, right_table, left_col, right_col):
        left = self.tables[left_table]
        right = self.tables[right_table]

        results = []

        # Optimization: use index if available
        if right_col in right.indexes:
            for row in left.rows:
                key = row[left_col]
                matches = right.indexes[right_col].get(key, [])
                for match in matches:
                    joined = {}

                    for k, v in row.items():
                        joined[f"{left_table}.{k}"] = v

                    for k, v in match.items():
                        joined[f"{right_table}.{k}"] = v

                    results.append(joined)
        else:
            # Nested loop join (slow but correct)
            for lrow in left.rows:
                for rrow in right.rows:
                    if lrow[left_col] == rrow[right_col]:
                        joined = {}

                        for k, v in lrow.items():
                            joined[f"{left_table}.{k}"] = v

                        for k, v in rrow.items():
                            joined[f"{right_table}.{k}"] = v

                        results.append(joined)

        return results

