import json
import sqlite3
import sys
import os
from dbi.config import getdb

def add_project(project):
    sql = ''' INSERT INTO projects(name,begin_date,end_date)
              VALUES(?,?,?) '''
    try:
        with sqlite3.connect(getdb()) as conn:
            cur = conn.cursor()
            cur.execute(sql, project)
            conn.commit()
    except sqlite3.Error as e:
        print(e)
    return cur.lastrowid

def to_tuple(obj, table_type):
    data = None
    if table_type == 'projects':
        cols = ['name', 'begin_date', 'end_date']
    elif table_type == 'tasks':
        cols = ['name', 'priority', 'project_id', 'status_id', 'begin_date', 'end_date']
    else:
        cols = None
    if cols:
        for col in cols:
            if col not in obj:
                break
        else:
            data = []
            for col in cols:
                data.append(obj[col])
            data = tuple(data)
    return data

def add_task(task):
    sql = '''INSERT INTO tasks(name,priority,status_id,project_id,begin_date,end_date)
             VALUES(?,?,?,?,?,?) '''
    try:
        with sqlite3.connect(getdb()) as conn:
            cur = conn.cursor()
            cur.execute(sql, task)
            conn.commit()
    except sqlite3.Error as e:
        print(e)
    return cur.lastrowid


def main():
    infile = None
    table_type = None
    if len(sys.argv) > 2:
        infile = sys.argv[1]
        table_type = sys.argv[2]
    if infile and table_type:
        if os.path.exists(infile):
            # data = None
            with open(infile) as jfile:
                obj = json.load(jfile)
                data = to_tuple(obj, table_type)
            if data:
                if table_type == 'projects':
                    project_id = add_project(data)
                    print(project_id)
                elif table_type == 'tasks':
                    task_id = add_task(data)
                    print(task_id)

def main1():
    try:
        with sqlite3.connect(getdb()) as conn:
            # add a new project
            project = ('Cool App with SQLite & Python', '2015-01-01', '2015-01-30')
            project_id = add_project(conn, project)
            print(f'Created a project with the id {project_id}')

            # tasks
            tasks = [
                ('Analyze the requirements of the app', 1, 1, project_id, '2015-01-01', '2015-01-02'),
                ('Confirm with user about the top requirements', 1, 1, project_id, '2015-01-03', '2015-01-05')
            ]
            for task in tasks:
                task_id = add_task(conn, task)
                print(f'Created a task with the id {task_id}')


    except sqlite3.Error as e:
        print(e)


if __name__ == '__main__':
    main()


