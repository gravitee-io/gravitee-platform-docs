---
title: How to add custom metrics in dashboards
tags:
  - APIM
  - How to
  - Custom metrics
  - Dashboards
  - Enterprise Edition feature
---

# How to add custom metrics in dashboards

## Overview

This document describes how you can easily configure the 'Assign metrics' policy to use custom metrics in your dashboards.

## Assign metrics policy

1.  In Design Studio, add the Assign metrics policy to a request or a
    response.
2.  Add a new metric and give it a name. This name will be the field
    name to use in dashboards.  
    *Example: MyCustomHeader*
3.  Specify a value for your metric. It can be a static value, but you
    can also use Expression Language syntax.  
    *Example:*
    `{#request.headers['X-MyCustomHeader'] != null ? #request.headers['X-MyCustomHeader'][0] : null}`

**Assign-metrics policy configuration:**

![Assign-metrics policy configuration diagram](/images/apim/3.x/how-tos/configure-custom-metrics/configure-assign-metrics-policy.png)

## Configure your dashboard

Only **table**, **pie** and **line** widgets can be configured with a custom field.

1.  Click **Settings &gt; Analytics**.
2.  Create or edit a dashboard.
3.  Add a widget and select the **table**, **line** or **pie** type.
4.  Toggle on the **Use custom field?** option.
5.  Add your metric name in the **Field** input.  
    *Example: MyCustomHeader*
6.  Save your configuration.

**Configuration of widgets using a custom field:**

![Configuration of widgets using a custom field](/images/apim/3.x/how-tos/configure-custom-metrics/configure-custom-field.png)

## Result

You now have a widget using your custom metric.  

In the example, you can see the distribution of different requests depending on the HTTP Header *X-MyCustomHeader*.

**Custom widgets in action:**

![Custom widgets in action](/images/apim/3.x/how-tos/configure-custom-metrics/custom-metric-dashboard-result.png)
