# logging-analytics

\= Logging and analytics :page-sidebar: apim\_3\_x\_sidebar :page-permalink: apim/3.x/apim\_publisherguide\_logging\_analytics.html :page-folder: apim/user-guide/publisher :page-layout: apim3x

\== Overview

You can view metrics and logs for applications and APIs using the _Analytics_ menu options in APIM Console.

TIP: From APIM version 3.6.x, you can mask secure data in your logs by adding the Data logging masking policy to your API. For more details, see link:\{{ '/apim/3.x/apim\_policies\_data\_logging\_masking.html' | relative\_url \}}\[Data logging masking^].

\=== Metrics

Metrics are presented in one or more _dashboards_. You can select the dashboard with the metrics you want to see from the _Select a dashboard_ drop-down menu. You can then select a time period and view several different types of analytics -- such as requests received and responses sent, the most frequently called applications and response times, presented in different views and formats -- such as bar charts and maps.

image:

\[]

For more details on creating and configuring dashboards, see link:\{{ '/apim/3.x/apim\_installguide\_dashboard\_configuration.html' | relative\_url \}}\[Configure dashboards^].

\=== Logs

You can list the API requests for a single API or for an application by viewing the logs, as follows:

* Select the API and click _Analytics > Logs_.
* Select the application and click _Logs_.

This lists all the API requests in date and time order. You can filter by date or search term and click on an individual entry to view more details.

image:

\[]

Log entries include details such as:

* the API endpoint for the request
* the URL of the gateway through which the request was sent

By default, the request header and payload are not logged in APIM, to save space, as shown in the basic logging detail page below. You specify how much detail to log in the logging configuration.

image:

\[Basic logging detail]

\== Configure API logging

NOTE: If you configured a maximum logging duration in the global settings, the maximum duration will be applied to the API logging configuration specified here. For more details, see link:\{{ '/apim/3.x/apim\_how\_to\_configuration.html#update-the-default-apim-settings' | relative\_url \}}\[Update the default APIM settings^].

WARNING: Logging configuration changes can have a significant impact on performance. Proceed with caution.

. link:\{{ '/apim/3.x/apim\_quickstart\_console\_login.html' | relative\_url \}}\[Log in to APIM Console^]. . Click _APIs_ and select the API from the list. . Click _Analytics > Logs_. . Click the _Configure the logging_ link at the top. + image:

\[]

*

If you configured a maximum logging duration in the global settings, APIM displays a message to remind you: image:

\[]

ifeval::\[\{{ site.products.apim.\_3x.version \}} < 3.6.0]

. In the _Mode_ drop-down, select the type of logging required:

* _Client only_ -- to log HTTP request header and payload details between the client and the gateway
* _Proxy only_ -- to log HTTP request header and payload details between the gateway and the backend
* _Client and proxy_ -- to log HTTP request header and payload details for both . Select _Logging enabled_ to go ahead and enable logging, or _Conditional logging_ to specify conditions for logging. . To specify logging conditions, click _SHOW EDITOR_ and select all the conditions which apply. You can restrict logging by:
* application or plan
* request header or query parameter
* HTTP method
* request IP address
* duration
* end date
*

You can create rules by combining conditions. Each new condition is added to the _Condition_ field. See the example below for more details.

\== Example

The following example shows how to configure logging to only log `GET` HTTP methods which include an `X-debug` request header with a value of `true`. We need to specify it as a combined condition in two parts.

. Click _SHOW EDITOR_ and in the condition editor, select _Condition type_ as _HTTP Method_. Click _ADD_. + image:

\[]

. Select _GET_ as the HTTP method. + image:

\[]

. Click _SAVE_. The new condition is added. Note that you need to take a copy the syntax of the condition, as it will be overwritten when you specify the next one. + image:

\[]

. Now click _SHOW EDITOR_ again to specify the second part of the condition. . Select _Request query-parameter_ as the _Condition type_. Click _ADD_. + image:

\[]

. Enter _X-debug_ as the _Query parameter name_ and _true_ as the value. + image:

\[]

. Click _SAVE_. We can see that the second condition has been added. To add back in the first condition, go to the end of the condition line and type _&&_, then paste it at the end. + image:

\[] endif::\[] ifeval::\[\{{ site.products.apim.\_3x.version \}} >= 3.6.0] . Toggle on the _Enabled_ option. . Select the level of logging required for the mode, content and scope. + image:\[]

. Specify all logging conditions which apply in link:\{{ '/apim/3.x/apim\_publisherguide\_expression\_language.html' | relative\_url \}}\[Gravitee Expression Language^]. You can restrict logging by:

* application or plan
* request header or query parameter
* HTTP method
* request IP address
* duration
* end date
*

You can combine conditions, as in the example below: + image:

\[] endif::\[]

. Click _SAVE_ to save the new logging configuration. Don't forget to redeploy your API. + We can now return to the logging screen and see the logging detail when we click on a log entry, as in the image below: + image:

\[]
