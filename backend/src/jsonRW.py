import json


def read_json(fileName):
    filePath = f'../weeks_data/json_data/{fileName}.json'
    file = open(filePath)
    return json.load(file)

def write_json(fileName, newJSON):
    filePath = f'../weeks_data/json_data/{fileName}.json'
    with open(filePath, "w") as outfile:
        outfile.write(f"{newJSON}")

def read_class_link(fileName):
    json_read = read_json(fileName)
    return json_read['class_link']

def write_analysis(fileName, analysis):
    json_read = read_json(fileName)
    analysis_read = json_read['analysis']
    analysis_read.update(analysis)
    write_json(fileName, json.dumps(json_read, indent=4))

def write_level(fileName, level, level_data):
    json_read = read_json(fileName)
    level_one_read = json_read['classification'][level]
    level_one_read.update(level_data)
    write_json(fileName, json.dumps(json_read, indent=4))

def read_level(fileName, level):
    json_read = read_json(fileName)
    return json_read['classification'][level]