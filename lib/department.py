from __init__ import CURSOR, CONN


class Department:
    
    def __init__(self, name, location, id=None):
        self.id = id
        self.name = name
        self.location = location

    def __repr__(self):
        return f"<Department {self.id}: {self.name}, {self.location}>"

    @classmethod
    def create_table(cls):
        """Create the departments table if it does not exist."""
        sql = """
        CREATE TABLE IF NOT EXISTS departments (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT,
            location TEXT
        )
        """
        CURSOR.execute(sql)
        CONN.commit()

    @classmethod
    def drop_table(cls):
        """Drop the departments table if it exists."""
        sql = "DROP TABLE IF EXISTS departments"
        CURSOR.execute(sql)
        CONN.commit()

    def save(self):
        """Save the department instance to the database and assign it an id."""
        if self.id is None:
            # If there's no id, it's a new department, so we insert it into the database
            sql = """
            INSERT INTO departments (name, location) 
            VALUES (?, ?)
            """
            CURSOR.execute(sql, (self.name, self.location))
            CONN.commit()
            self.id = CURSOR.lastrowid
        else:
            # If there's an id, update the existing department
            self.update()

    def update(self):
        """Update the department's details in the database."""
        sql = """
        UPDATE departments
        SET name = ?, location = ?
        WHERE id = ?
        """
        CURSOR.execute(sql, (self.name, self.location, self.id))
        CONN.commit()

    def delete(self):
        """Delete the department from the database."""
        sql = "DELETE FROM departments WHERE id = ?"
        CURSOR.execute(sql, (self.id,))
        CONN.commit()

    @classmethod
    def create(cls, name, location):
        """Create a new department in the database and return the instance."""
        department = cls(name, location)
        department.save()  # This will insert the department and set its ID
        return department

    @classmethod
    def find(cls, department_id):
        """Find and return a department by its ID."""
        sql = "SELECT * FROM departments WHERE id = ?"
        row = CURSOR.execute(sql, (department_id,)).fetchone()
        if row:
            return cls(id=row[0], name=row[1], location=row[2])
        return None

    @classmethod
    def all(cls):
        """Return a list of all departments."""
        sql = "SELECT * FROM departments"
        rows = CURSOR.execute(sql).fetchall()
        return [cls(id=row[0], name=row[1], location=row[2]) for row in rows]
