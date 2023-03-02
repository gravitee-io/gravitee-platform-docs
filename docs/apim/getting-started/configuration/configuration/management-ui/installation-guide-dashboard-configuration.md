# Overview

You can configure *dashboards* in APIM Console to display different
types of analytics in various formats. For each dashboard, you can
choose the type of data displayed and the format of the display, such as
a chart, map or table. You can also specify a filter, to display
analytics only for the queries you want.

You can create generic dashboards for the whole APIM platform, or
specific dashboards for APIs and applications.

-   Platform-wide dashboards are viewable through the APIM Console
    **Dashboard** menu option, by clicking the **ANALYTICS** tab.

-   API dashboards are viewable through the **APIs** menu option, by
    selecting an API and clicking **Analytics**.

-   Application dashboards are viewable through the **Applications**
    menu option, by selecting an application and clicking **Analytics**.

You can create multiple dashboards of each type with different
configurations, and choose the order in which they are displayed in the
menu.

# Create or configure a dashboard

Dashboards are configured by adding and removing *widgets*, which are
containers for different types and views of data.

1.  link:{{ */apim/3.x/apim\_quickstart\_console\_login.html* |
    relative\_url }}\[Log in to APIM Console^\].

2.  Click **Settings &gt; Analytics**.

    image:{% link
    images/apim/3.x/installation/configuration/configure-dashboards.png
    %}\[\]

3.  You can now:

    -   Add a new platform-wide dashboard by clicking **ADD A NEW
        DASHBOARD PLATFORM**

    -   Add a new API-level dashboard by clicking **ADD A NEW DASHBOARD
        API**

    -   Add a new application-level dashboard by clicking **ADD A NEW
        DASHBOARD APPLICATION**

    -   Select a dashboard from one of the three dashboard lists to
        configure it

4.  Specify a query filter in the **Query filter** field if you want to
    filter the API calls included in the analytics.

5.  Click the plus icon image:{% link images/icons/plus-icon.png
    %}\[role="icon"\] to add new widgets to the dashboard.

6.  Select the widget type from the list and specify the other values.

    image:{% link
    images/apim/3.x/installation/configuration/configure-dashboard-widgets.png
    %}\[\]

    Click **ENABLE PREVIEW** to preview your dashboard changes before
    saving.

    image:{% link
    images/apim/3.x/installation/configuration/configure-dashboards-preview.png
    %}\[\] . Add more widgets, as required. You can also edit or delete
    existing widgets. . Click **SAVE**.

By using the link:{{ */apim/3.x/apim\_policies\_assign\_metrics.html* |
relative\_url }}\[Assign Metrics policy\] in one of your APIs, you can
use a custom field in the widget.

See link:{{
*/apim/3.x/apim\_how\_to\_add\_custom\_metrics\_in\_dashboards.html* |
relative\_url }}\[How to add custom metrics in dashboards\].

# Update a dashboard

You can perform the following actions on any dashboard in the three
dashboard lists:

-   Delete it with the delete icon image:{% link
    images/icons/delete-icon.png %}\[role="icon"\]

-   Disable or enable it by toggling the enabled image:{% link
    images/icons/enabled-icon.png %}\[role="icon"\] and disabled
    image:{% link images/icons/disabled-icon.png %}\[role="icon"\] icons

-   Move it up or down the list with the up image:{% link
    images/icons/up-arrow-icon.png %}\[role="icon"\] and down image:{%
    link images/icons/down-arrow-icon.png %}\[role="icon"\] arrows to
    change its order of priority in the menu
