#!/usr/bin/python

import requests
import sys
import urllib3
import json

# Disable warning
urllib3.disable_warnings()

# Variables for Jira API Request
jira_url = sys.argv[1]
jira_pat = sys.argv[2]
offenseID = sys.argv[3]

# Payload of Jira API Request
payload = json.dumps({
    'fields': {
        'project': {'key': 'Project Name'},
        'summary': 'Test QRadar Offense:' + ' ' + offenseID,
        'issuetype': {'name': 'Issue Type'} 
        }
    })

# Header of Jira API Request using Personal Access Token
header={'Accept': 'application/json', 'Connection': 'keep-alive', 'Content-Type': 'application/json', 'Authorization': 'Bearer  {}'.format(jira_pat)}

# POST Request to create the JIRA ticket
response = requests.post(jira_url, data=payload, headers=header, timeout=60, verify=False)


# Check if the JIRA ticket was created successfully
if response.status_code == 201:
    print('JIRA ticket created successfully.')
    print(response.json())
else:
    print('Failed to create JIRA ticket.')
    print(response.json())