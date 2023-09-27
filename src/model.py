
import os
import log
import datetime

# Insert Users


class User:
    def __init__(self, id: str, has_label: bool) -> None:
        self.id = id
        self.has_label = has_label


def generate_users(dataset_folder=str) -> list[User]:
    users = []

    labeled_ids_file = os.path.join(dataset_folder, 'labeled_ids.txt')
    with open(labeled_ids_file, 'r') as f:
        labeled_ids = f.readlines()
        labeled_ids = [x.strip() for x in labeled_ids]

    data_folder = os.path.join(dataset_folder, 'Data')
    for id in os.listdir(data_folder):
        if id in labeled_ids:
            users.append(User(id, True))
        else:
            users.append(User(id, False))

    return users

# Insert Trackpoints

class Trackpoint:
    def __init__(self, id: int, activity_id: int, lat: float, lon: float, altitude: float, date_days: str, date_time: str) -> None:
        self.id = id
        self.activity_id = activity_id
        self.lat = lat
        self.lon = lon
        self.altitude = altitude
        self.date_days = date_days
        self.date_time = date_time

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
            lat, lon, _, altitude, _, date_days, date_time = line.strip().split(',')

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

            trackpoint = Trackpoint(0, activity_id, lat, lon, altitude, date_days, date_time)
            trackpoints.append(trackpoint)

    return trackpoints



# Insert Activities

class Activity:
    def __init__(self, id: int, user_id: str, transportation_mode: str, start_date_time: datetime.datetime, end_date_time: datetime.datetime) -> None:
        self.id = id
        self.user_id = user_id
        self.transportation_mode = transportation_mode
        self.start_date_time = start_date_time
        self.end_date_time = end_date_time


def generate_activities(dataset_folder: str, users: list[User]) -> list[Activity]:
    activities = []

    data_folder = os.path.join(dataset_folder, 'Data')
    for (i,user) in enumerate(users):
        user_folder = os.path.join(data_folder, user.id)

        labels_file = os.path.join(user_folder, 'labels.txt')
        labels = []
        if os.path.isfile(labels_file):
            with open(labels_file, 'r') as f:
                labels = f.readlines()
                labels = [x.strip() for x in labels]

        trajectory_folder = os.path.join(user_folder, 'Trajectory')
        for activity_file in os.listdir(trajectory_folder):
            activity_file_path = os.path.join(trajectory_folder, activity_file)

            activity_id = activity_file.split('.')[0]

            trackpoints = generate_trackpoints_for(dataset_folder, user.id, activity_id)
            
            start_date_time = datetime.datetime.now()
            end_date_time = datetime.datetime(1900, 1, 1)

            for trackpoint in trackpoints:
                date = trackpoint.date_days
                time = trackpoint.date_time
                trackpoint_time = datetime.datetime.strptime(date + ' ' + time, '%Y-%m-%d %H:%M:%S')

                if trackpoint_time < start_date_time:
                    start_date_time = trackpoint_time
                if trackpoint_time > end_date_time:
                    end_date_time = trackpoint_time

            transportation_mode = ""

            activity = Activity(activity_id, user.id, transportation_mode, start_date_time, end_date_time)
            activities.append(activity)

    return activities