class Table:
    def __init__(self, name, columns, primary_key=None, unique_columns=None):
        self.name = name
        self.columns = columns
        self.primary_key = primary_key
        self.unique_columns = unique_columns or []
        self.rows = []

        # column_name -> { value: row }
        self.indexes = {}

        if self.primary_key:
            self.indexes[self.primary_key] = {}

        for col in self.unique_columns:
            self.indexes[col] = {}

    def insert(self, values):
        row = {}
        for col, val in zip(self.columns.keys(), values):
            row[col] = self._normalize(col, val)

        # PRIMARY KEY check
        if self.primary_key:
            if row[self.primary_key] in self.indexes[self.primary_key]:
                raise Exception("Primary key violation")

        # UNIQUE constraint checks
        for col in self.unique_columns:
            if row[col] in self.indexes[col]:
                raise Exception(
                    f"UNIQUE constraint failed: {self.name}.{col}"
                )

        self.rows.append(row)

        # Update indexes
        for col, index in self.indexes.items():
            index[row[col]] = row

    def select_all(self):
        return self.rows

    def select_where(self, column, value):
        value = self._normalize(column, value)
        
        # 1. Indexed lookup (fast path)
        if column in self.indexes:
            row = self.indexes[column].get(value)
            return [row for row in self.rows if row[column] == value] if row else []

        # 2. Full table scan (slow path)
        results = []
        for row in self.rows:
            if row[column] == value:
                results.append(row)
        return results
    
    def _normalize(self, column, value):
        col_type = self.columns[column]

        if col_type == "INT":
            return int(value)

        return value

    def delete_where(self, column, value):
        value = self._normalize(column, value)

        # 1. Indexed delete (fast)
        if column in self.indexes:
            row = self.indexes[column].get(value)
            if not row:
                return 0

            self.rows.remove(row)

            # Remove from all indexes
            for col, index in self.indexes.items():
                index.pop(row[col], None)

            return 1

        # 2. Full table scan delete (slow)
        deleted = 0
        remaining_rows = []

        for row in self.rows:
            if row[column] == value:
                deleted += 1
                for col, index in self.indexes.items():
                    index.pop(row[col], None)
            else:
                remaining_rows.append(row)

        self.rows = remaining_rows
        return deleted
    
    def update_where(self, where_col, where_val, set_col, set_val):
        where_val = self._normalize(where_col, where_val)
        set_val = self._normalize(set_col, set_val)

        updated = 0

        # Step 1: find target rows
        if where_col in self.indexes:
            row = self.indexes[where_col].get(where_val)
            target_rows = [row] if row else []
        else:
            target_rows = [
                row for row in self.rows if row[where_col] == where_val
            ]

        for row in target_rows:
            # Step 2: constraint checks

            # PRIMARY KEY check
            if set_col == self.primary_key:
                if set_val in self.indexes[self.primary_key]:
                    raise Exception("Primary key violation")

            # UNIQUE check
            if set_col in self.unique_columns:
                if set_val in self.indexes[set_col]:
                    raise Exception(
                        f"UNIQUE constraint failed: {self.name}.{set_col}"
                    )

            # Step 3: update indexes (remove old value)
            if set_col in self.indexes:
                self.indexes[set_col].pop(row[set_col], None)

            # Step 4: update row
            row[set_col] = set_val

            # Step 5: reinsert into indexes
            if set_col in self.indexes:
                self.indexes[set_col][set_val] = row

            updated += 1

        return updated

