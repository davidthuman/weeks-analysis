#######################
### Import Packages ###
#######################

import requests
import pandas as pd
import authentication.credential as CR


########################
### Global Variables ###
########################

NOTION_TOKEN = CR.NOTION_TOKEN
BASE_URL = "https://api.notion.com/v1/"
BASE_HEADERS = {
    "accept": "application/json",
    "Notion-Version": "2022-06-28",
    "Authorization": NOTION_TOKEN
}

#######################
### Search Function ###
#######################

# search(payload) searches all original pages, databases, and child pages/databases that are shared with the integration.
def search(payload: dict={}):
    url = BASE_URL + "search"
    headers = BASE_HEADERS
    headers.update({"content-type": "application/json"})

    response = requests.post(url=url, json=payload, headers=headers)
    return response.json()

##########################
### Database Functions ###
##########################

# database(database_id) retrieves a Database object using the ID specified.
def database(database_id: str):
    url = BASE_URL + "databases/" + database_id

    response = requests.get(url=url, headers=BASE_HEADERS)
    return response.json()

# query_database(database_id, payload) gets a list of Pages contained in the database, 
# fitered and ordered according to the filter conditions and sort criteria provided in the request.
def query_database(database_id: str, payload: dict = {}):
    url = BASE_URL + "databases/" + database_id + "/query"
    headers = BASE_HEADERS
    headers.update({"content-type": "application/json"})

    response = requests.post(url=url, json=payload, headers=headers)
    return response.json()

######################
### Page Functions ###
######################

# page(page_id) retrieves a Page object using the ID specified.
def page(page_id: str):
    url = BASE_URL + "pages/" + page_id

    response = requests.get(url=url, headers=BASE_HEADERS)
    return response.json()

#######################
### Block Functions ###
#######################

# block(block_id) retrieves a Block object using the ID specified.
def block(block_id: str):
    url = BASE_URL + "blocks/" + block_id

    response = requests.get(url=url, headers=BASE_HEADERS)
    return response.json()

# block_children(block_id) returns a paginated array of children block objects contained in the block using
# the ID specified.
def block_children(block_id: str):
    url = BASE_URL + "blocks/" + block_id + "/children"

    response = requests.get(url=url, headers=BASE_HEADERS)
    return response.json()

########
###  ###
########

# get_timetables() returns a list of Block objects for Timetable databases
def get_timetables():

    # Page ID for 'Year 2023' that contains the WEEKS pages.
    page_id = "513f9a9b1ebc44f28a632db0b88c2ac7"

    # filter the 'Year 2023' page for WEEKS pages
    filter_for_weeks = lambda x: (x['type'] == 'child_page') and ('WEEK' in x['child_page']['title'])
    children = filter(filter_for_weeks, block_children(page_id)['results'])

    # filter the WEEKS pages for Timetable databases
    filter_for_timetables = lambda x: (x['type'] == 'child_database') and (x['child_database']['title'] == 'Timetable')
    result = [(child['child_page']['title'], next(filter(filter_for_timetables, block_children(child['id'])['results']))['id']) for child in children]
    
    return result

def extract_action(data: list):
    return "" if data == [] else data[0]["text"]["content"]

def notion_to_pandas(database_id: str):

    days = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
    week = query_database(database_id, payload={"sorts":[{"property": "Time", "direction": "ascending"}]})['results']
    data = list(map(lambda x: [x["properties"]["Time"]["title"][0]["text"]["content"]] + [extract_action(x["properties"][day]["rich_text"]) for day in days], week))
    return pd.DataFrame(data, columns=(['Time'] + days))