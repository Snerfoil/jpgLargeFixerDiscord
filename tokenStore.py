import psycopg2
import os
import pickle

selectQuery = "SELECT data_value FROM bottokens WHERE key_value=%s;"
insertQuery = "INSERT INTO bottokens (key_value ,data_value) VALUES (%s,%s);"
updateQuery = "UPDATE bottokens SET data_value=(%s) WHERE key_value = (%s);"
deleteQuery = "DELETE FROM bottokens WHERE key_value=%s;"

makeTable = "CREATE table bottokens(key_value VARCHAR NOT NULL PRIMARY KEY, data_value BYTEA NOT NULL);"
dropTable = "DROP TABLE bottokens;"

dbUrl = None
client = {}
try:
    dbUrl = os.environ['DATABASE_URL']
except KeyError:
    dbUrl = "" #input('url>>> ')
    print("DATABASE_URL isnt set")

def dbAction(func):
    def wrapper(*args,**kwargs):
        client['conn'] = psycopg2.connect(dbUrl)
        client['cur'] = client['conn'].cursor()
        runFunctRes = func(*args,**kwargs)
        client['conn'].commit()
        client['cur'].close()
        client['conn'].close()
        return runFunctRes
    return wrapper

@dbAction
def getVal(x):
    client['cur'].execute(selectQuery,(str(x),))
    result = client['cur'].fetchone()
    if(result is not None):
        return pickle.loads(result[0].tobytes())
    return None

@dbAction
def setVal(x,y):
    crunch = pickle.dumps(y)
    client['cur'].execute(selectQuery,(str(x),))
    result = client['cur'].fetchone()
    if(result is None):
        client['cur'].execute(insertQuery,(str(x),crunch,))
    else:
        client['cur'].execute(updateQuery,(crunch,str(x)))
    
    return crunch
        
@dbAction
def delVal(x):
    client['cur'].execute(selectQuery,(str(x),))
    result = client['cur'].fetchone()
    if(result is not None):
        client['cur'].execute(deleteQuery,(str(x),))
    else:
        return False
    return pickle.loads(result[0].tobytes())
    
@dbAction
def initSetup():
    print("preform setup")
    try:
        client['cur'].execute(makeTable)
        print("made table")
    except psycopg2.errors.DuplicateTable:
        print("table exists")

initSetup()