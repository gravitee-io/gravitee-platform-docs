# MCP Usage Dashboard 

## Overview

The LLM Dashboard provides users with clear visibility into the LLM usage for their environment. With this Dashboard, the user can monitor how often a tool is used, the behavior of the LLM, and any errors produced by the LLM.

### Metrics for the MCP Dashboard
The LLM dashboard shows the following metrics:
* MCP requests. The total number of requests targeting MCP APIs.
* Average latency. The average Gateway latency for MCP requests.
* Max latency. The maximum Gateway latency observed for MCP requests.
* P90 latency. The 90th percentile Gateway latency for MCP requests.
* P99 latency. The 99th percentile Gateway latency for MCP requests.
* Method usage. The distribution of MCP proxy methods by request count. 
* Method usage over time. The evolution of the method usage over time.
* Most used resources. The top five used MCP resources by request count.
* Response status repartition. The distribution of HTTP response status codes for MCP requests.
* Most used tools. The top 5 MCP tools by request count.
* Most used prompts. The top 5 most used request prompts by request count.
* Average response time. Average Gateway response time. for MCP requests over time.

## Prerequisities 
To configure the MCP Dashboard, the user must have the following permissions:
* Environment-dashboard-r : see dashboard  
* Environment-dashboard-c : create a dashboard  
* Environment-dashboard-u : update a dashboard  
* Environment-dashboard-d : delete a dashboard  

## Create an MCP usage Dashboard

1. From the **Dashboard**, click **Observability**.
2. From the **Observability** dropdown menu, click **Dashboard**.
![Screenshot showing observability dropdown menu in the console](/.gitbook/assets/LLM_dashboard_navigation.jpg)
3. Click **Create dashboard**, and then click **Create from template**. 
![Screenshot showing dashboard list with the create dashboard dropdown clicked](/.gitbook/assets/LLM_Dashboard_create_dropdown_menu.jpg)
4. Click **MCP**, and then click **Use template**. 
![Screenshot showing the MCP dashboard template](/.gitbook/assets/MCP_Dashboard_template.jpg)
5. (Optional) Change the name of the dashboard and the labels for the dashboard. To change the name of the dashboard and the labels for the dashboard, complete the following sub-steps:
    a. Click **Dashboard options**, and then click **Edit**.
    ![Screenshot showing the MCP dashboard edit button](/.gitbook/assets/MCP_Dashboard_edit_dropdown.jpg)
    b. In the **Edit dashboard** pop-up window, navigate to the **Name** field, and then enter a new name for your dashboard.
    c. To add a new label for your dashboard, click **+ Add label**, and then enter the key-value pair. 
    d. To delete a label, click the **X** next the key-value pair that you want to delete.
    ![Screenshot showing the edit popup window](/.gitbook/assets/MCP_Dashboard_edit_popup_window.jpg)
6. (Optional) Change the timeframe for the dashboard. To changee the timeframe for the dashboard, compelte the following sub-steps:
    a. Click the **timeframe** dropdown menu.
    b. Select a new time frame or select **custom** to enter a custome timeframe. 
    ![Screenshot showing the timeframe list](/.gitbook/assets/MCP_Dashboard_timeframe.jpg)

## Verification 
Your dashboard appears in the Dashboard list.
![Screenshot showing the timeframe list](/.gitbook/assets/MCP_Dashboard_dashboard_list.jpg)