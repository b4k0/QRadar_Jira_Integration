#!/usr/bin/python3

import requests
import sys
import urllib3
import json
import re
from time import sleep

urllib3.disable_warnings()

# Variables for Jira API
jira_url = sys.argv[1]
jira_pat = sys.argv[2]

# Variables for QRadar API
offense = sys.argv[3]
apiToken= sys.argv[4] 
qradar_endpoint = sys.argv[5]
magnitude_filter = sys.argv[6]
seconds = int(sys.argv[7])


endpoint = "https://{0}/api/siem/offenses?fields=id%2C%20description%2C%20magnitude%2C%20domain_id%2C%20offense_type&filter=id%20%3D%20'{1}'".format(qradar_endpoint, offense)



print(endpoint)

jira_endpoint = jira_url


# Create a JIRA ticket based on QRadar offense
def create_jira_ticket(magnitude, description, domain_id, offenses_type):
    
    magnitude_int = int(magnitude)
    print(magnitude_int)
    
    # Compose the JIRA ticket payload
    payload = json.dumps({
        'fields': {
            'project': {'key': 'Project Name'},
            'summary': 'QRadar Offense:' + ' ' + offense,
            'description': 'QRadar Offense Description: ' + ' ' + description + '\n' + 'Magnitude: ' + ' ' + magnitude + '\n' + 'Domain: ' + ' ' + domain_id + '\n' + 'Offense Type: ' + ' ' + offenses_type,
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
    r = requests.get(endpoint, headers={'Accept': 'application/json', 'Connection': 'keep-alive', 'SEC': apiToken}, verify=False, timeout=60)
    print(r.status_code)
    print(r.elapsed.total_seconds())
    # Check if the request was successful
    if r.status_code == 200:
        offenseJSON = r.json()
        print(offenseJSON)
        print(len(offenseJSON))
        # Extract relevant information from QRadar offense
        print(offenseJSON[0])
        magnitude = offenseJSON[0]['magnitude']
        print(magnitude)
        #Check if magnitude > 5
        if magnitude >= int(magnitude_filter):
            jira_url_2 =  "{0}/rest/api/2/search?jql=project%20%3D%20MSS%20%26%20issuetype%20%3D%20Incident%20%26%20'Alert Link'%20%7E%20{1}&fields=project%2C%20issuetype%2C%20customfield_19101%2C%20customfield_19103".format(jira_endpoint, offense)
            rJira = requests.get(jira_url_2, headers={'Accept': 'application/json', 'Connection': 'keep-alive', 'Content-Type': 'application/json', 'Authorization': 'Bearer  {}'.format(jira_pat)}, timeout=60, verify=False)
            print(rJira.status_code)
            print(rJira.elapsed.total_seconds())
            if rJira.status_code == 200:
                JiraJSON = rJira.json()
                print(JiraJSON)
                print(len(JiraJSON))
                # Extract relevant information from Jira Issue
                print(JiraJSON['issues'])
                 # check if there is open QRadar offense on Jira
                if len(JiraJSON['issues']) <= 0 :
                    print("There is not any issue with this offense ID")
                    magnitude = str(magnitude)
                    description = offenseJSON[0]['description']
                    domain = offenseJSON[0]['domain_id']
                    print("Domain is: " + str(domain))
                    offense_type = offenseJSON[0]['offense_type']
                    print("Type is: " + str(offense_type))
                    endpoint2 = "https://{0}/api/config/domain_management/domains?fields=description&filter=id%3D%20'{1}'".format(qradar_endpoint, domain)
                    r2 = requests.get(endpoint2, headers={'Accept': 'application/json', 'Connection': 'keep-alive', 'SEC': apiToken}, verify=False, timeout=60)
                    print(r2.status_code)
                    if r2.status_code == 200:
                        domainJSON = r2.json()
                        print(domainJSON)
                        domain_id = domainJSON[0]['name']
                    endpoint3 = "https://{0}/api/siem/offense_types?fields=name&filter=id%20%3D%20'{1}'".format(qradar_endpoint, offense_type)
                    r3 = requests.get(endpoint3, headers={'Accept': 'application/json', 'Connection': 'keep-alive', 'SEC': apiToken}, verify=False, timeout=60)
                    print(r3.status_code)
                    if r3.status_code == 200:
                        typeJSON = r3.json()
                        print(typeJSON)
                        offenses_type = typeJSON[0]['name']
                    create_jira_ticket(magnitude, description, domain_id, offenses_type)
                else:
                    offense2 = JiraJSON['issues'][0]['fields']['customfield_19101']
                    magnitude2 = JiraJSON['issues'][0]['fields']['customfield_19103']
                    key = JiraJSON['issues'][0]['key']
                    print(magnitude2)
                    print(key)
                    print("Issue found with this offense ID" + " " + offense2)
                    print("Issue found with this key" + " " + key)
                    #Update Jira issue magnitude
                    jira_url_3 = "{0}/rest/api/2/issue/{1}".format(jira_endpoint, key)
                    print(jira_url_3)
                    # Compose the JIRA ticket payload
                    payload2 = json.dumps({
                            'fields': {
                                'customfield_19103': magnitude
                                }
                            })
                        # Send a PUT request to update the JIRA ticket
                    response2 = requests.put(jira_url_3, data=payload2, headers={'Accept': 'application/json', 'Connection': 'keep-alive', 'Content-Type': 'application/json', 'Authorization': 'Bearer  {}'.format(jira_pat)}, timeout=60, verify=False)
                    
                    print(response2.status_code)

                    # Check if the JIRA ticket was created successfully
                    if response2.status_code == 204:
                        print('JIRA ticket updated successfully.')
                    else:
                        print('Failed to update JIRA ticket.')
                    
            else:
                print('Failed to retrieve Jira Issue.')
        else:
            print('Magnitude is smaller than' + ' ' + magnitude_filter)
    else:
        print('Failed to retrieve QRadar offenses.')

# Main entry point
def main():
#    sleep(seconds)
#    print('Sleep mode finished!')
    retrieve_qradar_offenses()


if __name__ == '__main__':
    main()