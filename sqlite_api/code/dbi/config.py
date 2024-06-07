import os

DBNAME = "my.db"

def getdb():
    database_path = os.environ.get('DBPATH')
    if database_path:
        if not os.path.exists(database_path):
            raise FileNotFoundError("No such database found")
        else:
            print(f"database from environment: {database_path}")
            return database_path
    else:
        if os.environ.get('DBNAME') is not None:
            database = os.environ.get('DBNAME')
            print(f"database from environment: {database}")
        else:
            database = 'my.db'
        basedir = os.path.dirname(os.path.abspath(__file__))
        fname = '%s/../data/database/%s' % (basedir, database)
        if not os.path.exists(fname):
            raise FileNotFoundError("No such database found")
        return fname