create_user_table = """
                    CREATE TABLE IF NOT EXISTS user (
                        id VARCHAR(255) PRIMARY KEY,
                        has_labels BOOLEAN NOT NULL
                    )
                    """


create_activity_table = """
                        CREATE TABLE IF NOT EXISTS activity (
                            id INT PRIMARY KEY,
                            user_id VARCHAR(255),
                            transportation_mode VARCHAR(255),
                            start_date_time DATETIME,
                            end_date_time DATETIME,
                            FOREIGN KEY (user_id) REFERENCES user(id) ON DELETE CASCADE ON UPDATE CASCADE
                        )
                        """

create_trackpoint_table = """
                          CREATE TABLE IF NOT EXISTS trackpoint (
                              id INT PRIMARY KEY,
                              activity_id INT,
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