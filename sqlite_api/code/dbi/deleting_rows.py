import json
import sqlite3
import sys
import os.path
from dbi.config import getdb

def delete_row_projects(id):
    try:
        delete_statement = '''DELETE FROM projects WHERE ? = ?'''
        with sqlite3.connect(getdb()) as conn:
            cur = conn.cursor()
            cur.execute(delete_statement, id)
            conn.commit()
            print(f'Deleted row with {id[1]} from projects table.')
    except sqlite3.Error as e:
        print(e)


def delete_row_tasks(id):
    try:
        delete_statement = '''DELETE FROM tasks WHERE ? = ?'''
        with sqlite3.connect(getdb()) as conn:
            cur = conn.cursor()
            cur.execute(delete_statement, id)
            conn.commit()
            print(f'Deleted row with {id[1]} from tasks table')
    except sqlite3.Error as e:
        print(e)


def make_tuple(data, table):
    res = []
    res.append(table)
    projects_cols = ('name', 'begin_date', 'end_date', 'id')
    tasks_cols = ('name', 'priority', 'project_id', 'status_id', 'begin_date', 'end_date', 'id')

    if table.lower() == 'projects':
        for i in data:
            if i in projects_cols:
                res.append(i)
                res.append(data[i])
    else:
        for i in data:
            if i in tasks_cols:
                res.append(i)
                res.append(data[i])
    return tuple(res)


def delete_row(id):
    try:
        delete_statement = f'DELETE FROM {id[0]} WHERE {id[1]} = ?'
        with sqlite3.connect(getdb()) as conn:
            cur = conn.cursor()
            cur.execute(delete_statement, id[2:])
            conn.commit()
            print(f'Deleted row with {id[1]} = {id[2]} from {id[0]} table')
    except sqlite3.Error as e:
        print(e)


def main():
    try:
        data_file = None
        table_type = None
        if len(sys.argv) > 2:
            data_file = sys.argv[1]
            table_type = sys.argv[2]
        if data_file:
            os.path.exists(data_file)
            assert table_type.lower() == 'projects' or table_type.lower() == 'tasks', 'table_type can only be "tables" or "tasks"'
            with open(data_file) as fd:
                data = json.load(fd)
            data = make_tuple(data, table_type)
            if data:
                delete_row(data)
    except Exception as err:
        print(err)

# delete_row_projects(3)
# delete_row_tasks(6)

if __name__ == '__main__':
    main()