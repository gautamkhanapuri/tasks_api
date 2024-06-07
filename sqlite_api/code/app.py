from flask import Flask, request, jsonify, Response
import os
import yaml

from dbi.querying_data import query
from dbi.updating_rows import convert_to_tuple, update_tab
from dbi.inserting_rows import to_tuple, add_project, add_task
from dbi.deleting_rows import make_tuple, delete_row


# Globally visible.
app = Flask(__name__)


@app.route('/', methods=['GET'])
def home():
    return """<h1>Projects and Tasks APIs</h1>
    <p>Prototype APIs for Projects and Tasks from sqlite tutorial.</p>
    """


# Query data from projects table and return it to the user in json format
@app.route('/projects/query', methods=['GET'])
@app.route('/projects/query/<rowid>', methods=['GET'])
def projects(rowid=None):
    if rowid:
        data = query('select * from projects where id = %s' % rowid, "projects")
        if data:
            data = data[0]
            taskdata = query(f'select * from tasks where project_id = {rowid}', "tasks")
            data['tasks'] = taskdata
    else:
        data = query('select * from projects', "projects")
    print(data)
    return jsonify(data)


# Query data from tasks table and return it to the user in json format
@app.route('/tasks/query', methods=['GET'])
@app.route('/tasks/query/<rowid>', methods=['GET'])
def tasks(rowid):
    if rowid:
        data = query(f'select * from tasks where id = {rowid}', 'tasks')
    else:
        data = query('select * from tasks', 'tasks')
    print(jsonify(data))
    return jsonify(data)


# Accept input from user. accept data in the form of a dictionary. pass it to the convert to tuple func which returns
# a update query for projects table along with the values to be updated for the specific columns
@app.route('/projects/update', methods=['PUT'])
def projects_upd():
    indata = request.json
    print(indata)
    qry, data = convert_to_tuple(indata, "projects")
    print(qry)
    print(data)
    update_tab(qry, data)
    return jsonify({"message": "project updated"})


# Accept input from user. accept data in the form of a dictionary. pass it to the convert to tuple func which returns
# a update query for tasks table along with the values to be updated for the specific columns
@app.route('/tasks/update', methods=['PUT'])
def tasks_upd():
    indata = request.json
    print(indata)
    qry, data = convert_to_tuple(indata, 'tasks')
    print(qry)
    print(data)
    update_tab(qry, data)
    return jsonify({"message": "task updated"})


@app.route('/projects/insert', methods=['POST'])
def insert_project():
    indata = request.json
    print(indata)
    new_row_data = to_tuple(indata, 'projects')
    print(new_row_data)
    add_project(new_row_data)
    return jsonify({"message": "project added"}), 201


@app.route('/tasks/insert', methods=['POST'])
def insert_task():
    indata = request.json
    print(indata)
    new_row_data = to_tuple(indata, 'tasks')
    print(new_row_data)
    new_row_id = add_task(new_row_data)
    return jsonify({"message": "task added"}), 201


@app.route('/projects/delete', methods=['DELETE'])
def remove_row_projects():
    indata = request.json
    print(indata)
    del_row_data = make_tuple(indata, 'projects')
    print(del_row_data)
    delete_row(del_row_data)
    return jsonify({"message": "project removed"})


@app.route('/tasks/delete', methods=['DELETE'])
def remove_row_tasks():
    indata = request.json
    print(indata)
    del_row_data = make_tuple(indata, 'tasks')
    print(del_row_data)
    delete_row(del_row_data)
    return jsonify({"message": "task removed"})


@app.route('/yml/projects/query', methods=['GET', 'POST'])
@app.route('/yml/projects/query/<rowid>', methods=['GET', 'POST'])
@app.route('/yaml/projects/query', methods=['GET', 'POST'])
@app.route('/yaml/projects/query/<rowid>', methods=['GET', 'POST'])
def ymldata(rowid=None):
    # print(request.data)
    # rdata = yaml.safe_load(request.data)
    # print(rdata)
    # ydata = yaml.safe_dump(rdata)
    # print(ydata)
    print("*" * 20 + 'ymldata' + "*" *20)
    print(request.method)
    print(type(request.headers))
    print(request.headers)
    print(request.headers['Accept'])
    oformat = request.headers['Accept']
    if oformat and (oformat.lower() == 'application/yaml' or oformat.lower() == 'application/yml'
                    or oformat.lower() == '*/*'):
        if rowid:
            data = query('select * from projects where id = %s' % rowid, "projects")
            if data:
                data = data[0]
                taskdata = query(f'select * from tasks where project_id = {rowid}', "tasks")
                data['tasks'] = taskdata
        else:
            data = query('select * from projects', "projects")
        print(data)
        ydata = yaml.safe_dump(data)
        print(ydata)
        return Response(ydata, mimetype='application/yaml')
    elif oformat and oformat.lower() == 'application/json':
        if rowid:
            data = query('select * from projects where id = %s' % rowid, "projects")
            data = query('select * from projects where id = %s' % rowid, "projects")
            if data:
                data = data[0]
                taskdata = query(f'select * from tasks where project_id = {rowid}', "tasks")
                data['tasks'] = taskdata
        else:
            data = query('select * from projects', "projects")
        print(data)
        jdata = jsonify(data)
        print(jdata)
        return jdata


@app.route('/yaml/tasks/query', methods=['GET', 'POST'])
@app.route('/yaml/tasks/query/<rowid>', methods=['GET', 'POST'])
@app.route('/yml/tasks/query', methods=['GET', 'POST'])
@app.route('/yml/tasks/query/<rowid>', methods=['GET', 'POST'])
def yamldata(rowid=None):
    print('*' * 20 + 'yamldata' + '*'* 20)
    print(request.method)
    print(type(request.headers), request.headers)
    print(request.headers['Accept'])
    oformat = request.headers['Accept']
    if oformat and (oformat == 'application/yaml' or oformat == 'application/yml' or oformat == '*/*'):
        if rowid:
            data = query(f'select * from tasks where id = {rowid}', 'tasks')
        else:
            data = query('select * from tasks', 'tasks')
        if data:
            print(data)
            ydata = yaml.safe_dump(data)
            print(ydata)
            return Response(ydata, mimetype='application/yaml')
    elif oformat and oformat == 'application/json':
        if rowid:
            data = query(f'select * from tasks where id = {rowid}', 'tasks')
        else:
            data = query(f'select * from tasks', 'tasks')
        if data:
            print(data)
            jdata = jsonify(data)
            print(jdata)
            return jdata


@app.route('/yaml/projects/update', methods=['PUT'])
def yaml_projects_update():
    indata = yaml.safeload(request.data)
    qry, data = convert_to_tuple(indata, 'projects')
    print(qry)
    print(data)
    update_tab(qry, data)
    if request.headers['Accept'] == 'application/yaml' or request.headers['Accept'] == '*/*':
        return yaml.safe_dump({"message":"project updated"})
    else:
        return jsonify({"message":"project updated"})


@app.route('/yaml/tasks/update', methods=['PUT'])
def yaml_tasks_update():
    indata = yaml.safe_load(request.data)
    qry, data = convert_to_tuple(indata, 'tasks')
    update_tab(qry, data)
    if request.headers['Accept'] == 'application/yaml':
        return yaml.safe_dump({"message":"task updated"})
    else:
        return jsonify({"message":"project updated"})


@app.route('/yaml/projects/insert', methods=['POST'])
def yaml_projects_insert():
    indata = yaml.safe_load(request.data)
    new_row_data = to_tuple(indata, 'projects')
    add_project(new_row_data)
    if request.headers['Accept'] == 'application/yaml':
        return yaml.safe_dump({"message": "new project inserted"})
    else:
        return jsonify({"message": "new project inserted"})


@app.route('/yaml/tasks/insert', methods=['POST'])
def yaml_tasks_insert():
    indata = yaml.safe_load(request.data)
    new_row_data = to_tuple(indata, 'tasks')
    add_task(new_row_data)
    if request.headers['Accept'] == 'application/yaml':
        return yaml.safe_dump({"message": "new task inserted"})
    else:
        return jsonify({"message": "new task inserted"})


@app.route('/yaml/projects/delete', methods=['DELETE'])
def yaml_remove_row_projects():
    indata = yaml.safe_load(request.data)
    print(indata)
    del_row_data = make_tuple(indata, 'projects')
    print(del_row_data)
    delete_row(del_row_data)
    if request.headers['Accept'] == 'application/yaml':
        return yaml.safe_dump({"message": "project removed"})
    else:
        return jsonify({"message": "project removed"})

# TODO add try-except blocks, modularize functions, add xml compatibility

@app.route('/tasks/delete', methods=['DELETE'])
def yaml_remove_row_tasks():
    indata = yaml.safe_load(request.data)
    print(indata)
    del_row_data = make_tuple(indata, 'tasks')
    print(del_row_data)
    delete_row(del_row_data)
    if request.headers['Accept'] == 'application/yaml':
        return yaml.safe_dump({"message": "task removed"})
    else:
        return jsonify({"message": "task removed"})


@app.errorhandler(404)
def page_not_found(e):
    return """<h1>Projects and Tasks APIs</h1><h2>Page Not Found</h2>""", 404



if __name__ == '__main__':
    if os.environ.get('PORT') is not None:
        print(os.environ.get('PORT'))
        app.run(host='0.0.0.0', port=os.environ.get('PORT'))
    else:
        app.run(host='0.0.0.0') 

