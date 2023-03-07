---
description: >-
  Conceptual explanation of everything that Gravitee does to help you track API
  status, measure their overall performance, and improve performance via load
  balancing, failover, and health checks.
---

# Concepts

## Measurement, tracking, analytics, auditing, and logging

Gravitee offers several ways to measure, track and analyze APIs, in addition to capturing logs so that you can easily stay on top of your APIs and retain visibility into performance and consumption. Let's explore the various platform components and features that enable this—at a conceptual level.

### The Dashboard

The Gravitee "Dashboard" is an area in the UI where you'll be able to create custom dashboards around API performance, status, lifecycle stage, and more. The dashboard includes several sub-modules across different tabs, each with various features. To explore in depth, feel free to use the interactive UI exploration tool or the text descriptions provided below.

{% tabs %}
{% tab title="Interactive UI exploration" %}
{% @arcade/embed flowId="bTYh1yLqcbJU6xaGZQZm" url="https://app.arcade.software/share/bTYh1yLqcbJU6xaGZQZm" %}
{% endtab %}

{% tab title="Text descriptions" %}
The "Dashboard" in Gravitee is made up of several modules:

* **The "Home" board module:** This is your "Metrics and analytics homepage." You can configure this page to show chosen charts, filter chart data based on time range, and configure how regularly the charts should be refreshed.
* **The "API Status" module:** this module shows you status and availability of your APIs across time. You can filter which APIs to view and what for time range you want to view API status and availability.
* **The "Analytics" module:** the analytics module is where you can see and slightly configure all of the various dashboards, charts, etc. that refer to your Gravitee API analytics. You can build multiple anayltics dashboards and view them all from this page. Your "Home board" will be pulling charts from these various dashboards.
* **The "Alerts" module:** this module is for keeping track of all API alerts over a given amount of time.&#x20;
{% endtab %}
{% endtabs %}

### The APIs menu

While there is less "measurement" here, the APIs menu is crucial for being able to track information per each API that you are mangaging in Gravitee. Check out the interactive UI exploration or the text descriptions of the API menu to learn more.

{% tabs %}
{% tab title="Interactive UI exploration" %}
{% @arcade/embed flowId="6XNg5xzEOEkNwJRZ6Ogm" url="https://app.arcade.software/share/6XNg5xzEOEkNwJRZ6Ogm" %}
{% endtab %}

{% tab title="Second Tab" %}
The APIs menu includes several key bits of information that you can use to keep track of and search for your APIs that are being managed in Gravitee. The page lists information around:

* API name
* API context path
* Tags
* Quality (this is determined by your Gravitee API quality settings)
* Owner
* Mode (this essentially refers to the Gravitee API definition that is used for that API and manner of policy application that comes with that definition)
* Visibility settings&#x20;
{% endtab %}
{% endtabs %}

### The Applications page

The **Applications** page is where you can keep track of and view various information related to applications that are subscribed to your APIs. Check out the interactive UI exploration or the text descriptions to learn more.&#x20;

{% tabs %}
{% tab title="Interactive UI exploration" %}
{% @arcade/embed flowId="WvD0RpAfXJIdCJQBSSOz" url="https://app.arcade.software/share/WvD0RpAfXJIdCJQBSSOz" %}
{% endtab %}

{% tab title="Text descriptions" %}
The **Applications** page is comprised of the following resources for active and archived applications:

* Name of application(s)
* Type of application(s)
* Owner of the application(s)
* The ability to edit the application(s)
* The ability to add an application
{% endtab %}
{% endtabs %}

### The Audit trail

The **Audit** trail is where you can audit API consumption and activity, per event and type for your Gravitee APIs. You can use the **Audit trail** for monitoring the behavior of your API and platform over time.&#x20;

For example, you can use it in conjunction with the analytics feature to identify a point at which your API behavior changed, view the configuration which caused the change, and roll back to an earlier configuration if required. Check out the interactive UI exploration or the text descriptions to learn more.&#x20;

{% tabs %}
{% tab title="Interactive UI exploration" %}
{% @arcade/embed flowId="8cTbVX8QGEQ3XsLURvW0" url="https://app.arcade.software/share/8cTbVX8QGEQ3XsLURvW0" %}
{% endtab %}

{% tab title="Text descriptions" %}
The **Audits** page is comprised of a table and filtering mechanisms. You are able to do the following:

* Filter activity by **Event** and **Type**
  * **Event** refers to a specific change in state related to API or application consumption/us
  * **Type** refers to either an API or application
    * You can further filter your **Type** by individual APIs or individual applications
* Filter activity by a date range
* View the following information per auditable event:
  * Date
  * Name
  * Type
  * Reference
  * Event
  * Target
  * Patch
{% endtab %}
{% endtabs %}

### API Quality

The Gravitee **API Quality** feature enables you to create and automatically assign customizable scores based on certain variables that you feel impact an API's overall quality. When enabled, APIs that you create in Gravitee will automatically be assigned an API quality score. This feature is incredibly valuable for organizations interested in API governance, as it allows them to ensure that certain standards are met, where these standards are treated as score-relevant variables. Check out the interactive UI exploration or the text descriptions to learn more.&#x20;

{% tabs %}
{% tab title="Interactive UI exploration" %}
{% @arcade/embed flowId="crEmd5VTMLuJSdb8c9aM" url="https://app.arcade.software/share/crEmd5VTMLuJSdb8c9aM" %}
{% endtab %}

{% tab title="Text descriptions" %}
You can view and configure API quality scoring in multiple areas in product. You can see your APIs' quality scores in the:

* APIs menu
* On the individual API's details

You can configure scoring mechanisms in the **Settings > API Quality** menu. Here, you can set certain weights to certain API characteristics that will impact the overall quality scoring and decide whether or not you will require review from an API reviewer before being able to publish that API. Gravitee comes pre-baked with a set of certain characteristics. You give a certain amount of points (correlates to weight) to each of the following categories and subcategories:

* General: defines quality requirements for API details such as description, labels, and categories
* Documentation: defines quality requirements for documentation quality
* Endpoint: defines a quality requirement that states a healthcheck must be configured for your API

In addition to the pre-baked characteristics, you can also create manual quality rules, where you create and assign weight to custom characteristics.&#x20;
{% endtab %}
{% endtabs %}

### Load balancing

Load balancing is a technique used to distribute incoming traffic across multiple backend servers. The goal of load balancing is to optimize resource utilization, maximize throughput, minimize response time, and avoid overloading any single server. The Gravitee Gateway comes with a built-in load balancer, which you can enable and configure for your API endpoints according to your requirements. Check out the interactive UI exploration or the text descriptions to learn more.&#x20;

{% tabs %}
{% tab title="Interactive UI exploration" %}
{% @arcade/embed flowId="q2cetEPiktDGaSv7t4gM" url="https://app.arcade.software/share/q2cetEPiktDGaSv7t4gM" %}
{% endtab %}

{% tab title="Text descriptions" %}
In order to successfully use Gravitee load balancing, you'll need to understand two key concepts:

* **Endpoint groups:** a logical grouping of endpoints that share a load balancing algorithm
* **Load balancing types:** Gravitee offers four different types of load balancing:
  * **Round robin:** The algorithm works by maintaining a list of backend servers and assigning each incoming request to the next server in the list. Once the last server in the list has been reached, the algorithm starts again from the beginning of the list, cycling through the servers in a circular fashion.
  * **Random:** The algorithm selects a backend server at random for each incoming request. Each server has an equal chance of being selected, regardless of its current load or processing capacity.
  * **Weighted round robin:** The algorithm works similarly to the Round Robin mode, but doesn't assign incoming requests in a ciricular fashion, but, instead, assisgns requests based of a specified weight that you have given each backend server.
    * For example, if you have endpoint 1 with a weight of 9 and endpoint 2 with a weight of 1, endpoint 1 is selected 9 times out of 10, whereas endpoint 2 is selected only 1 time out of 10.
  * **Weighted random:** Weighted random load balancing leverages an algorithm that distributes incoming traffic across multiple backend servers based on a predefined weight assigned to each server. The weight represents the relative capacity or processing power of each server, with higher weights indicating a higher capacity to handle incoming requests. The algorithm works by generating a random number within a defined range, based on the total sum of all server weights. The random number is then used to select one of the backend servers for processing the incoming request.
    * For example, if you have a group of three backend servers A, B, and C, with weights of 1, 2, and 3, respectively. The total weight of all servers is 6. When an incoming request arrives, the load balancer generates a random number between 1 and 6. If the number is between 1 and 1 (inclusive), server A is selected. If the number is between 2 and 3, server B is selected. If the number is between 4 and 6, server C is selected.
{% endtab %}
{% endtabs %}

### Failover

Failover is a mechanism to ensure high availability and reliability of APIs by redirecting incoming traffic to a secondary server or backup system in the event of a primary server failure. Gravitee includes built-in failover mechanisms and capabilities. Check out the interactive UI exploration or the text descriptions to learn more.&#x20;

{% tabs %}
{% tab title="Interactive UI exploration" %}
{% @arcade/embed flowId="VaRhvOcOU39TQb3PtfRd" url="https://app.arcade.software/share/VaRhvOcOU39TQb3PtfRd" %}
{% endtab %}

{% tab title="Text descriptions" %}
Once you have configured your endpoints as a part of your load-balancing configuration, you can configure failover for those endpoints and whichever load balancing algorithm that you chose. You'll need to understand the following concepts to make the most of Gravitee failover mechanisms:

* **Max attempts**: limits the number of possible tries before returning an error. Each try gets an endpoint according to the load balancing algorithm.
* **Timeout**: limits the time allowed to try another attempt
{% endtab %}
{% endtabs %}

### Healthchecks&#x20;

A health check is a mechanism used in API management to monitor the availability and health of backend servers, microservices, or other components that make up an API. Gravitee includes a built-in health check mechanism that allows you to create global health check configurations. Check out the interactive UI exploration or the text descriptions to learn more.&#x20;

{% @arcade/embed flowId="VaRhvOcOU39TQb3PtfRd" url="https://app.arcade.software/share/VaRhvOcOU39TQb3PtfRd" %}

