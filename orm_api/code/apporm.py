import os
import datetime
from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy


def get_db():
    """
    To get the path of the database being used. Extracts the path from the environment variable DBPATH.
    """
    return 'sqlite:///' + os.environ.get('DBPATH')


RESOURCES = ['Projects', 'Tasks']
app = Flask(__name__)
# app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////tmp/my.db'
app.config['SQLALCHEMY_DATABASE_URI'] = get_db()
db = SQLAlchemy(app)


dateformat = "%Y-%m-%d"


class Projects(db.Model):
    """
    Represents the projects table. Makes it table object.
    """
    __tablename__ = 'projects'
    exclude = ["id"]
    fields = ["name", "begin_date", "end_date"]
    mandatory_fields = ["name"]
    optional_fields = ["begin_date", "end_date"]
    updateable_fields = ["name", "end_date"]

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.Text, nullable=False)
    begin_date = db.Column(db.Text)
    end_date = db.Column(db.Text)
    # tasks = db.relationship('Tasks', backref='project_fk_id')



class Tasks(db.Model):
    """
    Represents the tasks table. Makes it table object.
    """
    __tablename__ = 'tasks'
    exclude = ["id", "project_id"]
    fields = ["name", "priority", "status_id", "begin_date", "end_date"]
    mandatory_fields = ["name", "begin_date", "end_date", "project_id"]
    optional_fields = ["priority", "status_id"]
    updateable_fields = ["name", "end_date", "priority", "status_id"]

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.Text, nullable=False)
    priority = db.Column(db.Integer, default=1)
    status_id = db.Column(db.Unicode, default=1)
    begin_date = db.Column(db.Text, nullable=False)
    end_date = db.Column(db.Text, nullable=False)
    project_id = db.Column(db.Integer, db.ForeignKey('projects.id'))
    # project_fk = db.relationship('Projects', primaryjoin='Tasks.project_id == Projects.id')


def update_from_json(modelObj, obj, cls):
    """
    Update the DB row object if the column is in the updateable row category. A column in the mandatory category
    cannot be updated to be empty.
    """
    obj_updated = False
    for fld in modelObj.fields :
        if fld in obj:
            if fld in cls.updateable_fields:
                if fld in cls.mandatory_fields:
                    if obj[fld]:
                        setattr(modelObj, fld, obj[fld])
                else:
                    setattr(modelObj, fld, obj[fld])
                obj_updated = True
    return obj_updated

    #     if fld in obj and obj[fld]:
    #         setattr(modelObj, fld, obj[fld])
    #         obj_updated = True
    # return obj_updated


def mandatory_field_check(data, mandatory_fields):
    """
    Checks if the given data has all the mandatory fields of that table. If all mandatory fields are present, returns
    a dictionary only mandatory columns and their provided values.
    """
    valid = {}
    for field in mandatory_fields:
        if field in data and data[field]:
            valid[field] = data[field]
        else:
            valid.clear()
            break
    return valid


def add_optional_fields(data, obj, optional_fields):
    """
    Adds optional columns and their values to the provided dictionary from an input data set.
    """
    for field in optional_fields:
        if field in data and data[field]:
            obj[field] = data[field]


@app.route('/', methods=['GET'])
def home():
    """
    Home page.
    """
    return """<h1>Projects and Tasks APIs</h1>
    <p>Prototype APIs for Projects and Tasks from sqlite tutorial.</p>
    """

@app.route('/api/resources/projects', methods=['PUT'])
@app.route('/api/resources/projects/<int:row_id>', methods=['PUT'])
def projects_update(row_id=None):
    """
    To update a row in the projects table.
    """
    data = request.json
    print(data)
    if row_id:
        modelObj = db.session.query(Projects).filter(Projects.id == row_id).first()
    else:
        modelObj = db.session.query(Projects).filter(Projects.id == data['id']).first()
    if modelObj:
        updated = update_from_json(modelObj, data, Projects)
        if updated:
            # db.session.add(modelObj)
            db.session.commit()
            # project = Projects(modelObj)
            outdata = to_dict(modelObj, Projects, [])
            print(outdata)
            return jsonify(outdata), 200
        return jsonify({"message": "incorrect field", "updateable fields": Projects.updateable_fields,
                        "Non empty fields": Projects.mandatory_fields}), 400
    return jsonify({"message": "invalid row"}), 400


@app.route('/api/resources/tasks', methods=['PUT'])
@app.route('/api/resources/tasks/<int:row_id>', methods=['PUT'])
def tasks_update(row_id=None):
    """
    To update a row in the tasks table
    """
    data = request.json
    print(data)
    if row_id:
        modelObj = db.session.query(Tasks).filter(Tasks.id == row_id).first()
    else:
        modelObj = db.session.query(Tasks).filter(Tasks.id == data['id']).first()
    if modelObj:
        updated = update_from_json(modelObj, data, Tasks)
        if updated:
            db.session.commit()
            outdata = to_dict(modelObj, Tasks, [])
            return jsonify(outdata), 200
        return jsonify({"message": "incorrect field", "updateable fields": Tasks.updateable_fields,
                        "Non empty fields": Tasks.mandatory_fields}), 400
    return jsonify({"message": "invalid row"}), 400


@app.route('/api/resources/projects', methods=['POST'])
def projects_create():
    '''
    To create a new row in the projects table
    '''
    data = request.json
    print(data)
    obj = mandatory_field_check(data, Projects.mandatory_fields)
    if obj:
        if "begin_date" not in obj:
            obj["begin_date"] = datetime.datetime.now().date().strftime(dateformat)
        add_optional_fields(data, obj, Projects.optional_fields)
        project = Projects(**obj)
        db.session.add(project)
        db.session.commit()
        outdata = to_dict(project, Projects, [])
        return jsonify(outdata), 201
    else:
        return jsonify({"message": "missing fields", "fields": Projects.mandatory_fields}), 400
        # if 'name' in data:
        #     data = {'name': data["name"], "begin_date": date.today(), "end_date": "Yet to be decided"}
        # else:
        #     return jsonify({"message": "nok"}), 404


@app.route('/api/resources/tasks', methods=['POST'])
def tasks_create():
    """
    To create a new row in the tasks table
    """
    data = request.json
    print(data)
    obj = mandatory_field_check(data, Tasks.mandatory_fields)
    if obj:
        stobj = datetime.datetime.strptime(obj["begin_date"], dateformat)
        edobj = datetime.datetime.strptime(obj["end_date"], dateformat)
        if stobj > edobj:
            return jsonify({"message": "invalid date"}), 404
        else:
            modelObj = db.session.query(Projects).filter(Projects.id == obj["project_id"]).first()
            if not modelObj:
                return jsonify({"message": "Associated project not found"}), 404
            proj_stobj = datetime.datetime.strptime(modelObj.begin_date, dateformat)
            if stobj < proj_stobj:
                return jsonify({"message": "invalid date"}), 404
            if modelObj.end_date:
                proj_edobj = datetime.datetime.strptime(modelObj.end_date, dateformat)
                if edobj < proj_edobj:
                    return jsonify({"message": "invalid date"}), 404
            add_optional_fields(data, obj, Tasks.optional_fields)
            task = Tasks(**obj)
            db.session.add(task)
            db.session.commit()
            outdata = to_dict(task, Tasks, [])
            return jsonify(outdata), 201
    else:
        return jsonify({"message": "missing fields", "fields": Tasks.mandatory_fields}), 400


@app.route('/api/resources/projects', methods=['DELETE'])
@app.route('/api/resources/projects/<int:project_id>', methods=['DELETE'])
def projects_delete(project_id=None):
    """
    To delete a row in the projects table based on row id
    """
    if project_id:
        data = project_id
    elif request.json and 'id' in request.json:
        data = request.json['id']
    print(data)
    modelObj = db.session.query(Projects).filter(Projects.id == data).first()
    if modelObj:
        c = db.session.query(Tasks).filter(Tasks.project_id == modelObj.id).count()

        if c:
            return jsonify({"message": f"{c} Tasks exists for this project"}), 400
        db.session.delete(modelObj)
        db.session.commit()
        return ('', 204)
    return jsonify({"message": "nok"}), 404


# @app.route('/api/resources/tasks', methods=['DELETE'])
# @app.route('/api/resources/tasks/<int:task_id>', methods=['DELETE'])
# def tasks_delete(task_id=None):
#     """
#     To delete a row in the tasks table based on row id
#     """
#     if task_id:
#         data = task_id
#     elif request.json and 'id' in request.json:
#         data = request.json['id']
#     print(data)
#     modelObj = db.session.query(Tasks).filter(Tasks.id == data).first()
#     if modelObj:
#         db.session.delete(modelObj)
#         db.session.commit()
#         return ('', 204)
#     return jsonify({"message": "nok"}), 404


@app.route('/api/resources/projects/<int:project_id>/tasks/<int:task_id>', methods=['DELETE'])
def tasks_del(project_id, task_id):
    """
    To delete a row in the tasks table based on row id
    """
    if project_id:
        projobj = db.session.query(Projects).filter(Projects.id == project_id).first()
        if projobj and task_id:
            task_obj = db.session.query(Tasks).filter(Tasks.project_id == project_id, Tasks.id == task_id).first()
            if task_obj:
                db.session.delete(task_obj)
                db.session.commit()
                return ('', 204)
            return jsonify({"message": "No task associated with project"}), 404
        return jsonify({"message": "Project not found"}), 404


@app.route('/api/resources/projects', methods=['GET'])
@app.route('/api/resources/projects/<int:resource_id>', methods=['GET'])
def projects(resource_id=None):
    """
    To retrieve either all rows or a specific row based on a column
    """
    if resource_id:
        modelObj = db.session.query(Projects).filter(Projects.id == resource_id).first()
        if modelObj:
            return jsonify(to_dict(modelObj, Projects, Projects.exclude))
        return jsonify({"message": "project not found"}), 404
    else:
        modelobjs = []
        objs = db.session.query(Projects).all()
        for obj in objs:
            modelobjs.append(to_dict(obj, Projects, []))
        return jsonify(modelobjs)


@app.route('/api/resources/tasks', methods=['GET'])
@app.route('/api/resources/tasks/<int:resource_id>', methods=['GET'])
def tasks(resource_id=None):
    """
    To retrieve either all rows or a specific row based on a column
    """
    if resource_id:
        modelObj = db.session.query(Tasks).filter(Tasks.id == resource_id).first()
        if modelObj:
            return jsonify(to_dict(modelObj, Tasks, Tasks.exclude))
        return jsonify({"message": "tasks not found"}), 404
    else:
        modelobjs = []
        objs = db.session.query(Tasks).all()
        for obj in objs:
            modelobjs.append(to_dict(obj, Tasks, []))
        return jsonify(modelobjs)


@app.route('/api/resources/projects/<int:project_id>/tasks', methods=['GET'])
@app.route('/api/resources/projects/<int:project_id>/tasks/<int:resource_id>', methods=['GET'])
def project_tasks(project_id, resource_id=None):
    """
    To retrieve either all rows or a specific row based on a column
    """

    projectObj = db.session.query(Projects).filter(Projects.id == project_id).first()
    if projectObj:
        if resource_id:
            modelObj = db.session.query(Tasks).filter(Tasks.project_id == project_id, Tasks.id == resource_id).first()
            if modelObj:
                return jsonify(to_dict(modelObj, Tasks, Tasks.exclude))
            return jsonify({"message": "Task for project_id not found"}), 404
        else:
            taskobjs = db.session.query(Tasks).filter(Tasks.project_id == project_id).all()
            modelobjs = []
            for obj in taskobjs:
                modelobjs.append(to_dict(obj, Tasks, []))
            return jsonify(modelobjs), 200
    return jsonify({"message": "project not found"}), 404


# @app.route('/api/resources/<resource>', methods=['GET'])
# @app.route('/api/resources/<resource>/<int:resource_id>', methods=['GET'])
# def resources(resource, resource_id=None):
#     res = resource.title()
#     if res not in RESOURCES:
#         return jsonify({"message": "Unsupported resource: %s" % resource})
#     clsObj = eval(resource.title())
#     if resource_id:
#         modelObj = db.session.query(clsObj).filter(clsObj.id == resource_id).first()
#         return jsonify(to_dict(modelObj, modelObj.__class__))
#     else:
#         modelobjs = []
#         objs = db.session.query(clsObj).all()
#         for obj in objs:
#             modelobjs.append(to_dict(obj, obj.__class__))
#         return jsonify(modelobjs)


@app.errorhandler(404)
def page_not_found(e):
    """
    In case an incorrect url is specified
    """
    return """<h1>Projects and Tasks APIs</h1><h2>Page Not Found</h2>""", 404


def to_dict(inst, cls, exclude_list):
    """
    Converts an instance of a projects table or tasks table class or row instance to a dictionary
    """
    convert = dict()
    # add your coversions for things like datetime's 
    # and what-not that aren't serializable.
    d = dict()
    print(cls)
    print(type(cls))
    if not inst or cls.__name__ == 'NoneType':
        return d
    for c in cls.__table__.columns:
        if c.name in exclude_list:
            continue
        v = getattr(inst, c.name)
        if c.type in convert.keys() and v is not None:
            try:
                d[c.name] = convert[c.type](v)
            except:
                d[c.name] = "Error:  Failed to covert using ", str(convert[c.type])
        elif v is None:
            d[c.name] = str()
        else:
            d[c.name] = v
    return d


if __name__ == '__main__':
    if os.environ.get('PORT') is not None:
        app.run(debug=True, host='0.0.0.0', port=os.environ.get('PORT'))
    else:
        app.run(debug=True, host='0.0.0.0') 
