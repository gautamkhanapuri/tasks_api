import os
import sqlite3
import sys
import json
from config import getdb

def update_projects(conn, values):
    update_statement = '''UPDATE projects SET name = ?, begin_date = ?, end_date = ? WHERE id = ?'''
    cur = conn.cursor()
    cur.execute(update_statement, values)
    conn.commit()


def update_tasks(conn, values):
    update_statement = '''UPDATE tasks SET name = ?, priority = ?, status_id = ?, project_id = ?, begin_date = ?, end_date = ?  WHERE id = ?'''
    cur = conn.cursor()
    cur.execute(update_statement, values)
    conn.commit()


def convert_to_tuple(data, table_name):
    res = []
    updatetable_query = None
    if table_name == 'projects':
        cols = ['name', 'begin_date', 'end_date']
        primary_key = 'id'
    elif table_name == 'tasks':
        cols = ['name', 'priority', 'project_id', 'status_id', 'begin_date', 'end_date']
        primary_key = 'id'
    else:
        cols = None
    if primary_key in data and data[primary_key]:
        updatetable_query = 'UPDATE %s SET ' %table_name
        for col in cols:
            if col in data:
                updatetable_query += '%s = ?, ' % col
                res.append(data[col])
        if res:
            updatetable_query = updatetable_query[:-2] + ' where %s = ? ' %  primary_key
            res.append(data[primary_key])
        else:
            raise ValueError('No existing columns are found in the data')
        res = tuple(res)
    return updatetable_query, res


def update_tab(query, value):
    with sqlite3.connect(getdb()) as conn:
        cur = conn.cursor()
        cur.execute(query, value)
        conn.commit()

def main():
    try:
        data_file = None
        table_type = None
        if len(sys.argv) > 2:
            data_file = sys.argv[1]
            table_type = sys.argv[2]
        if data_file and table_type:
            os.path.exists(data_file)
            assert table_type.lower() == 'projects' or table_type.lower() == 'tasks', 'table_type can only be "tables" or "tasks"'
            with open(data_file) as fd:
                data = json.load(fd)
            qry, data = convert_to_tuple(data, table_type)
            print(qry)
            print(data)
            if qry and data:
                update_tab(qry,data)
    except Exception as err:
        print(err)




def main1():
    try:
        with sqlite3.connect(getdb()) as conn:
            # updating projects
            project_values_2 = ('Short video clip on Cool App', '2015-02-01', '2015-02-25', 2)
            update_projects(conn, project_values_2)
            # updating tasks
            task_values_3 = ('Think about improvements to the app', 2, 2, 2, '2015-02-01', '2015-02-25', 3)
            task_values_4 = ('Think about new features and services', 3, 2, 3, '2015-02-01', '2015-02-25', 4)
            update_tasks(conn, task_values_3)
            update_tasks(conn, task_values_4)
    except sqlite3.Error as e:
        print(e)


if __name__ == '__main__':
    main()


