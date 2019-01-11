#!/usr/bin/env python3

""" Creates a New Relic Synthetic monitor.
    reads user input for the Monitor name (label) & URL
    Works with API v3.
    To do: 1) use a different key. Currently using Mike's
    2) use a real function
"""
import json
import re
import requests
import sys

#NAME = str(input('Enter the Name: '))
#SITE = str(input('Enter the URL: '))
NAME = sys.argv[1]
SITE = sys.argv[2]

def main():
    """  Grab user input & post the json to New Relic
         Synthetics API.
         Read the output (combination of headers & json)
         match the value from "Location" key (it's a json list)
         slice the list to strip brackets & single quotes
         and assign that value to a variable used in the second
         request. The output should give two 201 status codes
         and the URL of the newly created monitor. Pay attention
         to the status codes. A 40X error will give you a lot
         of noise, and represents an attempt to create a monitor
         using the same name (label) as an existing monitor.
         A 50x status means something is way wrong.
         Only runs in python 3.
    """
    url = "https://synthetics.newrelic.com/synthetics/api/v3/monitors"
    values = {"name" : NAME, "type" : "SIMPLE", "frequency" : 15, "uri" : SITE,
              "locations" : ["AWS_EU_CENTRAL_1", "AWS_US_WEST_1",
                             "AWS_US_EAST_1"], "status": "ENABLED"
             }

    headers = {'Content-Type': 'application/json', 'X-Api-Key': '886933983d488b0df84adbcca780c231'}

    first_post = requests.post(url, data=json.dumps(values), headers=headers)
    print(first_post.status_code)
    #x = r.headers
    #print(x)
    #print(site)
    result = first_post.headers['Location']
    # grab the value from the Location key
    newresult = re.findall(r'\w+-\w+-\w+-\w+-\w+$', result)
    print(result)
    #print(newresult)
    # newresult is returned as a list, strip the brackets and single quotes
    monid = newresult[0]
    #print("monid", monid)

    url2 = "https://api.newrelic.com/v2/alerts_synthetics_conditions/policies/276078.json"
    values = {"synthetics_condition": {"name": "Check Failure", "monitor_id": monid,
                                       "runbook_url": "string", "enabled": "true"}}

    headers = {'Content-Type': 'application/json', 'X-Api-Key': '886933983d488b0df84adbcca780c231'}
    second_post = requests.post(url2, data=json.dumps(values), headers=headers)
    print(second_post.status_code)
    #print(second_post.headers)
main()
