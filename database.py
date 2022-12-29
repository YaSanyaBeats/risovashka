import sqlite3

path = "data.db"
sqlite_connection = sqlite3.connect(path, check_same_thread=False)
print("База данных создана и успешно подключена к SQLite")

cursor = sqlite_connection.cursor()

def existsTable(name):
    result = False

    cursor.execute(f''' SELECT count(name) FROM sqlite_master WHERE type='table' AND name='{name}' ''')

    if cursor.fetchone()[0] == 1:
        result = True

    sqlite_connection.commit()
    return result


def createTables():
    sqlite_create_table_query = '''CREATE TABLE levels (
                                        id      INTEGER PRIMARY KEY AUTOINCREMENT
                                                        UNIQUE
                                                        NOT NULL,
                                        title   TEXT    NOT NULL,
                                        picture TEXT    NOT NULL
                                    );
                                '''
    cursor.execute(sqlite_create_table_query)

    sqlite_create_table_query = '''CREATE TABLE colors (
                                        id    INTEGER PRIMARY KEY AUTOINCREMENT
                                                      UNIQUE
                                                      NOT NULL,
                                        title TEXT
                                    );

                                    '''
    cursor.execute(sqlite_create_table_query)

    sqlite_create_table_query = '''CREATE TABLE levelData (
                                        id       INTEGER PRIMARY KEY AUTOINCREMENT
                                                         NOT NULL
                                                         UNIQUE,
                                        id_level INTEGER REFERENCES levels (id),
                                        [row]    INTEGER,
                                        [column] INTEGER,
                                        id_color INTEGER REFERENCES colors (id) 
                                    );
                                    '''
    cursor.execute(sqlite_create_table_query)

    sqlite_connection.commit()


def getLevels():
    sqlite_select_table_query = "SELECT * FROM levels"

    cursor.execute(sqlite_select_table_query)
    rows = cursor.fetchall()
    sqlite_connection.commit()

    return rows

def getProgressLevels():
    sqlite_select_table_query = "SELECT * FROM levels WHERE status='In progress'"

    cursor.execute(sqlite_select_table_query)
    rows = cursor.fetchall()
    sqlite_connection.commit()

    return rows


def getContent(id):
    sqlite_select_table_query = "SELECT content FROM levels WHERE id=" + str(id)

    cursor.execute(sqlite_select_table_query)
    rows = cursor.fetchall()
    sqlite_connection.commit()

    return rows[0][0]

def getStatus(id):
    sqlite_select_table_query = "SELECT status FROM levels WHERE id=" + str(id)

    cursor.execute(sqlite_select_table_query)
    rows = cursor.fetchall()
    sqlite_connection.commit()

    return rows[0][0]
def getProgress(id):
    sqlite_select_table_query = "SELECT progress FROM levels WHERE id=" + str(id)

    cursor.execute(sqlite_select_table_query)
    rows = cursor.fetchall()
    sqlite_connection.commit()

    return rows[0][0]

def setProgress(id, progress):
    sqlite_select_table_query = "UPDATE levels set progress=?, status='In progress' WHERE id=?"

    cursor.execute(sqlite_select_table_query, (progress, id))
    rows = cursor.fetchall()
    sqlite_connection.commit()

def deleteProgress(id):
    sqlite_select_table_query = "UPDATE levels set progress=NULL, status='Not start' WHERE id=?"

    cursor.execute(sqlite_select_table_query, (id,))
    rows = cursor.fetchall()
    sqlite_connection.commit()