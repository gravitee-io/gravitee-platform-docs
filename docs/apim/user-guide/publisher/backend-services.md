# backend-services

\= Load balancing, failover and health check :page-sidebar: apim\_3\_x\_sidebar :page-permalink: apim/3.x/apim\_publisherguide\_backend\_services.html :page-folder: apim/user-guide/publisher :page-layout: apim3x

\== Overview

APIM includes a number of backend services for managing your APIs. This page explains how to configure the following services for your APIs:

* Load balancing
* Failover
* Health check

\=== How to access the API backend service configuration

To update the configuration for these services:

. link:\{{ '/apim/3.x/apim\_quickstart\_console\_login.html' | relative\_url \}}\[Log in to APIM Console^]. . Click _APIs_ and select an API. . Click _Proxy_. + The backend service configuration options are in the _BACKEND SERVICES_ section. + image:

\[]

WARNING: You must redeploy your API with the _deploy the API_ link after each new configuration.

\== Configure load balancing

APIM Gateway includes a built-in load balancer, which you can enable and configure for your API endpoints according to your requirements.

\[\[endpoint-groups]] === Endpoint groups

You configure load balancing by creating a logical grouping of endpoints and specifying a load balancing algorithm for them. For example, you can define a group of endpoints representing instances of the same API deployed on different servers.

APIM always uses the first group defined for load balancing. Any additional groups you define are for use in policies:

* redirection rules including named groups in the link:\{{ '/apim/3.x/apim\_policies\_dynamic\_routing.html#regular\_expressions' | relative\_url \}}\[Dynamic routing^] policy
* traffic shadowing using endpoints in these groups link:\{{ '/apim/3.x/apim\_policies\_traffic\_shadowing.html' | relative\_url \}}\[Traffic shadowing^] policy

\=== Load balancing types

You can configure four types of load balancing:

* Round robin
* Random
* Weighted round robin
* Weighted random

For the two weighted types, you need to assign a weight to your endpoints to determine the frequency with which APIM Gateway selects one endpoint for load balancing compared to another.

For example, if you have the following two endpoints:

* Endpoint 1 with a weight of 9
* Endpoint 2 with a weight of 1

Endpoint 1 is selected 9 times out of 10, whereas Endpoint 2 is selected only 1 time out of 10.

\=== Create a group

. Click _Endpoints_. . Click _ADD A NEW GROUP_. . In the _GENERAL_ tab, enter a _Name_ for the group and the type of load balancing algorithm to use. . In the _CONFIGURATION_ tab, configure any additional HTTP details for the group, such as proxy and SSL details. . In the _SERVICE DISCOVERY_ tab, enable _Enabled service discovery_ if you want external endpoints to be dynamically added or removed to or from the group, then specify the type of service discovery. For more details of service discovery in APIM, see link:\{{ '/apim/3.x/apim\_service\_discovery\_overview.html' | relative\_url \}}\[Service discovery^]). . Click _SAVE_.

Your group is added to the list. You can now perform any of the following actions on the group by clicking the corresponding icon in the group header:

* Add endpoints to your group by clicking the plus icon image:\[role="icon"]
* Update the group configuration by clicking the settings icon image:\[role="icon"]
* Delete the group by clicking the delete icon image:\[role="icon"]
* Change the display order of the endpoints from ascending to descending and vice versa, by clicking the arrow icon image:\[role="icon"] next to the _Name_, _Type_ or _Weight_ header

\=== Add endpoints to your group

. Click the plus icon image:

\[role="icon"] to add new endpoints to your group. . In the _GENERAL_ tab, specify the endpoint details as follows:

* The _Type_ and _Name_ of the endpoint
* The endpoint URL in the _Target_ field
* A number in the _Weight_ field (only if the endpoint is in a group configured with _Weighted Round-Robin_ or _Weighted Random_ load balancing), representing the weight the endpoint has in terms of selecting it for _Weighted_ load balancing
* If a global health check configuration exists, it is automatically applied to this endpoint. If you want to change the health check behavior for your endpoint, click the settings icon image:\[role="icon"]in the _Health-check_ section, then: \*\* Uncheck _Enable health-check_ to disable health checking for your endpoint \*\* Uncheck _Inherit configuration_ and specify a different health check configuration, as described in <> from step 4
* Check the _Secondary endpoint_ option to define this endpoint outside the main load balancing pool, to be used for load balancing only if all the primary endpoints are marked as down by the health check

. In the _CONFIGURATION_ tab, uncheck the option to inherit the HTTP configuration specified for the group if you want to specify a different HTTP configuration for this endpoint, then enter the details of the HTTP configuration. . Click _SAVE_. + Your new endpoint is added to the list. Endpoints with inherited configuration are denoted by a right-angled arrow and endpoints with health checking configured are denoted by a heart: + image:

\[]

You can now perform any of the following actions on the endpoint:

* Update the endpoint configuration by clicking the settings icon image:\[role="icon"] next to the endpoint
* Delete one or more of the endpoints in the group by selecting the relevant checkboxes and clicking the delete icon image:\[role="icon"] in the header row

\== Configure failover

Once you have configured your endpoints, as described in <>, you can configure failover for the endpoints and load balancing algorithm configured.

. Click _Failover_. . Select _Enabled_ to enable failover. + image:

\[]

. Enter a _Max attempts_ number, for the number of times APIM Gateway attempts to find a suitable endpoint, according to the load balancing algorithm, before returning an error. . Enter a _Timeout_, for the number of milliseconds between each attempt. . Click _SAVE_.

\== Configure health check

This section explains how to create a global health check configuration. When you create a global health check configuration, APIM applies the configuration to all existing endpoints and all new endpoints you create by default.

To create an endpoint-specific health check configuration or disable health checking for an endpoint, choose the endpoint first and click the health check settings, as described in <>.

From APIM version 3.6, you can view the health of your APIs in _Dashboard_, by clicking the _APIS STATUS_ tab:

image:

\[]

To configure health checking:

. Click _Health-check_. . Click the _Configure Health-check_ link at the top of the page. . Select _Enable health-check_. + image:

\[]

ifeval::\[\{{ site.products.apim.\_3x.version \}} < 3.6.0] . Enter the interval between each health check as an _Interval_ number and a _Time Unit_. Note that this interval is applied for each gateway in your APIM environment. endif::\[] ifeval::\[\{{ site.products.apim.\_3x.version \}} >= 3.6.0] . Enter the schedule as a `cron` expression. endif::\[]

. Enter the _HTTP Method_ which triggers the health check. . Add the path which triggers the health check. Select _From root path_ to apply the path specified at root URL level. For example, if your endpoint URL is `www.test.com/api`, this option removes `/api` before appending the path. . Specify headers which trigger the health check, if any. You can use link:\{{ '/apim/3.x/apim\_publisherguide\_expression\_language.html' | relative\_url \}}\[Gravitee Expression Language^] to configure a header. Available variables are link:\{{ '/apim/3.x/apim\_publisherguide\_expression\_language.html#dictionaries' | relative\_url \}}\[dictionaries^] and link:\{{ '/apim/3.x/apim\_publisherguide\_expression\_language.html#properties' | relative\_url \}}\[api's properties^] access. . In _Assertions_, specify any conditions to test for in the API response in order to trigger the health check. Assertions are written in link:\{{ '/apim/3.x/apim\_publisherguide\_expression\_language.html' | relative\_url \}}\[Gravitee Expression Language^]. An assertion can be a simple 200 response (`#response.status == 200`) but you can also test for specific content. . Click _SAVE_. + You can see a visual summary of the health check configuration you specified on the right. + After you deploy your API, click _Back to Health-check_ to view the health check. You can filter the display by date and time period.
