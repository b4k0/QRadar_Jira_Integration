#!/usr/bin/python

import requests
import sys
import urllib3

# Disable warning
urllib3.disable_warnings()

# Variables for QRadar API Request
apiToken= sys.argv[1] 
endpointURL = sys.argv[2]
offenseID = sys.argv[3]

# Endpoint of QRadar API Request
endpoint = "https://{0}/api/siem/offenses?fields=id%2C%20description%2C%20magnitude&filter=id%20%3D%20'{1}'".format(endpointURL, offenseID)

# Header of QRadar API Request using QRadar API Token
header = {'Accept': 'application/json', 'Connection': 'keep-alive', 'SEC': apiToken}

# GET Request for retrieving QRadar Offenses
request = requests.get(endpoint, headers=header, verify=False, timeout=60)

# Print Response
print(request.json())
