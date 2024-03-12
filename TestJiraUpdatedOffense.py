#!/usr/bin/python3

import requests
import sys
import urllib3
import json
import re

urllib3.disable_warnings()

jira_url = sys.argv[1]
jira_pat = sys.argv[2]
offense = sys.argv[3]
project = sys.argv[4]
issue_type = sys.argv[5]

# Search for jira issues with a specific offense ID
endpoint =  "https://{0}/rest/api/2/search?jql=project%20%3D%20{1}%20%26%20issuetype%20%3D%20{2}%20%26%20'Alert Link'%20%7E%20{3}&fields=project%2C%20issuetype%2C%20customfield_19101%2C%20customfield_19103".format(jira_url, project, issue_type, offense)

rJira = requests.get(endpoint, headers={'Accept': 'application/json', 'Connection': 'keep-alive', 'Content-Type': 'application/json', 'Authorization': 'Bearer  {}'.format(jira_pat)}, timeout=60, verify=False)
print(rJira.status_code)
print(rJira.elapsed.total_seconds())
if rJira.status_code == 200:
    JiraJSON = rJira.json()
    print(JiraJSON)
    print(len(JiraJSON))
    print(JiraJSON['issues'])
# Check if there is Jira issue with specific offense ID
    if len(JiraJSON['issues']) <= 0 :
        print("There is not any issue with this offense ID")
    else:
# Extract relevant information from QRadar offense on Jira
        offense = JiraJSON['issues'][0]['fields']['customfield_19101']
        magnitude = JiraJSON['issues'][0]['fields']['customfield_19103']
        key = JiraJSON['issues'][0]['key']
        print(str(magnitude))
        print(magnitude)
        print(key)
        print("Issue found with this offense ID" + " " + offense)
        
