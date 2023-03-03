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

###
