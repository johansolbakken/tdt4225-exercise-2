import dbconnection
import log
import performance
import queries
from model import User

"""
Singleton database connection
"""

initiated: bool = False
connector: dbconnection.DbConnector = None
cursor = None
db_connection = None

def init():
    global initiated, connector, cursor, db_connection
    _ = performance.Timer("(Database) Database init")
    try:
        connector = dbconnection.DbConnector(
            HOST="localhost",
            DATABASE="example",
            USER="example",
            PASSWORD="example",
        )
    except Exception as e:
        log.error(f"(Database) Failed to connect to database. {e}")

    cursor = connector.cursor
    db_connection = connector.db_connection

    initiated = True

def shutdown():
    check_initiated()
    global initiated, connector
    _ = performance.Timer("(Database) Database shutdown")
    connector.close_connection()
    initiated = False

def check_initiated():
    if initiated == False:
        log.error("(Database) Not initiated. Call db.init() first.")
        raise Exception("(Database) Not initiated. Call db.init() first.")

def nuke_database():
    global cursor
    check_initiated()
    _ = performance.Timer("(Database) Nuking database")

    try:
        cursor.execute("DROP TABLE IF EXISTS trackpoint")
        cursor.execute("DROP TABLE IF EXISTS activity")
        cursor.execute("DROP TABLE IF EXISTS user")
    except Exception as e:
        log.error(f"(Database) Failed to nuke database. {e}")
        exit(1)

def create_tables():
    global cursor
    check_initiated()
    _ = performance.Timer("(Database) Creating tables")

    cursor.execute(queries.create_user_table)
    cursor.execute(queries.create_activity_table)
    cursor.execute(queries.create_trackpoint_table)

def upload_data(self, data: list[User]=[]):
    global cursor, db_connection
    check_initiated()
    _ = performance.Timer("(Database) Uploading data")
    for (i, user) in enumerate(data):
        # if already exists, skip
        self.__cursor.execute(
            "SELECT * FROM user WHERE id = %s", (user.id,))
        if self.__cursor.fetchone() is not None:
            continue

        percentage = (i+1)/len(data) * 100
        _ = performance.Timer(
            f"\tUploading data for user {user.id} ({percentage:.2f}%)")

        if user.has_label:
            self.__cursor.execute(queries.insert_user, (user.id, 1))
        else:
            self.__cursor.execute(queries.insert_user, (user.id, 0))

        for activity in user.activities:
            self.__cursor.execute(queries.insert_activity, (activity.id, activity.user_id,
                                    activity.transportation_mode, activity.start_date_time, activity.end_date_time))

            for trackpoint in activity.trackpoints:
                self.__cursor.execute(queries.insert_new_trackpoint, (trackpoint.activity_id, trackpoint.lat,
                                        trackpoint.lon, trackpoint.altitude, trackpoint.date_days, trackpoint.date_time))
        self.__db_connection.commit()

def tables_exist():
    global cursor
    check_initiated()
    _ = performance.Timer("(Database) Checking if tables exist")
    cursor.execute("SHOW TABLES")
    tables = cursor.fetchall()
    return len(tables) == 3

# -------------- Part 2 --------------

# 1
def get_number_of_users():
    global cursor
    check_initiated()
    cursor.execute("SELECT COUNT(*) FROM user")
    return cursor.fetchone()[0]

def get_number_of_activities():
    global cursor
    check_initiated()
    cursor.execute("SELECT COUNT(*) FROM activity")
    return cursor.fetchone()[0]

def get_number_of_trackpoints():
    global cursor
    check_initiated()
    cursor.execute("SELECT COUNT(*) FROM trackpoint")
    return cursor.fetchone()[0]

# 2 

def get_average_trackpoints_per_user():
    global cursor
    check_initiated()
    cursor.execute("""SELECT AVG(t.amount)FROM (
                        SELECT COUNT(trackpoint.id) as amount
                        FROM trackpoint JOIN activity ON trackpoint.activity_id = activity.id JOIN user ON user.id = activity.user_id
                        GROUP BY user_id) as t""")
    return cursor.fetchone()[0]

def get_max_trackpoints_per_user():
    global cursor
    check_initiated
    cursor.execute("""SELECT MAX(t.amount)FROM (
                        SELECT COUNT(trackpoint.id) as amount
                        FROM trackpoint JOIN activity ON trackpoint.activity_id = activity.id JOIN user ON user.id = activity.user_id
                        GROUP BY user_id) as t""")
    return cursor.fetchone()[0]

def get_min_trackpoints_per_user():
    global cursor
    check_initiated()
    cursor.execute("""SELECT MIN(t.amount)FROM (
                        SELECT COUNT(trackpoint.id) as amount
                        FROM trackpoint JOIN activity ON trackpoint.activity_id = activity.id JOIN user ON user.id = activity.user_id
                        GROUP BY user_id) as t""")
    return cursor.fetchone()[0]