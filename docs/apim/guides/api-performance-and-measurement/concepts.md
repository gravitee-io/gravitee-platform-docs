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
