#!/usr/bin/env python3

import urllib.request
import urllib.parse
import json

import pathlib
import shutil

def setup_request(url, query=None):
    if query:
        url = "{}?{}".format(url, urllib.parse.urlencode(query))
    request = urllib.request.Request(url)
    request.add_header("User-Agent", "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.182 Safari/537.36 OPR/74.0.3911.203")
    return request

def get_json(url, query=None):
    request = setup_request(url, query)
    print("> get_json {}".format(request.full_url))
    with urllib.request.urlopen(request) as response:
        return json.load(response)

def get_file(url, file_name, query=None):
    request = setup_request(url, query)
    file_name = pathlib.Path(__file__).parent.absolute() / file_name
    file_name.parent.mkdir(parents=True, exist_ok=True)
    print("> get_file {} -> {}".format(request.full_url, file_name))
    with urllib.request.urlopen(request) as response, open(file_name, "wb") as out_file:
        return shutil.copyfileobj(response, out_file)

print("Downloading available databases...")
databases_url = "https://api.wow.tools/databases/"
database_names = dict(map(lambda x: (x["displayName"], x["name"]), get_json(databases_url)))

versions_url = "https://api.wow.tools/databases/{}/versions/"
database_versions = dict()
needed_databases = ["SpellEffect", "SpellCastTimes"]
print("Downloading database versions...")
for db_name in needed_databases:
    if db_name not in database_names:
        raise Exception("missing database {}".format(db_name))
    database_versions[db_name] = get_json(versions_url.format(database_names[db_name]))[0]

print("Downloading database csvs...")
csv_url = "https://wow.tools/dbc/api/export/"
for db_name in needed_databases:
    query = {
            "name": database_names[db_name],
            "build": database_versions[db_name],
            }
    get_file(csv_url, "csvs/{}_{}.csv".format(db_name, database_versions[db_name]), query)

