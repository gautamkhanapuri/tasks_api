import os

DBNAME = "my.db"

def getdb(database=None):
    if database is None:
        database = DBNAME
    if os.environ.get('DBNAME') is not None:
        database = os.environ.get('DBNAME')
        print(f"database from environment: {database}")
    basedir = os.path.dirname(os.path.abspath(__file__))
    fname = '%s/../data/database/%s' % (basedir, database)
    if not os.path.exists(fname):
        raise FileNotFoundError("No such database found")
    return fname