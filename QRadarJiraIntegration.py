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
offense = sys.argv[3]
apiToken= sys.argv[4] 
endpoint = sys.argv[5]
magnitude_filter = sys.argv[6]
seconds = int(sys.argv[7])

# QRadar API URL
qradar_endpoint = "https://{0}/api/siem/offenses?fields=id%2C%20description%2C%20magnitude&filter=id%20%3D%20'{1}'".format(endpoint, offenseID)

# Jira API URL
jira_endpoint = jira_url


# Create a JIRA ticket based on QRadar offense
def create_jira_ticket(magnitude, description, domain_id, offenses_type, offense_source):
    magnitude_int = int(magnitude)
    print(magnitude_int)
    # Compose the JIRA ticket payload
    payload = json.dumps({
        'fields': {
             'project': {'key': 'Project Name'},
            'summary': 'Security Incident on ' + ' ' + offenses_type + ' ' + offense_source + ' ' + '-' + ' ' + offense,
            'description': 'QRadar Offense Description: ' + ' ' + description + '\n' + 'Magnitude: ' + ' ' + magnitude + '\n' + 'Domain: ' + ' ' + domain_id + '\n' + 'Offense Type: ' + ' ' + offenses_type + '\n' + 'Offense Source: ' + ' ' + offense_source,
            'issuetype': {'name': 'Issue Type'},
            'customfield_19101': offense,
            'customfield_19103': magnitude_int,
            'customfield_19302': domain_id,
            'customfield_18502': { 'value': 'Service Type'}
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
        offenseJSON = r.json()
        print(offenseJSON)
        print(len(offenseJSON))
        # Extract relevant information from QRadar offense
        print(offenseJSON[0])
        magnitude = offenseJSON[0]['magnitude']
        print(magnitude)
        #Check if magnitude => 5
        if magnitude >= int(magnitude_filter):
            magnitude = str(magnitude)
            description = offenseJSON[0]['description']
            domain = offenseJSON[0]['domain_id']
            print("Domain is: " + str(domain))
            offense_type = offenseJSON[0]['offense_type']
            print("Type is: " + str(offense_type))
            offense_source = offenseJSON[0]['offense_source']
            print("Offense Source is: " + str(offense_source))
            # Extract Domain from Domain ID
            endpoint2 = "https://{0}/api/config/domain_management/domains?fields=name&filter=id%3D%20'{1}'".format(qradar_endpoint, domain)
            r2 = requests.get(endpoint2, headers={'Accept': 'application/json', 'Connection': 'keep-alive', 'SEC': apiToken}, verify=False, timeout=60)
            print(r2.status_code)
            if r2.status_code == 200:
                domainJSON = r2.json()
                print(domainJSON)
                domain_id = domainJSON[0]['name']
            # Extract Offense Type from Offense Type ID
            endpoint3 = "https://{0}/api/siem/offense_types?fields=name&filter=id%20%3D%20'{1}'".format(qradar_endpoint, offense_type)
            r3 = requests.get(endpoint3, headers={'Accept': 'application/json', 'Connection': 'keep-alive', 'SEC': apiToken}, verify=False, timeout=60)
            print(r3.status_code)
            if r3.status_code == 200:
                typeJSON = r3.json()
                print(typeJSON)
                offenses_type = typeJSON[0]['name']
            create_jira_ticket(magnitude, description, domain_id, offenses_type, offense_source)
        else:
            print('Failed to Open QRadar Ticket due to magnitude.')
    else:
        print('Failed to retrieve QRadar offenses.')
        print(r.text)

# Main entry point
def main():
    # Add delay in order to retrieve offense at real time
    sleep(seconds)
    print('Sleep mode finished!')
    retrieve_qradar_offenses()

if __name__ == '__main__':
    main()
