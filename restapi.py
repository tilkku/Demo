#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Class for getting covid-19 information of certain areas in Finland from Finnish Institute for Health and Welfare (THL) database.
For now this class gets covid-19 information from Varsinais-Suomi, Pirkanmaa and Helsinki ja Uusimaa areas as JSON format. 
For the THL database restrictions the user agent is changed to refer to Chrome. 

THL database have unique id:s for all areas in Finland. 
- "haeData" -method gets new data from the THL database
- "idAreas" -list includes all the unique area id:s that we want to get from the THL database. This list is being used to build querystring parameters. 
"cases" and "labels" -lists are produced from the response JSON.
- "cases" -list includes total covid-19 cases of the areas respective to "idAreas" -list.
- "labels" -list includes labels of the areas respective to "idAreas" -list.
"""

import requests 
import random

# THL API for covid-19 cases by area in Finland
url ="https://sampo.thl.fi/pivot/prod/fi/epirapo/covid19case/fact_epirapo_covid19case.json"

# THL API id:s of the areas of interest into lists
# Varsinais-Suomen SHP, Raisio, Turku, Pirkanmaan SHP, Tampere, Helsingin ja Uudenmaan SHP, Helsinki, Koko Suomi
idAreas=["445197","445021","445257","445282","445081","445193","445171","445222"]
idVS=["445197","445021","445257"]
idPM=["445282","445081"]
idHUS=["445193","445171"]
idS=["445222"]

# Build string of row parameters for the query
querystringRow = "hcdmunicipality2020-"
for idArea in idAreas:
    querystringRow = querystringRow+idArea+"."
querystring = {"row": querystringRow, "column": "dateweek2020010120201231-443686.", "filter": "measure-444833"} 

# Change agent headers refer to Chrome randomly changing
# User agent list
user_agents = [
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_5) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/13.1.1 Safari/605.1.15",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:77.0) Gecko/20100101 Firefox/77.0",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.97 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:77.0) Gecko/20100101 Firefox/77.0",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.97 Safari/537.36",
]
#Pick a random user agent
user_agent = random.choice(user_agents)
#Set the headers 
headers = {"User-Agent": user_agent}

# Get new data from THL API
def haeData():
    '''
    Get new data from THL API 
    Return two lists:
    - first a list including area labels 
    - second a list including corresponding total covid-19 cases
    '''
    response = requests.request("GET", url, headers=headers, params=querystring)
    jsonResponse=response.json()

    # List of total covid cases respective to the area id:s in idAreas 
    cases = []
    count = 0
    while count < len(idAreas):
        cases.insert(count, jsonResponse['dataset']['value'][str(count)])
        count += 1

    # List of area labels respective to the id:s in idAreas
    labels = []
    count = 0
    while count < len(idAreas):
        # Change "Kaikki Alueet" label to "Koko Suomi"
        if idAreas[count]=="445222":
            labels.insert(count, "Koko Suomi")
        else:
            labels.insert(count, jsonResponse['dataset']['dimension']['hcdmunicipality2020']['category']['label'][idAreas[count]])
        count += 1

    return labels, cases



