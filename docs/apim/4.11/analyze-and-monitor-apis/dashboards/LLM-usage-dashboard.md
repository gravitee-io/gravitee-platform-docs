# LLM Usage Dashboard

## Overview

The LLM Dashboard provides users with clear visibility into the LLM usage for their environment. With this Dashboard, the user can monitor how often a tool is used, the behavior of the LLM, and any errors produced by the LLM.

### Metrics for the LLM Dashboard

The LLM dashboard shows the following metrics:

* Total tokens. The combined total of prompt tokens and completion tokens processed.
* Average tokens per request. The average token consumption for each LLM call.
* Total token count over time. The cost trend of tokens for prompts and completion.
* Token cost over time. The trend of prompt, completion, and total tokens consumed.
* Total cost. The total cost of the LLM usage.
* Average cost per request. The average spend for each LLM call.
* Response status reparition. The breakdown of HTTP outcomes for each LLM call.
* Total token per model. The breadkown of comsumption across LLM models.
* Total requests. All HTTP calls processed by the Gateway.
* LLM requests. Total call volume targeting LLM providers.

<figure><img src="../../.gitbook/assets/LLM_Dashboard_metrics.jpg" alt=""><figcaption></figcaption></figure>

## Prerequisities

To configure the LLM Dashboard, the user must have the following permissions:

* Environment-dashboard-r : see dashboard
* Environment-dashboard-c : create a dashboard
* Environment-dashboard-u : update a dashboard
* Environment-dashboard-d : delete a dashboard

## Create an LLM usage Dashboard

1. From the **Dashboard**, click **Observability**.
2.  From the **Observability** dropdown menu, click **Dashboard**. <br>

    <figure><img src="../../.gitbook/assets/LLM_dashboard_navigation.jpg" alt=""><figcaption></figcaption></figure>
3.  Click **Create dashboard**, and then click **Create from template**. <br>

    <figure><img src="../../.gitbook/assets/LLM_Dashboard_create_dropdown_menu.jpg" alt=""><figcaption></figcaption></figure>
4.  Click **LLM**, and then click **Use template**.&#x20;

    <figure><img src="../../.gitbook/assets/LLM_Dashboard_template_screen.jpg" alt=""><figcaption></figcaption></figure>
5. (Optional) Change the name of the dashboard and the labels for the dashboard. To change the name of the dashboard and the labels for the dashboard, complete the following sub-steps:&#x20;
   1.  Click **Dashboard options**, and then click **Edit**. <br>

       <figure><img src="../../.gitbook/assets/image (5).png" alt=""><figcaption></figcaption></figure>
   2. In the **Edit dashboard** pop-up window, navigate to the **Name** field, and then enter a new name for your dashboard.&#x20;
   3. To add a new label for your dashboard, click **+ Add label**, and then enter the key-value pair.&#x20;
   4.  To delete a label, click the **X** next the key-value pair that you want to delete.&#x20;

       <figure><img src="../../.gitbook/assets/LLM_Dashboard_edit_popup_window.jpg" alt=""><figcaption></figcaption></figure>
6. (Optional) Change the timeframe for the dashboard. To changee the timeframe for the dashboard, compelte the following sub-steps:&#x20;
   1.  Click the **timeframe** dropdown menu. b. Select a new time frame or select **custom** to enter a custome timeframe. <br>

       <figure><img src="../../.gitbook/assets/LLM_Dashboard_timeframe_dropdown_menu.jpg" alt=""><figcaption></figcaption></figure>

## Verification

Your dashboard appears in the Dashboard list.&#x20;

<figure><img src="../../.gitbook/assets/LLM_Dashboard_dashboard_list.jpg" alt=""><figcaption></figcaption></figure>
