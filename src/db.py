"""
file: db.py
written by: Johan Solbakken, Morten Tobias Rinde Sunde
date: 05.10.2023

    Contains all the database functions used in the project.
    
"""

import dbconnection
import log
import performance
import queries as Queries
import datetime

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
        for name, _, drop in Queries.indexes:
            cursor.execute(drop)
            log.info(f"(Database) Dropped index {name}")

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

    cursor.execute(Queries.create_user_table)
    cursor.execute(Queries.create_activity_table)
    cursor.execute(Queries.create_trackpoint_table)

    for name,create,_ in Queries.indexes:
        cursor.execute(create)
        log.info(f"(Database) Created index {name}")

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
    _ = performance.Timer("(Database) Getting number of users")
    cursor.execute(Queries.number_of_users)
    return cursor.fetchone()[0]

def get_number_of_activities():
    global cursor
    check_initiated()
    _ = performance.Timer("(Database) Getting number of activities")
    cursor.execute(Queries.number_of_activities)
    return cursor.fetchone()[0]

def get_number_of_trackpoints():
    global cursor
    check_initiated()
    _ = performance.Timer("(Database) Getting number of trackpoints")
    cursor.execute(Queries.number_of_trackpoints)
    return cursor.fetchone()[0]

# 2 

def get_average_trackpoints_per_user():
    global cursor
    check_initiated()
    _ = performance.Timer("(Database) Getting average trackpoints per user")
    cursor.execute(Queries.average_trackpoint_per_user)
    return cursor.fetchone()[0]

def get_max_trackpoints_per_user():
    global cursor
    check_initiated()
    _ = performance.Timer("(Database) Getting max trackpoints per user")
    cursor.execute(Queries.most_trackpoint_per_user)
    return cursor.fetchone()[0]

def get_min_trackpoints_per_user():
    global cursor
    check_initiated()
    _ = performance.Timer("(Database) Getting min trackpoints per user")
    cursor.execute(Queries.least_trackpoint_per_user)
    return cursor.fetchone()[0]

# 3
def get_top_users_most_activites(n:int):
    global cursor
    check_initiated()
    _ = performance.Timer("(Database) Getting top users with most activities")
    cursor.execute(Queries.top_users_most_activites, [n])
    return cursor.fetchall()

# 4
def get_all_users_that_used(transportation_mode: str):
    global cursor
    check_initiated()
    _ = performance.Timer("(Database) Getting all users that have taken the bus")
    cursor.execute(Queries.users_that_have_taken_transportation_mode, [transportation_mode])
    return cursor.fetchall()

# 5
def get_top_users_with_the_most_different_transportation_modes(n:int):
    global cursor
    check_initiated()
    _ = performance.Timer("(Database) Getting top users with the most different transportation modes")
    cursor.execute(Queries.top_users_with_the_most_different_transportation_modes, [n])
    return cursor.fetchall()

# 6
def get_all_duplicate_activities():
    global cursor
    check_initiated()
    _ = performance.Timer("(Database) Getting all duplicate activities")
    cursor.execute(Queries.duplicate_activities)
    return cursor.fetchall()

# 7
def get_amount_of_users_with_activities_lasting_to_next_day():
    global cursor
    check_initiated()
    _ = performance.Timer("(Database) Getting amount of users with activities lasting to next day")
    cursor.execute(Queries.users_with_activities_lasting_to_next_day)
    return cursor.fetchone()[0]

def get_user_transportation_activity_hours_lasting_to_next_day(limit: bool = False):
    global cursor
    check_initiated()
    _ = performance.Timer("(Database) Getting users with activities lasting to next day")
    if limit:
        cursor.execute(Queries.user_transportation_mode_activity_hours + " LIMIT 15")
    else:
        cursor.execute(Queries.user_transportation_mode_activity_hours)
    return cursor.fetchall()

def get_all_users():
    global cursor
    check_initiated()
    _ = performance.Timer("(Database) Getting all users")
    cursor.execute(Queries.get_all_users)
    return cursor.fetchall()

def get_all_activities():
    global cursor
    check_initiated()
    _ = performance.Timer("(Database) Getting all activities")
    cursor.execute(Queries.get_all_activities)
    return cursor.fetchall()

def get_all_trackpoints():
    global cursor
    check_initiated()
    _ = performance.Timer("(Database) Getting all trackpoints")
    cursor.execute(Queries.get_all_trackpoints)
    return cursor.fetchall()

def user_exists(user_id: str):
    global cursor
    check_initiated()
    _ = performance.Timer("(Database) Checking if user exists")
    cursor.execute(
        "SELECT * FROM user WHERE id = %s", [user_id])
    if cursor.fetchone() is not None:
        return True
    return False

def get_all_activities_for_user(user_id:str):
    global cursor
    check_initiated()
    _ = performance.Timer("(Database) Getting all activities for user")
    cursor.execute(
        "SELECT * FROM activity WHERE user_id = %s", [user_id])
    return cursor.fetchall()

def get_all_trackpoints_for_activity(activity_id:str):
    global cursor
    check_initiated()
    _ = performance.Timer("(Database) Getting all trackpoints for activity")
    cursor.execute(
        "SELECT * FROM trackpoint WHERE activity_id = %s", [activity_id])
    return cursor.fetchall()

def get_all_valid_trackpoints(activity_id:str):
    global cursor
    check_initiated()
    _ = performance.Timer("(Database) Getting all valid trackpoints for activity")
    cursor.execute(Queries.get_all_valid_trackpoints_for_activity, [activity_id])
    return cursor.fetchall()

def insert_user(user_id:str, has_labels:bool):
    global cursor, db_connection
    check_initiated()
    _ = performance.Timer("(Database) Inserting user")
    cursor.execute(Queries.insert_user, (user_id, has_labels))
    db_connection.commit()

def insert_activity(id:str, user_id:str, transportation_mode:str, start_date_time:datetime.datetime, end_date_time:datetime.datetime):
    global cursor, db_connection
    check_initiated()
    _ = performance.Timer("(Database) Inserting activity")
    cursor.execute(Queries.insert_activity, (id, user_id, transportation_mode, start_date_time, end_date_time))
    db_connection.commit()

def insert_trackpoint(activity_id:str, lat:str, lon:str, altitude:str, date_days:str, date_time:datetime.datetime):
    global cursor, db_connection
    check_initiated()
    _ = performance.Timer("(Database) Inserting trackpoint")
    cursor.execute(Queries.insert_new_trackpoint, (activity_id, lat, lon, altitude, date_days, date_time))
    db_connection.commit()

def get_distinct_transportation_modes():
    global cursor
    check_initiated()
    _ = performance.Timer("(Database) Getting distinct transportation modes")
    cursor.execute(Queries.distinct_transportation_modes)
    return cursor.fetchall()

def get_users_longest_distance_one_day_per_trasnsportation_mode():
    global cursor
    check_initiated()
    _ = performance.Timer("(Database) Getting users longest distance one day per trasnportation mode")
    cursor.execute(Queries.get_users_longest_distance_one_day_per_trasnportation_mode)
    return cursor.fetchall()

def count_user_activity_transportation_mode(user_id: str, transportation_mode: str):
    global cursor
    check_initiated()
    _ = performance.Timer("(Database) Count user activity transportation mode")
    cursor.execute(Queries.count_user_activity_transportation_mode, [user_id, transportation_mode])
    return cursor.fetchone()[0]

def find_user_id_from_activity_id(activity_id: str):
    global cursor
    check_initiated()
    _ = performance.Timer("(Database) Find user id from activity id")
    cursor.execute(Queries.find_user_from_activity, [activity_id])
    return cursor.fetchone()[0]