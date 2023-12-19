# QRadar_Jira_Integration

**Python** **Script** for integrating **IBM** **QRadar** **SIEM** with **Jira** **Ticketing** **System**, in order to **create** **issue**(open ticket) automatically on **Jira** for **offenses** with **magnitude** bigger than a selected score via **Custom** **Actions**!

## Development Process

* Generate **Jira** **Personal** **Access** **Token**
* Generate **QRadar** **API** **Key**
* Create a **QRadar** **Offense** **Rule**, when a **new** **offense** is **generated** then create a **new** **event** **"Offense Created"**
* Create a **QRadar** **Event** **Rule**, when the **event "Offense Created"** is **generated**, then **run** a **python script** via **Custom Actions** on **QRadar** **Console**.
* Python script:
  
    * Identify **API** **endpoints** both for **QRadar** and **Jira**.
	* Think of **script** **logic**.
	* Select the **attributes** of **QRadar** **API**.
	* Write the **python** **script**.
* Test the Integration:
  
    * Test **QRadar** **API** via **Custom Actions**.
  	* Test **Jira** **API** via **Custom Actions**.
  	* Test **QRadar-Jira Script** via **Custom Actions**.

<br>
<br>

![QRadar Jira Integration](https://github.com/Mpak1996/QRadar_Jira_Integration/assets/51766689/7005d639-7165-4f66-9f2f-efd7e38b9ab9)

