
import os
import log
import datetime
import config
import performance
import pickle
import db as Database
import tabulate

class Trackpoint:
    def __init__(self, id: int, activity_id: int, lat: float, lon: float, altitude: float, date_days: float, date_time: datetime.datetime) -> None:
        self.id = id
        self.activity_id = activity_id
        self.lat = lat
        self.lon = lon
        self.altitude = altitude
        self.date_days = date_days
        self.date_time = date_time

class Activity:
    def __init__(self, id: int, user_id: str, transportation_mode: str, start_date_time: datetime.datetime, end_date_time: datetime.datetime) -> None:
        self.id = id
        self.user_id = user_id
        self.transportation_mode = transportation_mode
        self.start_date_time = start_date_time
        self.end_date_time = end_date_time

        self.trackpoints: list[Trackpoint] = []
class User:
    def __init__(self, id: str, has_label: bool) -> None:
        self.id = id
        self.has_label = has_label
        self.activities: list[Activity] = []
class Dataset:
    def __init__(self, users=[]) -> None:
        self.users = users

    def toJson(self):
        return [u.toJson() for u in self.users]

def generate_trackpoints_for(dataset_folder: str, user_id:str, activity_id:str) -> list[Trackpoint]:
    trackpoints = []

    # print every line from 7 to inf
    data_folder = os.path.join(dataset_folder, 'Data')
    trajectory_folder = os.path.join(data_folder, user_id, 'Trajectory')
    activity_file = os.path.join(trajectory_folder, activity_id + '.plt')

    with open(activity_file, 'r') as f:
        for (lineno,line) in enumerate(f):
            if lineno < 6:
                continue
            lat, lon, _, altitude, days, date, time = line.strip().split(',')

            # Todo: ta stilling til altitude
            if False and altitude == '-777':
                continue

            try:
                lat = float(lat)
            except ValueError:
                log.error(f'Could not convert lat={lat} to float, in file {activity_file} on line {lineno + 1}')
                exit(-1)

            try:
                lon = float(lon)
            except ValueError:
                log.error(f'Could not convert lon={lon} to float, in file {activity_file} on line {lineno + 1}')
                exit(-1)

            try:
                altitude = float(altitude)
            except ValueError:
                log.error(f'Could not convert altitude={altitude} to float, in file {activity_file} on line {lineno + 1}')
                exit(-1)

            try:
                date_days = float(days)
            except ValueError:
                log.error(f'Could not convert date_days={date_days} to float, in file {activity_file} on line {lineno + 1}')
                exit(-1)

            try:
                date_time = datetime.datetime.strptime(date + ' ' + time, '%Y-%m-%d %H:%M:%S')
            except ValueError:
                log.error(f'Could not convert date_time={date_time} to datetime, in file {activity_file} on line {lineno + 1}')
                exit(-1)

            trackpoint = Trackpoint(0,  activity_id + user_id, lat, lon, altitude, date_days, date_time)
            trackpoints.append(trackpoint)

    return trackpoints

class Label:
    def __init__(self, start_time: datetime.datetime, end_time: datetime.datetime, transportation_mode: str) -> None:
        self.start_time = start_time
        self.end_time = end_time
        self.transportation_mode = transportation_mode

def parse_label_file(path: str) -> list[Label]:
    labels = []

    with open(path, 'r') as f:
        first = True
        for line in f:
            if first:
                first = False
                continue
            start_date, end_date, transportation_mode = line.strip().split('\t')
            start_date_time = datetime.datetime.strptime(start_date, '%Y/%m/%d %H:%M:%S')
            end_date_time = datetime.datetime.strptime(end_date, '%Y/%m/%d %H:%M:%S')
            label = Label(start_date_time, end_date_time, transportation_mode)
            labels.append(label)

    return labels 

def generate_activities_for_user(dataset_folder: str, user: User, activities: list[Activity]) -> None:
    data_folder = os.path.join(dataset_folder, 'Data')
    user_folder = os.path.join(data_folder, user.id)

    labels_file = os.path.join(user_folder, 'labels.txt')
    labels = None
    if os.path.isfile(labels_file):
        labels = parse_label_file(labels_file)

    trajectory_folder = os.path.join(user_folder, 'Trajectory')
    for activity_file in os.listdir(trajectory_folder):
        activity_id = activity_file.split('.')[0]

        header_size = 6 # lines
        with open(os.path.join(trajectory_folder, activity_file), 'r') as f:
            if len(f.readlines()) - header_size > config.MAX_TRACKPOINT_SIZE:
                continue

        trackpoints = generate_trackpoints_for(dataset_folder, user.id, activity_id)
        if len(trackpoints) == 0:
            continue

        start_date_time = datetime.datetime.now()
        end_date_time = datetime.datetime(1900, 1, 1)

        for trackpoint in trackpoints:
            if trackpoint.date_time < start_date_time:
                start_date_time = trackpoint.date_time
            if trackpoint.date_time > end_date_time:
                end_date_time = trackpoint.date_time

        transportation_mode = ""
        if labels is not None:
            for label in labels:
                if label.start_time <= start_date_time and label.end_time >= end_date_time:
                    transportation_mode = label.transportation_mode
                    break

        activity = Activity(activity_id + user.id, user.id, transportation_mode, start_date_time, end_date_time)
        activity.trackpoints = trackpoints
        activities.append(activity)

def generate_dataset(dataset_folder:str) -> list[User]:
    _ = performance.Timer("Generate dataset")
    users = []

    labeled_ids_file = os.path.join(dataset_folder, 'labeled_ids.txt')
    with open(labeled_ids_file, 'r') as f:
        labeled_ids = f.readlines()
        labeled_ids = [x.strip() for x in labeled_ids]

    data_folder = os.path.join(dataset_folder, 'Data')

    for id in os.listdir(data_folder):
        # _ = performance.Timer("Generate dataset for user " + id)
        user = User(id, False)
        if id in labeled_ids:
            user.has_label = True

        generate_activities_for_user(dataset_folder, user, user.activities)
        if len(user.activities) == 0:
            continue

        users.append(user)
        # 👹👹👹👹👹👹👹👹👹👹👹👹👹👹👹👹👹👹👹👹👹🇪🇸🇪🇸🇪🇸🇪🇸🇪🇸🇪🇸
        # break

    return users

def write_dataset_to_cache(users: list[User], filename:str="data/memcache.pkl"):
    if not os.path.exists(os.path.dirname(filename)):
        os.makedirs(os.path.dirname(filename))
    with open(filename, 'wb') as f:
        pickle.dump(users, f)
   

def load_dataset_from_cache(filename:str="data/memcache.pkl") -> list[User]:
    with open(filename, 'rb') as f:
        users = pickle.load(f)
    return users    

def upload_data(data: list[User]=[]):
    _ = performance.Timer("(Database) Uploading data")
    for (i, user) in enumerate(data):
        # if already exists, skip
        log.enabled(False)
        if Database.user_exists(user.id):
            continue

        percentage = (i+1)/len(data) * 100
        _ = performance.Timer(f"\tUploading data for user {user.id} ({percentage:.2f}%)")

        if user.has_label:
            Database.insert_user(user.id, 1)
        else:
            Database.insert_user(user.id, 0)

        for activity in user.activities:
            Database.insert_activity(activity.id, activity.user_id, activity.transportation_mode, activity.start_date_time, activity.end_date_time)

            for trackpoint in activity.trackpoints:
                Database.insert_trackpoint(trackpoint.activity_id, trackpoint.lat, trackpoint.lon, trackpoint.altitude, trackpoint.date_days, trackpoint.date_time)
        log.enabled(True)

def get_whole_data_set() -> list[User]:
    _ = performance.Timer("Get whole data set")

    log.enabled(False)
    users_table = Database.get_all_users()
    users = []

    for user_row in users_table:
        user = User(user_row[0], user_row[1])

        activity_table = Database.get_all_activities_for_user(user.id)
        for activity_row in activity_table:
            activity = Activity(activity_row[0], activity_row[1], activity_row[2], activity_row[3], activity_row[4])

            trackpoint_table = Database.get_all_trackpoints_for_activity(activity.id)
            for trackpoint_row in trackpoint_table:
                trackpoint = Trackpoint(trackpoint_row[0], trackpoint_row[1], trackpoint_row[2], trackpoint_row[3], trackpoint_row[4], trackpoint_row[5], trackpoint_row[6])
                activity.trackpoints.append(trackpoint)

            user.activities.append(activity)
        users.append(user)

    log.enabled(True)

    return users

def get_all_users() -> list[User]:
    users_table = Database.get_all_users()
    users = []

    for user_row in users_table:
        user = User(user_row[0], user_row[1])
        users.append(user)

    return users

def get_all_activities_for_user(user_id: str) -> list[Activity]:
    activity_table = Database.get_all_activities_for_user(user_id)
    activities = []

    for activity_row in activity_table:
        activity = Activity(activity_row[0], activity_row[1], activity_row[2], activity_row[3], activity_row[4])
        activities.append(activity)

    return activities

def get_all_trackpoints_for_activity(activity_id: str) -> list[Trackpoint]:
    trackpoint_table = Database.get_all_trackpoints_for_activity(activity_id)
    trackpoints = []

    for trackpoint_row in trackpoint_table:
        trackpoint = Trackpoint(trackpoint_row[0], trackpoint_row[1], trackpoint_row[2], trackpoint_row[3], trackpoint_row[4], trackpoint_row[5], trackpoint_row[6])
        trackpoints.append(trackpoint)

    return trackpoints

