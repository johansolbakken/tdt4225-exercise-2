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

# Part 2

number_of_users = "SELECT COUNT(*) FROM user"

number_of_activities = "SELECT COUNT(*) FROM activity"

number_of_trackpoints = "SELECT COUNT(*) FROM trackpoint"

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