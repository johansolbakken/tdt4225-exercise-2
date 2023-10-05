"""
file: queries.py
written by: Johan Solbakken, Morten Tobias Rinde Sunde
date: 05.10.2023

    Contains all the queries used in the project.
    
"""

create_user_table = """
                    CREATE TABLE IF NOT EXISTS user (
                        id VARCHAR(255) PRIMARY KEY,
                        has_labels BOOLEAN NOT NULL
                    )
                    """


create_activity_table = """
                        CREATE TABLE IF NOT EXISTS activity (
                            id BIGINT PRIMARY KEY,
                            user_id VARCHAR(255),
                            transportation_mode VARCHAR(255),
                            start_date_time DATETIME,
                            end_date_time DATETIME,
                            FOREIGN KEY (user_id) REFERENCES user(id) ON DELETE CASCADE ON UPDATE CASCADE
                        )
                        """


create_trackpoint_table = """
                          CREATE TABLE IF NOT EXISTS trackpoint (
                              id BIGINT PRIMARY KEY AUTO_INCREMENT,
                              activity_id BIGINT,
                              lat DOUBLE,
                              lon DOUBLE,
                              altitude INT,
                              date_days DOUBLE,
                              date_time DATETIME,
                              FOREIGN KEY (activity_id) REFERENCES activity(id) ON DELETE CASCADE ON UPDATE CASCADE
                          )
                          """

indexes = [
    ["altitude", "CREATE INDEX altitude_index ON trackpoint (altitude)", "DROP INDEX altitude_index ON trackpoint"],
]

insert_user = """
                INSERT INTO user (id, has_labels)
                VALUES (%s, %s)
                """

insert_activity = """
                    INSERT INTO activity (id, user_id, transportation_mode, start_date_time, end_date_time)
                    VALUES (%s, %s, %s, %s, %s)
                    """

insert_new_trackpoint = """
                    INSERT INTO trackpoint (activity_id, lat, lon, altitude, date_days, date_time)
                    VALUES (%s, %s, %s, %s, %s, %s)
                    """

# ---------- Part 2 ----------

# 2.1
number_of_users = "SELECT COUNT(*) FROM user"

number_of_activities = "SELECT COUNT(*) FROM activity"

number_of_trackpoints = "SELECT COUNT(*) FROM trackpoint"

# 2.2
average_trackpoint_per_user = """SELECT AVG(t.amount)FROM (
                                    SELECT COUNT(trackpoint.id) as amount
                                    FROM trackpoint JOIN activity ON trackpoint.activity_id = activity.id JOIN user ON user.id = activity.user_id
                                    GROUP BY user_id) as t"""

most_trackpoint_per_user = """SELECT MAX(t.amount)FROM (
                                SELECT COUNT(trackpoint.id) as amount
                                FROM trackpoint JOIN activity ON trackpoint.activity_id = activity.id JOIN user ON user.id = activity.user_id
                                GROUP BY user_id) as t"""

least_trackpoint_per_user = """SELECT MIN(t.amount)FROM (
                                SELECT COUNT(trackpoint.id) as amount
                                FROM trackpoint JOIN activity ON trackpoint.activity_id = activity.id JOIN user ON user.id = activity.user_id
                                GROUP BY user_id) as t"""

# 2.3
top_users_most_activites = """SELECT user.id, COUNT(activity.id)
                                FROM user JOIN activity on user.id = user_id
                                GROUP BY user_id
                                ORDER BY -COUNT(activity.id)
                                LIMIT %s"""

# 2.4
users_that_have_taken_transportation_mode = """
                                            SELECT DISTINCT user_id 
                                            FROM user join activity on user.id = user_id
                                            WHERE transportation_mode = %s
                                            """

# 2.5
top_users_with_the_most_different_transportation_modes = """SELECT user_id, COUNT(DISTINCT transportation_mode)
                                                            FROM activity
                                                            GROUP BY user_id
                                                            ORDER BY -COUNT(DISTINCT transportation_mode)
                                                            LIMIT %s"""

# 2.6 
duplicate_activities = """
                        SELECT a1.user_id, a1.id, a1.start_date_time, a1.end_date_time
                        FROM activity as a1, activity as a2
                        WHERE a1.id != a2.id AND a1.transportation_mode = a2.transportation_mode 
                                            AND a1.start_date_time = a2.start_date_time 
                                            AND a1.end_date_time = a2.end_date_time 
                                            AND a1.user_id = a2.user_id
"""

# 2.7a 
users_with_activities_lasting_to_next_day = """
                        SELECT COUNT(distinct user_id) as antall
                        FROM activity
                        WHERE day(start_date_time) + 1 = day(end_date_time) 
                            AND month(start_date_time) = month(end_date_time)
                            AND year(start_date_time) = year(end_date_time)"""

# 2.7b
user_transportation_mode_activity_hours = """
                        SELECT user_id, transportation_mode, timestampdiff(MINUTE,start_date_time,end_date_time) / 60 as hours
                        FROM activity
                        WHERE day(start_date_time) + 1 = day(end_date_time) 
                            AND month(start_date_time) = month(end_date_time)
                            AND year(start_date_time) = year(end_date_time)"""

get_all_users = "SELECT * FROM user"

get_all_activities = "SELECT * FROM activity"

get_all_trackpoints = "SELECT * FROM trackpoint"

get_all_valid_trackpoints_for_activity = """SELECT altitude
                                            FROM trackpoint
                                            WHERE activity_id = %s
                                                AND altitude != -777
                                            ORDER BY date_time"""

distinct_transportation_modes = """SELECT DISTINCT transportation_mode
                                    FROM activity
                                    WHERE activity.transportation_mode != "";"""


# 10. 
# Find the users that have traveled the longest total distance in one day for each transportation mode. 

get_users_longest_distance_one_day_per_trasnportation_mode = """
                        SELECT user_id,
                        transportation_mode,
                        TIMESTAMPDIFF(MINUTE, start_date_time, end_date_time) / 60 AS hours
                        FROM activity
                        WHERE DAY(start_date_time) = DAY(end_date_time)
                        AND MONTH(start_date_time) = MONTH(end_date_time)
                        AND YEAR(start_date_time) = YEAR(end_date_time)
                        AND transportation_mode != "";
                            """

count_user_activity_transportation_mode = """
    SELECT COUNT(*) FROM activity WHERE user_id = %s AND transportation_mode = %s AND transportation_mode != ""
"""

find_user_from_activity = """SELECT user_id FROM activity WHERE id = %s"""