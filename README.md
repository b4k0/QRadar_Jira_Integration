# QRadar_Jira_Integration
![QRadarJira](https://github.com/Mpak1996/QRadar_Jira_Integration/assets/51766689/4a5ad030-a2eb-4cf9-a2a0-7965e66d0ace)


**Python** **Script** for integrating **IBM** **QRadar** **SIEM** with **Jira** **Ticketing** **System**, in order to **create** **issue**(open ticket) automatically on **Jira** for **offenses** with **magnitude** bigger than a selected score via **Custom** **Actions**!

## Development Process

* Generate **Jira** **Personal** **Access** **Token**
* Generate **QRadar** **API** **Key**
* Create a **QRadar** **Offense** **Rule**, when a **new** **offense** is **generated** then create a **new** **event** **"Offense Created"**
* Create a **QRadar** **Event** **Rule**, when the **event "Offense Created"** is **generated**, then **run** a **python script** via **Custom Actions** on **QRadar** **Console**.
* Python script:
  
    * Identify **API** **endpoints** both for **QRadar** and **Jira**.
	* Select the **attributes** of **QRadar** **API**.
	* Write the **python** **script**.
* Test the Integration:
  
    * Test **QRadar** **API** via **Custom Actions**.
  	* Test **Jira** **API** via **Custom Actions**.
  	* Test **QRadar-Jira Script** via **Custom Actions**.
  	* Test the **integration** after the **QRadar** **Event** **Rule** is fired.
 
## **SOS**

  * **Jira Personal Access Token** is A **Bearer Token**, check your syntax on API Request **Authorization headers**.
  * Use **QRadar's Console IP**, **NOT Domain**, on API Request.
  * On **Custom** **Actions**, any property is a **string**.
  * Extract **Offense ID** from the **event** **"Offense Created"**, for creating the QRadar API request in order to catch any new offense.
---


![QRadar Jira Integration](https://github.com/Mpak1996/QRadar_Jira_Integration/assets/51766689/b8eed487-23d4-4ed6-af0f-6dff03bc6791)
