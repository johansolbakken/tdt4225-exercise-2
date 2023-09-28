
import os
import log
import datetime
import config
import performance

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



def generate_activities_for_user(dataset_folder: str, user: User, activities: list[Activity]) -> None:
    data_folder = os.path.join(dataset_folder, 'Data')
    user_folder = os.path.join(data_folder, user.id)

    labels_file = os.path.join(user_folder, 'labels.txt')
    labels = []
    if os.path.isfile(labels_file):
        with open(labels_file, 'r') as f:
            labels = f.readlines()
            labels = [x.strip() for x in labels]

    trajectory_folder = os.path.join(user_folder, 'Trajectory')
    for activity_file in os.listdir(trajectory_folder):
        activity_id = activity_file.split('.')[0]

        trackpoints = generate_trackpoints_for(dataset_folder, user.id, activity_id)
        if len(trackpoints) > config.MAX_TRACKPOINT_SIZE:
            continue
        
        start_date_time = datetime.datetime.now()
        end_date_time = datetime.datetime(1900, 1, 1)

        for trackpoint in trackpoints:
            if trackpoint.date_time < start_date_time:
                start_date_time = trackpoint.date_time
            if trackpoint.date_time > end_date_time:
                end_date_time = trackpoint.date_time

        transportation_mode = ""

        activity = Activity(activity_id + user.id, user.id, transportation_mode, start_date_time, end_date_time)
        activity.trackpoints = trackpoints
        activities.append(activity)

def generate_dataset(dataset_folder:str) -> list[User]:
    users = []

    labeled_ids_file = os.path.join(dataset_folder, 'labeled_ids.txt')
    with open(labeled_ids_file, 'r') as f:
        labeled_ids = f.readlines()
        labeled_ids = [x.strip() for x in labeled_ids]

    data_folder = os.path.join(dataset_folder, 'Data')
    for id in os.listdir(data_folder):
        user = User(id, False)
        if id in labeled_ids:
            user.has_label = True

        generate_activities_for_user(dataset_folder, user, user.activities)
        if len(user.activities) == 0:
            continue

        users.append(user)

    return users