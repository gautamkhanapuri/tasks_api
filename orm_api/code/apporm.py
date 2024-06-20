import os
import sys
import json
from datetime import date
from flask import Flask, request, jsonify, Response
from flask_sqlalchemy import SQLAlchemy


def get_db():
    return 'sqlite:///' + os.environ.get('DBPATH')


RESOURCES = ['Projects', 'Tasks']
app = Flask(__name__)
# app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////tmp/my.db'
app.config['SQLALCHEMY_DATABASE_URI'] = get_db()
db = SQLAlchemy(app)


class Projects(db.Model):
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
    __tablename__ = 'tasks'
    exclude = ["id", "project_id"]
    fields = ["name", "priority", "status_id", "begin_date", "end_date"]
    mandatory_fields = ["name", "begin_date", "end_date", "project_id"]
    optional_fields = ["priority", "status_id"]
    updateable_fields = ["name", "end_date", "priority", "status_id"]

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.Text, nullable=False)
    priority = db.Column(db.Integer)
    status_id = db.Column(db.Unicode)
    begin_date = db.Column(db.Text, nullable=False)
    end_date = db.Column(db.Text, nullable=False)
    project_id = db.Column(db.Integer, db.ForeignKey('projects.id'))
    # project_fk = db.relationship('Projects', primaryjoin='Tasks.project_id == Projects.id')


def update_from_json(modelObj, obj, cls):
    "Update the DB row object"
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
    valid = {}
    for field in mandatory_fields:
        if field in data and data[field]:
            valid[field] = data[field]
        else:
            valid.clear()
            break
    return valid


def add_optional_fields(data, obj, optional_fields):
    for field in optional_fields:
        if field in data and data[field]:
            obj[field] = data[field]


@app.route('/', methods=['GET'])
def home():
    return """<h1>Projects and Tasks APIs</h1>
    <p>Prototype APIs for Projects and Tasks from sqlite tutorial.</p>
    """

@app.route('/api/resources/projects', methods=['PUT'])
@app.route('/api/resources/projects/<int:row_id>', methods=['PUT'])
def projects_update(row_id=None):
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
    // TODO
    '''
    data = request.json
    print(data)
    obj = mandatory_field_check(data, Projects.mandatory_fields)
    if obj:
        add_optional_fields(data, obj, Projects.optional_fields)
        obj['id1'] = 2
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
    data = request.json
    print(data)
    obj = mandatory_field_check(data, Tasks.mandatory_fields)
    if obj:
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
    if project_id:
        data = project_id
    elif request.json and 'id' in request.json:
        data = request.json['id']
    print(data)
    modelObj = db.session.query(Projects).filter(Projects.id == data).first()
    if modelObj:
        db.session.delete(modelObj)
        db.session.commit()
        return ('', 204)
    return jsonify({"message": "nok"}), 404


@app.route('/api/resources/tasks', methods=['DELETE'])
@app.route('/api/resources/tasks/<int:task_id>', methods=['DELETE'])
def tasks_delete(task_id=None):
    if task_id:
        data = task_id
    elif request.json and 'id' in request.json:
        data = request.json['id']
    print(data)
    modelObj = db.session.query(Tasks).filter(Tasks.id == data).first()
    if modelObj:
        db.session.delete(modelObj)
        db.session.commit()
        return ('', 204)
    return jsonify({"message": "nok"}), 404


@app.route('/api/resources/projects', methods=['GET'])
@app.route('/api/resources/projects/<int:resource_id>', methods=['GET'])
def projects(resource_id=None):
    if resource_id:
        modelObj = db.session.query(Projects).filter(Projects.id == resource_id).first()
        return jsonify(to_dict(modelObj, Projects, Projects.exclude))
    else:
        modelobjs = []
        objs = db.session.query(Projects).all()
        for obj in objs:
            modelobjs.append(to_dict(obj, Projects, []))
        return jsonify(modelobjs)


@app.route('/api/resources/tasks', methods=['GET'])
@app.route('/api/resources/tasks/<int:resource_id>', methods=['GET'])
def tasks(resource_id=None):
    if resource_id:
        modelObj = db.session.query(Tasks).filter(Tasks.id == resource_id).first()
        return jsonify(to_dict(modelObj, Tasks, Tasks.exclude))
    else:
        modelobjs = []
        objs = db.session.query(Tasks).all()
        for obj in objs:
            modelobjs.append(to_dict(obj, Tasks, []))
        return jsonify(modelobjs)


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
    return """<h1>Projects and Tasks APIs</h1><h2>Page Not Found</h2>""", 404


def to_dict(inst, cls, exclude_list):
    """
    Dict conversion
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
