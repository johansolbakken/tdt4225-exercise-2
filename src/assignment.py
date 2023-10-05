import db as Database
import log
import tabulate
import algoritmo as Algoritmo


class Assignment:
    def task_2_1(self):
        number_of_users = Database.get_number_of_users()
        log.info(f"Number of users: {number_of_users}")

        number_of_activities = Database.get_number_of_activities()
        log.info(f"Number of activities: {number_of_activities}")

        number_of_trackpoints = Database.get_number_of_trackpoints()
        log.info(f"Number of trackpoints: {number_of_trackpoints}")

    def task_2_2(self):
        average_trackpoints_per_user = Database.get_average_trackpoints_per_user()
        log.info(f"Average trackpoints per user: {average_trackpoints_per_user}")

        max_trackpoints_per_user = Database.get_max_trackpoints_per_user()
        log.info(f"Max trackpoints per user: {max_trackpoints_per_user}")

        min_trackpoints_per_user = Database.get_min_trackpoints_per_user()
        log.info(f"Min trackpoints per user: {min_trackpoints_per_user}")

    def task_2_3(self):
        top_15_users_activities = Database.get_top_users_most_activites(15)
        log.info("Top 15 users with most activities:")
        print(tabulate.tabulate(top_15_users_activities, headers=["User ID", "Number of activities"]))

    def task_2_4(self):
        users_that_have_taken_the_bus = Database.get_all_users_that_used("bus")
        log.info("Users that have taken the bus:")
        print(tabulate.tabulate(users_that_have_taken_the_bus, headers=["User ID"]))

    def task_2_5(self):
        top_10_users_with_the_most_different_transportation_modes = Database.get_top_users_with_the_most_different_transportation_modes(10)
        log.info("Top 10 users with the most different transportation modes:")
        print(tabulate.tabulate(top_10_users_with_the_most_different_transportation_modes, headers=["User ID", "Number of different transportation modes"]))

    def task_2_6(self):
        duplicate_activities = Database.get_all_duplicate_activities()
        log.info("Duplicate activities:")
        print(tabulate.tabulate(duplicate_activities, headers=["User ID", "Activity ID", "Start date time", "End date time"]))

    def task_2_7_a(self): 
        users_with_activities_lasting_to_next_day = Database.get_amount_of_users_with_activities_lasting_to_next_day()
        log.info(f"Amount of users with activities lasting to the next day: {users_with_activities_lasting_to_next_day}")

    def task_2_7_b(self):
        user_transportation_mode_activities = Database.get_user_transportation_activity_hours_lasting_to_next_day(limit=True)
        log.info("Users with activities lasting to the next day (limit=15):")
        print(tabulate.tabulate(user_transportation_mode_activities, headers=["User ID", "Transportation mode", "duration (hours)"]))

    def task_2_8(self):
        count = Algoritmo.find_the_number_of_users_which_have_been_close_to_each_other_in_time_and_space()
        log.info(f"Number of users which have been close to each other in time and space: {count}")

    def task_2_9(self): 
        top_15_users_gained_most_elevation = Algoritmo.top_n_users_gained_most_elevation(15)
        log.info("Top 15 users gained most elevation:")
        print(tabulate.tabulate(top_15_users_gained_most_elevation, headers=["User ID", "Elevation gained (meters)"]))

    def task_2_10(self):
        for (transportation_mode,) in Database.get_distinct_transportation_modes(): 
            top = Algoritmo.top_users_a_day(transportation_mode, 10)
            log.info(f"Top 10 users with most distance traveled by {transportation_mode}:")
            print(tabulate.tabulate(top, headers=["User ID", "Transportation mode", "Distance (km)"]))

    def task_2_11(self):
        user_invalid_count = Algoritmo.users_count_invalid_activities()
        log.info("Users with invalid activities:")
        print(tabulate.tabulate(user_invalid_count, headers=["User ID", "Number of invalid activities"]))

    def task_2_12(self):
        user_favorite_transportation_mode = Algoritmo.users_favorite_transportation_mode()
        log.info("Users favorite transportation mode:")
        print(tabulate.tabulate(user_favorite_transportation_mode, headers=["User ID", "Transportation mode"]))

    ## IKKJE TENCH PA DAO)

    def comp(x):
        parts =  x.split("_")
        num1 = int(parts[1])
        num2 = int(parts[2])

        return num1 * 100 + num2

    def methods(self):
        methods = [method for method in dir(self) if callable(getattr(self, method)) and method.startswith("task")]
        methods.sort(key=Assignment.comp)
        return methods
    
    def format_title(self, title: str) -> str:
        tokens = title.split("_")
        
        tokens[0] = "Task"

        # insert "." between every pair of numbers
        for i in range(1, len(tokens)):
            if tokens[i].isdigit() and tokens[i - 1].isdigit():
                tokens[i] = f".{tokens[i]}"

        out = " ".join(tokens)
        out = out.replace(" .", ".")

        return out