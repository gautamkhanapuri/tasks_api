import sqlite3


def create_tables():
    sql_statements = [
        """CREATE TABLE IF NOT EXISTS projects (
                id INTEGER PRIMARY KEY, 
                name text NOT NULL, 
                begin_date TEXT, 
                end_date TEXT
        );""",
        """CREATE TABLE IF NOT EXISTS tasks (
                id INTEGER PRIMARY KEY, 
                name TEXT NOT NULL, 
                priority INT, 
                project_id INT NOT NULL, 
                status_id INT NOT NULL, 
                begin_date TEXT NOT NULL, 
                end_date TEXT NOT NULL, 
                FOREIGN KEY (project_id) REFERENCES projects (id)
        );"""]

    # create a database connection
    try:
        with sqlite3.connect('my.db') as conn:
            cursor = conn.cursor()
            for statement in sql_statements:
                cursor.execute(statement)

            conn.commit()
    except sqlite3.Error as e:
        print(e)


if __name__ == '__main__':
    create_tables()