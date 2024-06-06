import os
import sys
import json
from flask import Flask, request, jsonify, Response
from flask_sqlalchemy import SQLAlchemy

def get_db():
    database_path = os.environ.get('DBPATH')
    if database_path is None:
        print("Default database: my.db")
        basedir = os.path.dirname(os.path.abspath(__file__))
        fname = '%s/../data/database/my.db' % (basedir)
        return 'sqlite:///' + fname
    else:
        if not os.path.exists(database_path):
            raise FileNotFoundError("No such database found")
        else:
            print(f"database from environment: {database_path}")
            return 'sqlite:///' + os.environ.get('DBPATH')
    # if os.environ.get('DBNAME') is not None:
    #     database = os.environ.get('DBNAME')
    #     print(f"database from environment: {database}")
    # basedir = os.path.dirname(os.path.abspath(__file__))
    # fname = '%s/../data/database/%s' % (basedir, database)
    # if not os.path.exists(fname):
    #     raise FileNotFoundError("No such database found")
    # return fname
    # return 'sqlite:///' + os.environ.get('DBPATH')


RESOURCES = ['Projects', 'Tasks']
app = Flask(__name__)
# app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////tmp/my.db'
app.config['SQLALCHEMY_DATABASE_URI'] = get_db()
db = SQLAlchemy(app)



class Projects(db.Model):
    __tablename__ = 'projects'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.Text, nullable=False)
    begin_date = db.Column(db.Text)
    end_date = db.Column(db.Text)
    # tasks = db.relationship('Tasks', backref=db.backref('tasks', lazy='dynamic'))


class Tasks(db.Model):
    __tablename__ = 'tasks'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.Text, nullable=False)
    priority = db.Column(db.Integer)
    status_id = db.Column(db.Unicode)
    begin_date = db.Column(db.Text, nullable=False)
    end_date = db.Column(db.Text, nullable=False)
    project_id = db.Column(db.Integer, db.ForeignKey('projects.id'))


@app.route('/', methods=['GET'])
def home():
    return """<h1>Projects and Tasks APIs</h1>
    <p>Prototype APIs for Projects and Tasks from sqlite tutorial.</p>
    """


@app.route('/api/resources/projects', methods=['GET'])
@app.route('/api/resources/projects/<int:resource_id>', methods=['GET'])
def resources(resource_id=None):
    if resource_id:
        modelObj = db.session.query(Projects).filter(Projects.id == resource_id).first()
        return jsonify(to_dict(modelObj, Projects))
    else:
        modelobjs = []
        objs = db.session.query(Projects).all()
        for obj in objs:
            modelobjs.append(to_dict(obj, Projects))
        return jsonify(modelobjs)


@app.route('/api/resources/tasks', methods=['GET'])
@app.route('/api/resources/tasks/<int:resource_id>', methods=['GET'])
def tasks(resource_id=None):
    if resource_id:
        modelObj = db.session.query(Tasks).filter(Tasks.id == resource_id).first()
        return jsonify(to_dict(modelObj, Tasks))
    else:
        modelobjs = []
        objs = db.session.query(Tasks).all()
        for obj in objs:
            modelobjs.append(to_dict(obj, Tasks))
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


def to_dict(inst, cls):
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

