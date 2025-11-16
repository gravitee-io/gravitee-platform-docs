---
description: >-
  Gravitee offers several ways to measure, track and analyze APIs, in addition
  to capturing logs so that you can easily stay on top of your APIs and retain
  visibility into performance and consumption.
---

# API Measurement, Tracking, and Analytics

### Introduction

This section focuses on the various options for measuring, tracking, and keeping analytics on APIs. In this section, we cover:

* The Dashboard
* The APIs menu
* The Applications page
* The Audit trail
* API Quality
* APIM alerts and notifications
* Alert Engine and API Monitoring

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
* **The "Analytics" module:** the analytics module is where you can see and slightly configure all of the various dashboards, charts, etc. that refer to your Gravitee API analytics. You can build multiple analytics dashboards and view them all from this page. Your "Home board" will be pulling charts from these various dashboards.
* **The "Alerts" module:** this module is for keeping track of all API alerts over a given amount of time.
{% endtab %}
{% endtabs %}

### The APIs menu

While there is less "measurement" here, the APIs menu is crucial for being able to track information per each API that you are managing in Gravitee. Check out the interactive UI exploration or the text descriptions of the API menu to learn more.

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
* Visibility settings
{% endtab %}
{% endtabs %}

### The Applications page

The **Applications** page is where you can keep track of and view various information related to applications that are subscribed to your APIs. Check out the interactive UI exploration or the text descriptions to learn more.

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

{% hint style="warning" %}
**Enterprise only**

As of Gravitee 4.0, the Audit Trail is an Enterprise Edition capability. To learn more about Gravitee Enterprise, and what's included in various enterprise packages, please:

* [Refer to the EE vs OSS documentation](../../overview/gravitee-apim-enterprise-edition/README.md)
* [Book a demo](https://app.gitbook.com/o/8qli0UVuPJ39JJdq9ebZ/s/rYZ7tzkLjFVST6ex6Jid/)
* [Check out the pricing page](https://www.gravitee.io/pricing)
{% endhint %}

The **Audit** trail is where you can audit API consumption and activity, per event and type for your Gravitee APIs. You can use the **Audit trail** for monitoring the behavior of your API and platform over time.

For example, you can use it in conjunction with the analytics feature to identify a point at which your API behavior changed, view the configuration which caused the change, and roll back to an earlier configuration if required. Check out the interactive UI exploration or the text descriptions to learn more.

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

The Gravitee **API Quality** feature enables you to create and automatically assign customizable scores based on certain variables that you feel impact an API's overall quality. When enabled, APIs that you create in Gravitee will automatically be assigned an API quality score. This feature is incredibly valuable for organizations interested in API governance, as it allows them to ensure that certain standards are met, where these standards are treated as score-relevant variables. Check out the interactive UI exploration or the text descriptions to learn more.

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

In addition to the pre-baked characteristics, you can also create manual quality rules, where you create and assign weight to custom characteristics.
{% endtab %}
{% endtabs %}

### Alerts and notifications

Gravitee allows you to configure alerts and notifications through API Management. These allow individuals to subscribe to alerts and notifications based on specific events that they are interested in.

### Alert Engine and API Monitoring

In addition to Gravitee API Management and all of its features to measure, track, log, audit, etc., API consumption and performance, Gravitee also offers an enterprise-grade API monitoring and alerting solution called Gravitee Alert Engine (AE). To learn more about Gravitee AE, please refer to the [Gravitee AE documentation](https://app.gitbook.com/o/8qli0UVuPJ39JJdq9ebZ/s/WAKqxjzYogMr1tk18evT/).

### Making APIs more performant and reliable

In addition to features used to measure API reliability and performance, Gravitee offers several features and technology support that are meant to actively improve API reliability and performance. We will include brief descriptions of each here, but we recommend referring to their specific documentation to learn more about how implement them:

<table data-view="cards"><thead><tr><th></th><th></th><th></th></tr></thead><tbody><tr><td><a href="../../reference/policy-reference/rate-limit.md"><strong>Rate limiting policies</strong></a></td><td>While also useful for security measures, capping the amount of calls or requests per a given amount of time can ensure that an API is not "over consumed" and inducing too much load on backend systems, which can result in both poor performance and reliability incidents like downtime.</td><td></td></tr><tr><td><p><a href="../../reference/policy-reference/cache.md"><strong>Cache policy</strong></a></p><p>The Cache policy allows the Gateway to cache upstream responses (content, status, and headers) to eliminate the need for subsequent calls to the back end. This can help you avoid you calling the backend (and therefore inducing load) for non-changing requests.</p></td><td></td><td></td></tr><tr><td><p><a href="../create-apis/#supported-api-styles-event-brokers-and-communication-patterns"><strong>Support for asynchronous APIs and communication</strong></a></p><p>Gravitee's support for a variety of asynchronous APIs allows you to introduce APIs that can deliver real-time customer experiences and real-time data without constantly having to poll your backend resources.</p></td><td></td><td></td></tr></tbody></table>
