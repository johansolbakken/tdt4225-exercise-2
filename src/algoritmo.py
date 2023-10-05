import log as Log
import performance as Performance
import haversine
import model as Model
import db as Database

def find_the_number_of_users_which_have_been_close_to_each_other_in_time_and_space(min_radius_meter: float=50, min_time_sec: float=30) -> int:
    _ = Performance.Timer("(Algoritmo) find_the_number_of_users_which_have_been_close_to_each_other_in_time_and_space")
    return 0

def calculate_activity_elevation(activity: Model.Activity) -> float:
    s = 0
    trackpoints = Database.get_all_valid_trackpoints(activity.id)
    for i in range(len(trackpoints) - 1):
        tn = trackpoints[i][0]
        tn1 = trackpoints[i + 1][0]
        if tn < tn1:
            s += tn1 - tn
    return s

def find_highest_elevation(user: Model.User) -> float:
    highest = 0
    activities = Model.get_all_activities_for_user(user.id)
    for activity in activities:
        activity_elevation = calculate_activity_elevation(activity)
        if activity_elevation > highest:
            highest = activity_elevation
    return highest

def top_n_users_gained_most_elevation(n: int=15):
    _ = Performance.Timer("(Algoritmo) top_n_users_gained_most_elevation")
    Log.enabled(False)
    
    elevators = []
    users = Model.get_all_users()
    for user in users:
        highest_elevation = find_highest_elevation(user)
        elevators.append((user.id, highest_elevation))

    Log.enabled(True)

    elevators.sort(key=lambda x: x[1], reverse=True)

    return elevators[:min(n, len(elevators))]

def top_users_a_day(transportation_mode:str, limit:int=10):
    longest = Database.get_users_longest_distance_one_day_per_trasnsportation_mode()
    longest = [l for l in longest if l[1] == transportation_mode]
    total_per_user = {}
    for user_id, _, distance in longest:
        if user_id not in total_per_user:
            total_per_user[user_id] = 0
        total_per_user[user_id] += distance
    total_per_user = [(k, v) for k, v in total_per_user.items()]
    total_per_user.sort(key=lambda x: x[1], reverse=True)
    return total_per_user[:min(limit, len(total_per_user))]
