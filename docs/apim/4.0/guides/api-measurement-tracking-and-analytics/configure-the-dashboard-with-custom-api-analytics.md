---
description: >-
  Learn how to set up your Dashboard and various analytics options for APIs and
  applications.
---

# Configure the Dashboard with Custom API Analytics

### Introduction

This article focuses on how to customize and build your Gravitee Dashboard, complete with analytics and charts for your APIs and applications.

### The Dashboard <a href="#the-dashboard" id="the-dashboard"></a>

The Gravitee "Dashboard" is an area in the UI where you'll be able to create custom dashboards around API performance, status, lifecycle stage, and more. The Dashboard is comprised of four main modules:

* **The "Home" board module:** This is your "Metrics and analytics homepage." You can configure this page to show chosen charts, filter chart data based on time range, and configure how regularly the charts should be refreshed.
* **The "API Status" module:** this module shows you status and availability of your APIs across time. You can filter which APIs to view and what for time range you want to view API status and availability.
* **The "Analytics" module:** the analytics module is where you can see and slightly configure all of the various dashboards, charts, etc. that refer to your Gravitee API analytics. You can build multiple analytics dashboards and view them all from this page. Your "Home board" will be pulling charts from these various dashboards.
* **The "Alerts" module:** this module is for keeping track of all API alerts over a given amount of time.

To see what the Gravitee Dashboard is like, feel free to explore the UI via the interactive tutorial below:

{% @arcade/embed flowid="bTYh1yLqcbJU6xaGZQZm" url="https://app.arcade.software/share/bTYh1yLqcbJU6xaGZQZm" %}

#### Add dashboards to your Analytics tab

You are able to control what kinds of information and charts are presented on your Gravitee Dashboard by adding custom dashboards to your Analytics tab. Gravitee enables you to create charts for three different categories:

* Platform
* API
* Applications

To do so follow along with the interactive tutorial or follow the written steps. Both are below.

{% @arcade/embed flowid="nnYHELNaqBTNKvxqrQIL" url="https://app.arcade.software/share/nnYHELNaqBTNKvxqrQIL" %}

To add a dashboard to your Analytics tab, follow these steps:

1\. Log in to the API Management Console.

![](https://dubble-prod-01.s3.amazonaws.com/assets/5342ad4f-9b3f-4b92-a96b-5f4185f39799.png?0)

2\. Select **Settings**.

![](https://d3q7ie80jbiqey.cloudfront.net/media/image/zoom/cd439d7c-fc9e-497b-bd7b-56a161e9b08e/1.5/3.7037037037037/45.768833849329?0)

3\. Under **Dashboards** and **Platform**, select **Add a new platform dashboard**.

![](https://d3q7ie80jbiqey.cloudfront.net/media/image/zoom/0fe33cbd-132a-43dc-9dfe-4696d7b9e491/1/31.655092592593/65.644349845201?0)

4\. Here, you can define your dashboard by giving it a **Dashboard name** and a **Query filter** (optional).

![](https://d3q7ie80jbiqey.cloudfront.net/media/image/zoom/9a55d067-1636-423a-8c90-01e4ed7798cf/1.3104163767772/58.925826461227/29.411764705882?0)

5\. Select **Save**.

![](https://d3q7ie80jbiqey.cloudfront.net/media/image/zoom/8d25bf16-8576-4b1a-b471-b3fbdca61011/1.0539568345324/63.483796296296/37.564499484004?0)

10\. Now, let's add widgets to your dashboard. To add a widget to your dashboard, select the **Add a widget** icon in the bottom right-hand corner of your screen.

![](https://d3q7ie80jbiqey.cloudfront.net/media/image/zoom/a8d61d4c-92a2-4e39-b0f7-b7bc04e6a0c3/1/98.37962962963/97.316821465428?0)

11\. Now, you can start creating your widget. First, define the **Widget type**.

![](https://d3q7ie80jbiqey.cloudfront.net/media/image/zoom/b24f5738-4f80-4263-98fc-9aad26952f8c/1/43.036114728009/73.684210526316?0)

12\. For this example, we'll create a **table**. All of these types are pre-canned in Gravitee.

![](https://d3q7ie80jbiqey.cloudfront.net/media/image/zoom/ea8fc30d-a0a5-4078-9ede-73b2a7766c33/1/43.036114728009/74.716202270382?0)

13\. Give your widget a **Name** and (optionally) a **Subtitle**.

![](https://d3q7ie80jbiqey.cloudfront.net/media/image/zoom/1c18009a-c477-448e-8794-c37a5f85d4a3/1/33.796296296296/53.973168214654?0)

14\. If you prefer, you can use a **custom field**.

![](https://d3q7ie80jbiqey.cloudfront.net/media/image/zoom/d3ba85e8-2121-4e8d-b1e4-37bc3ab96f8d/2.5/33.796296296296/59.029927760578?0)

15\. We'll use Gravitee fields. Choose your field in the **Field** drop-down.

![](https://d3q7ie80jbiqey.cloudfront.net/media/image/zoom/ab2417d3-0c33-4bc8-890f-afa9b281f043/2.5/37.5/68.111455108359?0)

16\. We'll choose **API**.

![](https://d3q7ie80jbiqey.cloudfront.net/media/image/zoom/7d151601-e908-4045-9d8d-ed5911d240af/2.5/32.87037037037/69.865841073271?0)

17\. Now, its a matter of building a widget that contains the information you want around APIs (or whatever else you may have chosen).

![](https://d3q7ie80jbiqey.cloudfront.net/media/image/zoom/110aefe7-5e9d-4d60-95c8-4d0991a27278/2.5/37.5/73.168214654283?0)

![](https://d3q7ie80jbiqey.cloudfront.net/media/image/zoom/f099468d-bfa2-4755-9bcd-40996a5676da/2.5/32.87037037037/74.922600619195?0)

![](https://d3q7ie80jbiqey.cloudfront.net/media/image/zoom/483deed1-149f-418c-8200-5d538876dc39/2.5/33.796296296296/78.328173374613?0)

20\. When you're done, select **Save**.

![](https://d3q7ie80jbiqey.cloudfront.net/media/image/zoom/7bf6935f-693d-41ea-a7e8-469ab35bf518/2.5/31.655092592593/87.616099071207?0)

21\. If you'd like, you can preview your new dashboard with its new widget. To do, select **Enable Preview.**

![](https://d3q7ie80jbiqey.cloudfront.net/media/image/zoom/84178b56-8501-419b-bd91-9644f9283ec4/1/97.164351851852/37.358101135191?0)

22\. To see your dashboard in the "real world," head back to the **Dashboard**.

![](https://d3q7ie80jbiqey.cloudfront.net/media/image/zoom/c6e6f633-038d-49f0-90a1-3ef8e57bc6ac/2.5/0.92592592592593/16.047471620227?0)

23\. Select **Analytics**.

![](https://d3q7ie80jbiqey.cloudfront.net/media/image/zoom/0197030d-2b58-4264-a7e8-1e6d0aa4dd58/1.5/65.740740740741/9.5975232198142?0)

24\. Choose your dashboard from the **Select a dashboard** drop-down menu.

![](https://d3q7ie80jbiqey.cloudfront.net/media/image/zoom/8b3a1f39-0f38-44ba-99df-c5b99bd7e3bf/2.5/96.064814814815/19.401444788442?0)

25\. Select your dashboard.

![](https://d3q7ie80jbiqey.cloudfront.net/media/image/zoom/d62cf172-5b1d-4989-9299-3c6a550bf033/2.5/95.017722800926/41.176470588235?0)

{% hint style="success" %}
If you followed the above steps, you'll see your new dashboard and widget.

<img src="../../.gitbook/assets/image (95) (1).png" alt="" data-size="original">
{% endhint %}

#### Edit existing Analytics dashboards

In addition to adding new dashboards, you can also configure and re-configure existing dashboards in the Analytics tab. To do so, either use the interactive tutorial or follow the written steps. Both are below.

1\. Log in to the Gravitee API Management Console.

2\. Select **Settings**.

![](https://d3q7ie80jbiqey.cloudfront.net/media/image/zoom/0b4676ec-859b-4f97-ac47-9d6b3eaeb8ba/1.5/3.7037037037037/45.768833849329?0)

3\. Select the dashboard that you want to edit.

![](https://d3q7ie80jbiqey.cloudfront.net/media/image/zoom/01712ed7-1978-44f9-aa16-67997e75638b/1/31.886574074074/56.384642672859?0)

4\. Here, you can: define basic details for your dashboard enable and disable your dashboard set query filters and edit each individual chart that appears on your dashboard.

![](https://d3q7ie80jbiqey.cloudfront.net/media/image/zoom/9114c854-958a-4b4c-adce-620f521bc76d/1/88.916467737269/29.721362229102?0)

5\. Let's show what it looks like to edit an individual chart. Select the **Edit** icon for a chart that you'd like to edit/configure.

![](https://d3q7ie80jbiqey.cloudfront.net/media/image/zoom/dc935880-feb6-49db-ba80-2e313a37a4c6/1/49.989981121487/52.012383900929?0)

6\. Once inside the chart details, you can edit basic details like **Title** and **Subtitle**, decide to use custom fields, choose which pre-canned fields that you want to display (such as **Status**, Global **latency**, **API latency**, and more), and alter details around data presentation.

![](https://d3q7ie80jbiqey.cloudfront.net/media/image/zoom/37671ced-2937-4906-bb49-b18ba90527b7/2/41.765676336619/74.354274681779?0)

7. Once you're done, select **Save**. Depending on how many charts you have, this might require some scrolling all the way down to the bottom of this page.
