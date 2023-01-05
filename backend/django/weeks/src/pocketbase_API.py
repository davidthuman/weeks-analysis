#######################
### Import Packages ###
#######################

import datetime
import requests
import pandas as pd
# from pocketbase import PocketBase (This library is currently out-dated)
import authentication.credential as CR

import src.recap as RP
import src.extra as EX
import datetime
from IPython.display import clear_output

########################
### Global Variables ###
########################

BASE_URL = "http://127.0.0.1:8090"
ADMIN_EMAIL = CR.POCKETBASE_ADMIN_EMAIL
ADMIN_PASSWORD = CR.POCKETBASE_ADMIN_PASSWORD
POCKETBASE_AUTH_TOKEN = CR.POCKETBASE_AUTH_TOKEN

######################
### Authenitcation ###
######################

def admin_auth_with_password():

    url = BASE_URL + "/api/admins/auth-with-password"
    body = {"identity": ADMIN_EMAIL, "password": ADMIN_PASSWORD}
    response = requests.post(url=url, json=body, params={}, headers={})
    return response

########################
### Levels Functions ###
########################

def get_levels(level: str, params: dict = {}, full: bool = True):

    url = BASE_URL + f"/api/collections/{level}/records"
    headers = {"Authorization": POCKETBASE_AUTH_TOKEN}
    response = requests.get(url=url, params=params, headers=headers)
    if (full):
        return response
    else:
        items = response.json()['items']
        reduced_items = map(lambda x: {x['classification']: x['id']}, items)
        result = {}
        for x in list(reduced_items):
            result.update(x)
        return result

def post_level(level: str, json: dict, full: bool = True):

    url = BASE_URL + f"/api/collections/{level}/records"
    headers = {"Authorization": POCKETBASE_AUTH_TOKEN}
    response = requests.post(url=url, json=json, params={}, headers=headers)
    if (full):
        return response
    else:
        return {response.json()['classification']: response.json()['id']}


#########################
### Actions Functions ###
#########################

def get_actions(params: dict = {}, full: bool = True):

    url = BASE_URL + "/api/collections/actions/records"
    headers = {"Authorization": POCKETBASE_AUTH_TOKEN}
    response = requests.get(url=url, params=params, headers=headers)
    if (full):
        return response
    else:
        items = response.json()['items']
        reduced_items = map(lambda x: {x['action']: x['id']}, items)
        result = {}
        for x in list(reduced_items):
            result.update(x)
        return result

def post_action(json: dict):

    url = BASE_URL + "/api/collections/actions/records"
    headers = {"Authorization": POCKETBASE_AUTH_TOKEN}
    response = requests.post(url=url, json=json, params={}, headers=headers)
    return response

def patch_action(id: str, json: dict):

    url = BASE_URL + f"/api/collections/actions/records/{id}"
    headers = {"Authorization": POCKETBASE_AUTH_TOKEN}
    response = requests.patch(url=url, json=json, headers=headers)
    return response

def get_action_by_name(name: str):

    # If the action already exists in the database
    if ((pre_action := get_actions(params={"filter": f'action="{name}"'}, full=False)) != {}):
        return pre_action
    # If the action does not exist in the database
    else:
        data = post_action(json={"action": name}).json()
        return {data['action']: data['id']}


####################
### Era Function ###
####################

def get_eras(params: dict, full: bool = True):

    url = BASE_URL + "/api/collections/eras/records"
    headers = {"Authorization": POCKETBASE_AUTH_TOKEN}
    response = requests.get(url=url, params=params, headers=headers)
    if (full):
        return response
    else:
        items = response.json()['items']
        reduced_items = map(lambda x: {x['era']: x['id']}, items)
        result = {}
        for x in list(reduced_items):
            result.update(x)
        return result

def post_era(json: dict):

    url = BASE_URL + "/api/collections/eras/records"
    headers = {"Authorization": POCKETBASE_AUTH_TOKEN}
    response = requests.post(url=url, json=json, params={}, headers=headers)
    return response

######################
### Days Functions ###
######################

def get_days(params: dict, full: bool = True):

    url = BASE_URL + '/api/collections/days/records'
    headers = {"Authorization": POCKETBASE_AUTH_TOKEN}
    response = requests.get(url=url, params=params, headers=headers)
    if (full):
        return response
    else:
        items = response.json()['items']
        reduced_items = map(lambda x: {x['date']: x['id']}, items)
        result = {}
        for x in list(reduced_items):
            result.update(x)
        return result

def post_day(json: dict):

    url = BASE_URL + '/api/collections/days/records'
    headers = {"Authorization": POCKETBASE_AUTH_TOKEN}
    response = requests.post(url=url, json=json, headers=headers)
    return response

def patch_day(id: str, json: dict):

    url = BASE_URL + f"/api/collections/days/records/{id}"
    headers = {"Authorization": POCKETBASE_AUTH_TOKEN}
    response = requests.patch(url=url, json=json, headers=headers)
    return response
    
##########################
### DateTime Functions ###
##########################

def create_eastern_datetime(dt_date: datetime.datetime, time: str):

    # Eastern Standard Time
    timezone = datetime.timezone(offset=datetime.timedelta(hours=-5), name='EST')

    # Check if EST is correct for date range, if false, switch to Eastern Daylight Time (EDT)
    check = datetime.datetime.combine(dt_date, datetime.time(tzinfo=timezone)).astimezone()
    if (check.tzinfo != timezone):
        timezone = datetime.timezone(offset=datetime.timedelta(hours=-4), name='EDT')

    # Create datetime time
    hours = int(time.split(':')[0])
    minutes = int(time.split(':')[1])
    dt_time = datetime.time(hour=hours, minute=minutes, tzinfo=timezone)

    # Create final datetime
    final_dt = datetime.datetime.combine(dt_date, dt_time)

    return final_dt

def text_to_date(date: str):

    # Create datetime date
    return datetime.datetime.strptime(date, "%m/%d/%Y")

# to_UTC(dt, text) returns a datetime object if `text` is False, or a string format in `text` is True
def to_UTC(dt: datetime.datetime, text: bool = False):

    if (text):
        return dt.astimezone(tz=datetime.timezone(offset=datetime.timedelta(hours=0))).isoformat(' ')[:-6]
    else:
        return dt.astimezone(tz=datetime.timezone(offset=datetime.timedelta(hours=0)))

def create_dataframes(folder: str, class_links: dict):
    
    # Defining an empty list to hold strings that represent file locations
    weeks_files = []

    # For Loop to create strings that represent the file location of exported .csv files from Notion
    for x in range(1, 16):
        try:
            file = f"../database/weeks_data/{folder}/Week{str(x)}.csv"
            weeks_files.append(file)
        except:
            continue

    # Defining an empty list to hold Pandas Dataframe of the previously mentioned Notion .csv files
    weeks_df = []

    # For Loop to create, and clean multipe Dataframes to represent a week
    for x in range(15):
        try:
            df = pd.read_csv(weeks_files[x])
            time = pd.DataFrame(EX.military_time())
            df = df.drop(df.columns[[0]], axis=1)
            df = pd.concat([time, df], axis=1)
            df.columns = pd.Index(['Time', 'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday','Sunday'], dtype='object')
            df = df.replace(class_links)
            df = df.replace(to_replace=r'^https://www.notion.so/.*$', value="PIKE Meeting", regex=True)
            weeks_df.append(df.fillna("Unknown"))
        except Exception:
            continue

    return weeks_df

############################
### Population Functions ###
############################

# populate_database(level, data) will update the database with the actions found
# in data. `level` is used to gather the classifications. `data` should be in the 
# form of a dictionary with keys as classifications for the given `level` and values
# as lists of actions.
def populate_actions(level: str, data: dict):

    # Get the current classifications for the level
    cats = get_levels(level=level, full=False)

    # Loop through all the classifications
    for cat in list(data.keys()):

        # Get the set of all actions
        # actions = set(data[cat]["weekday"] + data[cat]["weekend"])
        actions = set(data[cat])

        # Loop through all the actions
        for action in actions:

            # If the classication in NOT in the level's collection
            if (cats.get(cat, 0) == 0):
                # Add the classification to the level's collection
                new_cat = post_level(level=level, json={"classification": cat}, full=False)
                # Update the current classifications
                cats.update(new_cat)

            # If the action is already in the collection
            if ((pre_action := get_actions(params={"filter": f'action="{action}"'}, full=False)) != {}):
                # Patch the action with the current level's classification
                patch_action(pre_action[action], json={level: cats[cat]})
                continue

            # Update the action's collection
            post_action({"action": action, level: cats[cat]})


def populate_days(folder: str, begin: str, era: str, class_links: dict):

    dataframes = create_dataframes(folder=folder, class_links=class_links)

    days = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday','Sunday']

    split_index = 72

    eras = get_eras(params={}, full=False)


    # Define the starting datetime date
    dt_date = text_to_date(date=begin)

    # Define pointer variables
    front_actions = pd.DataFrame() # actions from 00:00 to 05:45
    back_actions = [] # actions from 06:00 to 23:45

    # Loop through all weeks
    for week in dataframes:

        past_day = 'Sunday'

        # Loop through all days
        for day_index, day in enumerate(days):

            # Check if there are actions from 00:00 to 05:45
            if (front_actions.shape[0] != 0):
                
                # Loop through all actions from 00:00 to 05:45
                for index, time_action in front_actions.iterrows():

                    # Create time-string
                    eastern = create_eastern_datetime(dt_date=dt_date, time=time_action['Time'])
                    utc = to_UTC(dt=eastern, text=True)
                    # Get action's ID
                    action_name = time_action[past_day]
                    action_dict = get_action_by_name(name=action_name)
                    # Post day with date-string, era_ID, and action_ID
                    clear_output(wait=True)
                    print(f"Processing date {utc}")
                    post_day(json={"date": utc, "era": eras[era], "action": action_dict[action_name]})


            back_actions = week[['Time', day]].iloc[:split_index]

            # Loop through all actions from 06:00 to 23:45
            for index, time_action in back_actions.iterrows():

                # Create time-string
                eastern = create_eastern_datetime(dt_date=dt_date, time=time_action['Time'])
                utc = to_UTC(dt=eastern, text=True)
                # Get action's ID
                action_name = (time_action[day]).replace('"', "'")
                action_dict = get_action_by_name(name=action_name)
                # Post day with date-string, era_ID, and action_ID
                clear_output(wait=True)
                print(f"Processing date {utc}")
                post_day(json={"date": utc, "era": eras[era], "action": action_dict[action_name]})

            # Update front_actions
            front_actions = week[['Time', day]].iloc[split_index:]
            # Update datetime date
            dt_date = dt_date + datetime.timedelta(days=1)
            # Update past day
            past_day = day

    # Final Loop through front_actions pointer
    # Loop through all actions from 00:00 to 05:45
    for index, time_action in front_actions.iterrows():

        # Create time-string
        eastern = create_eastern_datetime(dt_date=dt_date, time=time_action['Time'])
        utc = to_UTC(dt=eastern, text=True)
        # Get action's ID
        action_name = time_action[past_day]
        action_dict = get_action_by_name(name=action_name)
        # Post day with date-string, era_ID, and action_ID
        post_day(json={"date": utc, "era": eras[era], "action": action_dict[action_name]})
