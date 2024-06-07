import sqlite3
import json
from dbi.config import getdb


def to_dict(row, table_type='projects'):
    if table_type == 'projects':
        cols = ['id', 'name', 'begin_date', 'end_date']
    elif table_type == 'tasks':
        cols = ['id', 'name', 'priority', 'project_id', 'status_id', 'begin_date', 'end_date']
    else:
        cols = None
    j_row = {}
    if cols:
        for key, value in zip(cols, row):
            j_row[key] = value
    return j_row

def query(query, table_type):
    data = []
    try:
        with sqlite3.connect(getdb()) as conn:
            cur = conn.cursor()
            cur.execute(query)
            rows = cur.fetchall()
            for row in rows:
                j_row = to_dict(row, table_type)
                # print(row)
                # print(json.dumps(j_row, indent=2))
                # print('#' * 20)
                data.append(j_row)
    except sqlite3.Error as e:
        print(e)
    return data



if __name__ == '__main__':
    rows = query('select * from projects', 'projects')
    print(json.dumps(rows, indent=2))
    task_rows = query('select * from tasks', 'tasks')
    print(json.dumps(task_rows, indent=2))

# data = query('select * from projects where id = 2', 'projects')
# data = data[0]
# print(data)
# taskdata = query(f'select * from tasks where project_id = 2', "tasks")
# data['tasks'] = taskdata
# print(json.dumps(data, indent=2))

