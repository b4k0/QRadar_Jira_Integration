#!/usr/bin/python

# Import Libraries
import requests
import sys
import urllib3
import json
import re
from time import sleep

# Disable Warnings
urllib3.disable_warnings()


# Variables for Jira API
jira_url = sys.argv[1]
jira_pat = sys.argv[2]

# Variables for QRadar API
offenseID = sys.argv[3]
apiToken= sys.argv[4] 
endpoint = sys.argv[5]
magnitude_filter = sys.argv[6]
seconds = int(sys.argv[7])

# QRadar API URL
qradar_endpoint = "https://{0}/api/siem/offenses?fields=id%2C%20description%2C%20magnitude&filter=id%20%3D%20'{1}'".format(endpoint, offenseID)

# Jira API URL
jira_endpoint = jira_url


# Create a JIRA ticket based on QRadar offense
def create_jira_ticket(offense, magnitude):
    magnitude = str(magnitude)
    description = offense[0]['description']
    # Compose the JIRA ticket payload
    payload = json.dumps({
        'fields': {
            'project': {'key': 'Project Name'},
            'summary': 'QRadar Offense:' + ' ' + offenseID,
            'description': 'QRadar Offense Description:' + ' ' + description + '\n' + 'Magnitude:' + magnitude,
            'issuetype': {'name': 'Issue Type'} 
            }
        })

    # Send a POST request to create the JIRA ticket
    response = requests.post(jira_url, data=payload, headers={'Accept': 'application/json', 'Connection': 'keep-alive', 'Content-Type': 'application/json', 'Authorization': 'Bearer  {}'.format(jira_pat)}, timeout=60, verify=False)
    
    print(response.status_code)

    # Check if the JIRA ticket was created successfully
    if response.status_code == 201:
        print('JIRA ticket created successfully.')
        print(response.json())
    else:
        print('Failed to create JIRA ticket.')
        print(response.json())
        
# Retrieve QRadar offenses
def retrieve_qradar_offenses():

    # Send a GET request to retrieve QRadar offenses
    r = requests.get(qradar_endpoint, headers={'Accept': 'application/json', 'Connection': 'keep-alive', 'SEC': apiToken}, verify=False, timeout=60)
       
    print(r.status_code)
    
    # Check if the request was successful
    if r.status_code == 200:
        offense = r.json()
        # Extract relevant information from QRadar offense
        magnitude = offense[0]['magnitude']
        # print(magnitude)
        #Check if magnitude => 5
        if magnitude >= int(magnitude_filter):
            create_jira_ticket(offense,magnitude)
        else:
            print('Failed to Open QRadar Ticket due to magnitude.')
    else:
        print('Failed to retrieve QRadar offenses.')
        print(r.text)

# Main entry point
def main():
    sleep(seconds)
    print('Sleep mode finished!')
    retrieve_qradar_offenses()

if __name__ == '__main__':
    main()
