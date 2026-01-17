def clean(value):
    return value.strip().strip(";")

def parse(query):
    query = query.strip()
    tokens = query.split()

    command = tokens[0].upper()

    if command == "CREATE":
        table_name = tokens[2]

        column_defs = query[
            query.find("(") + 1 : query.rfind(")")
        ].split(",")

        columns = {}
        unique_columns = []
        primary_key = None

        for col_def in column_defs:
            parts = col_def.strip().split()
            col_name = parts[0]
            col_type = parts[1].upper()

            columns[col_name] = col_type

            if "PRIMARY" in parts:
                primary_key = col_name

            if "UNIQUE" in parts:
                unique_columns.append(col_name)

        return ("CREATE", table_name, columns, primary_key, unique_columns)

    if command == "INSERT":
        table_name = tokens[2]
        values_part = query.split("VALUES")[1]
        values = values_part.strip(" ();").split(",")
        values = [v.strip().strip('"') for v in values]
        return ("INSERT", table_name, values)
    
    if command == "SELECT" and "JOIN" in tokens:
        left_table = clean(tokens[3])
        right_table = clean(tokens[6])

        on_index = tokens.index("ON")
        left_expr = tokens[on_index + 1]
        right_expr = tokens[on_index + 3]

        left_col = clean(left_expr.split(".")[1])
        right_col = clean(right_expr.split(".")[1])


        return (
            "JOIN",
            left_table,
            right_table,
            left_col,
            right_col
        )

    if command == "SELECT":
        table_name = clean(tokens[3])

        if "WHERE" in tokens:
            where_index = tokens.index("WHERE")
            column = tokens[where_index + 1]
            value = tokens[where_index + 3].strip('";')
            return ("SELECT_WHERE", table_name, column, value)

        return ("SELECT_ALL", table_name)
    
    if command == "DELETE":
        table_name = tokens[2]

        if "WHERE" in tokens:
            where_index = tokens.index("WHERE")
            column = tokens[where_index + 1]
            value = tokens[where_index + 3].strip('";')
            return ("DELETE", table_name, column, value)

    if command == "UPDATE":
        table_name = clean(tokens[1])

        set_index = tokens.index("SET")
        where_index = tokens.index("WHERE")

        set_col = tokens[set_index + 1]
        set_val = tokens[set_index + 3].strip('";')

        where_col = tokens[where_index + 1]
        where_val = tokens[where_index + 3].strip('";')

        return (
            "UPDATE",
            table_name,
            where_col,
            where_val,
            set_col,
            set_val
        )
        
    



            