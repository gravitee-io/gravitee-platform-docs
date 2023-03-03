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

{% @arcade/embed flowId="5zfoNz6KCHqs2XS8RZ1b" url="https://app.arcade.software/share/5zfoNz6KCHqs2XS8RZ1b" %}

{% @arcade/embed flowId="5zfoNz6KCHqs2XS8RZ1b" url="https://app.arcade.software/share/5zfoNz6KCHqs2XS8RZ1b" %}

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

## Navigating the APIs menu

[**Made by Alex Drag with Scribe**](https://scribehow.com/shared/Navigating\_the\_APIs\_menu\_\_scS7AryiQQKXTF9ERROJbQ)

**1. Navigate to https://apim-master-console.team-apim.gravitee.dev/#!/environments/DEFAULT/apis/?page=1\&size=10**

**2. Click here.**

![](https://ajeuwbhvhr.cloudimg.io/colony-recorder.s3.amazonaws.com/files/2023-03-03/e096385d-af89-4d3c-b62c-d3717d38aa89/ascreenshot.jpeg?tl\_px=0,10\&br\_px=1493,850\&sharp=0.8\&width=560\&wat\_scale=50\&wat=1\&wat\_opacity=0.7\&wat\_gravity=northwest\&wat\_url=https://colony-labs-public.s3.us-east-2.amazonaws.com/images/watermarks/watermark\_default.png\&wat\_pad=74,139)

**3. Click here.**

![](https://ajeuwbhvhr.cloudimg.io/colony-recorder.s3.amazonaws.com/files/2023-03-03/45f98d55-3164-428c-b097-33748c9f3f5c/ascreenshot.jpeg?tl\_px=125,54\&br\_px=1618,894\&sharp=0.8\&width=560\&wat\_scale=50\&wat=1\&wat\_opacity=0.7\&wat\_gravity=northwest\&wat\_url=https://colony-labs-public.s3.us-east-2.amazonaws.com/images/watermarks/watermark\_default.png\&wat\_pad=262,139)

**4. Click here.**

![](https://ajeuwbhvhr.cloudimg.io/colony-recorder.s3.amazonaws.com/files/2023-03-03/f5d087c8-05f3-4dd7-947a-5796f5444012/ascreenshot.jpeg?tl\_px=831,54\&br\_px=2324,894\&sharp=0.8\&width=560\&wat\_scale=50\&wat=1\&wat\_opacity=0.7\&wat\_gravity=northwest\&wat\_url=https://colony-labs-public.s3.us-east-2.amazonaws.com/images/watermarks/watermark\_default.png\&wat\_pad=262,139)

**5. Click "Tags"**

![](https://ajeuwbhvhr.cloudimg.io/colony-recorder.s3.amazonaws.com/files/2023-03-03/15eac6f1-b158-4f7d-8ed7-df7a762e5d79/ascreenshot.jpeg?tl\_px=1277,52\&br\_px=2770,892\&sharp=0.8\&width=560\&wat\_scale=50\&wat=1\&wat\_opacity=0.7\&wat\_gravity=northwest\&wat\_url=https://colony-labs-public.s3.us-east-2.amazonaws.com/images/watermarks/watermark\_default.png\&wat\_pad=262,139)

**6. Click "Quality"**

![](https://ajeuwbhvhr.cloudimg.io/colony-recorder.s3.amazonaws.com/files/2023-03-03/25d956f4-5d8f-465f-9ec6-d210e3bd5374/ascreenshot.jpeg?tl\_px=1483,50\&br\_px=2976,890\&sharp=0.8\&width=560\&wat\_scale=50\&wat=1\&wat\_opacity=0.7\&wat\_gravity=northwest\&wat\_url=https://colony-labs-public.s3.us-east-2.amazonaws.com/images/watermarks/watermark\_default.png\&wat\_pad=262,139)

**7. Click "Owner"**

![](https://ajeuwbhvhr.cloudimg.io/colony-recorder.s3.amazonaws.com/files/2023-03-03/8a215264-34ca-43e5-9735-b21d910c58f2/ascreenshot.jpeg?tl\_px=1753,64\&br\_px=3246,904\&sharp=0.8\&width=560\&wat\_scale=50\&wat=1\&wat\_opacity=0.7\&wat\_gravity=northwest\&wat\_url=https://colony-labs-public.s3.us-east-2.amazonaws.com/images/watermarks/watermark\_default.png\&wat\_pad=262,139)

**8. Click "Mode"**

![](https://ajeuwbhvhr.cloudimg.io/colony-recorder.s3.amazonaws.com/files/2023-03-03/7329a4d2-b094-4667-afba-727caaec55d5/ascreenshot.jpeg?tl\_px=1962,62\&br\_px=3455,902\&sharp=0.8\&width=560\&wat\_scale=50\&wat=1\&wat\_opacity=0.7\&wat\_gravity=northwest\&wat\_url=https://colony-labs-public.s3.us-east-2.amazonaws.com/images/watermarks/watermark\_default.png\&wat\_pad=350,139)

**9. Click here.**

![](https://ajeuwbhvhr.cloudimg.io/colony-recorder.s3.amazonaws.com/files/2023-03-03/24267c6f-fa37-4bac-a450-b2fd8f1d895b/ascreenshot.jpeg?tl\_px=1962,58\&br\_px=3455,898\&sharp=0.8\&width=560\&wat\_scale=50\&wat=1\&wat\_opacity=0.7\&wat\_gravity=northwest\&wat\_url=https://colony-labs-public.s3.us-east-2.amazonaws.com/images/watermarks/watermark\_default.png\&wat\_pad=465,139)

**10. Click "add Add API"**

![](https://ajeuwbhvhr.cloudimg.io/colony-recorder.s3.amazonaws.com/files/2023-03-03/a2485ad4-4406-40c0-820f-4685863ebb4f/ascreenshot.jpeg?tl\_px=1962,0\&br\_px=3455,840\&sharp=0.8\&width=560\&wat\_scale=50\&wat=1\&wat\_opacity=0.7\&wat\_gravity=northwest\&wat\_url=https://colony-labs-public.s3.us-east-2.amazonaws.com/images/watermarks/watermark\_default.png\&wat\_pad=461,73)

### The Applications menu

The Applications menu is where you can keep track of and view various information&#x20;
