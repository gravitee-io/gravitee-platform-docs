---
description: >-
  This page walks you through how to configure load-balancing, failover, and
  health checks for your Gravitee APIs and endpoints.
---

# Configure Load-balancing, Failover, and Health Checks for your APIs

### Introduction: load-balancing, failover, and health checks

Gravitee API Management (APIM) offers three main backend services for managing your APIs. These services are:&#x20;

* **Load-balancing:** a technique used to distribute incoming traffic across multiple backend servers. The goal of load balancing is to optimize resource utilization, maximize throughput, minimize response time, and avoid overloading any single server.
* **Failover:** a mechanism to ensure high availability and reliability of APIs by redirecting incoming traffic to a secondary server or backup system in the event of a primary server failure.
* **Health checks:** a mechanism used to monitor the availability and health of your endpoints and/or your API gateways.

All of these capabilities are built in to the Gravitee APIM platform. The rest of this article will focus on how to configure these services; if you want more conceptual explanations of the services, please refer to the [Concepts sections on load-balancing, failover, and health checks](../concepts.md#load-balancing).&#x20;



### How to configure load-balancing in Gravitee

To configure load-balancing in Gravitee, follow these steps:

1\. Log in to the Gravitee API Management UI.

2\. Load-balancing (as well other backend services) are configured per API. So, head to the APIs menu.

![Load-balancing: select the APIs menu.](https://ajeuwbhvhr.cloudimg.io/colony-recorder.s3.amazonaws.com/files/2023-03-07/95d2995f-b5b8-482a-bdd8-8109315e9bb7/ascreenshot.jpeg?tl\_px=0,38\&br\_px=1493,878\&sharp=0.8\&width=560\&wat\_scale=50\&wat=1\&wat\_opacity=0.7\&wat\_gravity=northwest\&wat\_url=https://colony-labs-public.s3.us-east-2.amazonaws.com/images/watermarks/watermark\_default.png\&wat\_pad=39,139)

3\. Find and select the API for which you want to configure load-balancing.

![](https://ajeuwbhvhr.cloudimg.io/colony-recorder.s3.amazonaws.com/files/2023-03-07/ffb6f144-5f64-474e-9aec-e636a81093d9/ascreenshot.jpeg?tl\_px=0,0\&br\_px=1493,840\&sharp=0.8\&width=560\&wat\_scale=50\&wat=1\&wat\_opacity=0.7\&wat\_gravity=northwest\&wat\_url=https://colony-labs-public.s3.us-east-2.amazonaws.com/images/watermarks/watermark\_default.png\&wat\_pad=232,128)

4\. Select the Edit API icon.

![](https://ajeuwbhvhr.cloudimg.io/colony-recorder.s3.amazonaws.com/files/2023-03-07/2d11dc86-a65a-4c5d-9b1f-cf9646055f77/ascreenshot.jpeg?tl\_px=1962,146\&br\_px=3455,986\&sharp=0.8\&width=560\&wat\_scale=50\&wat=1\&wat\_opacity=0.7\&wat\_gravity=northwest\&wat\_url=https://colony-labs-public.s3.us-east-2.amazonaws.com/images/watermarks/watermark\_default.png\&wat\_pad=477,139)

5\. Select Backend services

![](https://ajeuwbhvhr.cloudimg.io/colony-recorder.s3.amazonaws.com/files/2023-03-07/a87da572-ba67-4258-9d29-3be916be39c1/ascreenshot.jpeg?tl\_px=0,628\&br\_px=1493,1468\&sharp=0.8\&width=560\&wat\_scale=50\&wat=1\&wat\_opacity=0.7\&wat\_gravity=northwest\&wat\_url=https://colony-labs-public.s3.us-east-2.amazonaws.com/images/watermarks/watermark\_default.png\&wat\_pad=247,139)

6\. From here, you can either configure load-balancing for existing endpoint groups or, create a new endpoint group for which to configure load-balancing. For the sake of this article, we will create a new endpoint group from scratch. To do so, select + Add new endpoint group.

![](https://ajeuwbhvhr.cloudimg.io/colony-recorder.s3.amazonaws.com/files/2023-03-07/9478f6d1-c0fe-4cb9-acef-577b03d234f8/ascreenshot.jpeg?tl\_px=1962,0\&br\_px=3455,840\&sharp=0.8\&width=560\&wat\_scale=50\&wat=1\&wat\_opacity=0.7\&wat\_gravity=northwest\&wat\_url=https://colony-labs-public.s3.us-east-2.amazonaws.com/images/watermarks/watermark\_default.png\&wat\_pad=411,132)

7\. You'll be taken to the General tab. Here, you will name your endpoint group and select the load balancing algorithm. For the sake of this article, I will select Round robin.

{% hint style="info" %}
Please refer to the load-balancing concepts section if you need in-depth explanations of the various load-balancing algorithms that Gravitee supports.
{% endhint %}

![](https://colony-recorder.s3.amazonaws.com/files/2023-03-07/0f165e09-c3b5-43fc-b760-d34585ecd629/stack\_animation.webp)

8\. Now, it's time to configure your endpoint group with any additional HTTP details that might be relevant. To do so, select Configuration.

![](https://ajeuwbhvhr.cloudimg.io/colony-recorder.s3.amazonaws.com/files/2023-03-07/2bb0a7e1-883c-4a37-9cee-ffad16f3ee17/ascreenshot.jpeg?tl\_px=751,0\&br\_px=2244,840\&sharp=0.8\&width=560\&wat\_scale=50\&wat=1\&wat\_opacity=0.7\&wat\_gravity=northwest\&wat\_url=https://colony-labs-public.s3.us-east-2.amazonaws.com/images/watermarks/watermark\_default.png\&wat\_pad=262,111)

**9. Configure your HTTP details to your liking. For example, I might choose to enable HTTP pipelining, which will cause requests to be written to connections without waiting for previous responses to return. You can configure many other additional details, such as HTTP protocol version, Connect timeout time (in ms), idle timeout (in ms), SSL options, and more.**

![](https://colony-recorder.s3.amazonaws.com/files/2023-03-07/7526630f-4033-4b9d-9d41-0062e12ea856/stack\_animation.webp)

**10. Optional: if you want to enable Service Discovery, select the Service discovery tab. Service discovery will enable external endpoints to be dynamically added or removed to or from the group. For more information on Service Discovery, please refer to our documentation on Gravitee Service discovery.**

![](https://colony-recorder.s3.amazonaws.com/files/2023-03-07/cf7799b5-28eb-4dff-9895-1e7a6f481edb/stack\_animation.webp)

**11. Once you are done defining and configuring your endpoint group, select Create.**

![](https://ajeuwbhvhr.cloudimg.io/colony-recorder.s3.amazonaws.com/files/2023-03-07/46fa5604-2509-48c7-ae72-7c0176a7e4ef/ascreenshot.jpeg?tl\_px=1962,556\&br\_px=3455,1396\&sharp=0.8\&width=560\&wat\_scale=50\&wat=1\&wat\_opacity=0.7\&wat\_gravity=northwest\&wat\_url=https://colony-labs-public.s3.us-east-2.amazonaws.com/images/watermarks/watermark\_default.png\&wat\_pad=417,139)

**12. Now, it's time to add endpoints to your endpoint group. Once you've done this, you'll be able to configure load-balancing for your endpoint group. Let's head back to the Endpoints section of the Backend Services menu.**

![](https://ajeuwbhvhr.cloudimg.io/colony-recorder.s3.amazonaws.com/files/2023-03-07/e338a81b-8c36-4cf1-b927-3f4b7204cea6/ascreenshot.jpeg?tl\_px=489,0\&br\_px=1982,840\&sharp=0.8\&width=560\&wat\_scale=50\&wat=1\&wat\_opacity=0.7\&wat\_gravity=northwest\&wat\_url=https://colony-labs-public.s3.us-east-2.amazonaws.com/images/watermarks/watermark\_default.png\&wat\_pad=262,78)

\*\*13. You'll see your endpoint group. To add endpoints to this group, select + Add endpoint. \*\*

![](https://ajeuwbhvhr.cloudimg.io/colony-recorder.s3.amazonaws.com/files/2023-03-07/323033e1-0584-474a-87f4-4f9ad075a8e8/ascreenshot.jpeg?tl\_px=1823,560\&br\_px=3316,1400\&sharp=0.8\&width=560\&wat\_scale=50\&wat=1\&wat\_opacity=0.7\&wat\_gravity=northwest\&wat\_url=https://colony-labs-public.s3.us-east-2.amazonaws.com/images/watermarks/watermark\_default.png\&wat\_pad=262,139)

**14. In the General tab, define your endpoint name, target URL, weight (if you chose a weighted load-balancing algorithm), and your tenants. Click here.**

![](https://colony-recorder.s3.amazonaws.com/files/2023-03-07/accdc8c6-ee91-4bd6-a351-9c3a2656360f/stack\_animation.webp)

**15. Optional: select Secondary endpoint to define this endpoint outside the main load balancing pool. This will make the endpoint used for load balancing only if all the primary endpoints are marked as down by the health check.**

![](https://ajeuwbhvhr.cloudimg.io/colony-recorder.s3.amazonaws.com/files/2023-03-07/49f626c6-5ee4-45df-a8f3-5cb76bbcb15d/ascreenshot.jpeg?tl\_px=763,1098\&br\_px=2256,1938\&sharp=0.8\&width=560\&wat\_scale=50\&wat=1\&wat\_opacity=0.7\&wat\_gravity=northwest\&wat\_url=https://colony-labs-public.s3.us-east-2.amazonaws.com/images/watermarks/watermark\_default.png\&wat\_pad=262,141)

**16. Once you're finished specifying endpoint details in the General tab, its time to configure the HTTP configuration for your endpoint.**

![](https://ajeuwbhvhr.cloudimg.io/colony-recorder.s3.amazonaws.com/files/2023-03-07/da0973c3-44ba-4cd0-a288-e6ce86b4f185/ascreenshot.jpeg?tl\_px=849,166\&br\_px=2342,1006\&sharp=0.8\&width=560\&wat\_scale=50\&wat=1\&wat\_opacity=0.7\&wat\_gravity=northwest\&wat\_url=https://colony-labs-public.s3.us-east-2.amazonaws.com/images/watermarks/watermark\_default.png\&wat\_pad=262,139)

**17. By default, the endpoint will inherit configuration from the configuration that you set at the endpoint group level.**

![](https://ajeuwbhvhr.cloudimg.io/colony-recorder.s3.amazonaws.com/files/2023-03-07/b882af4c-95c0-44b4-ad35-c17a56dbdc5b/ascreenshot.jpeg?tl\_px=991,152\&br\_px=2484,992\&sharp=0.8\&width=560\&wat\_scale=50\&wat=1\&wat\_opacity=0.7\&wat\_gravity=northwest\&wat\_url=https://colony-labs-public.s3.us-east-2.amazonaws.com/images/watermarks/watermark\_default.png\&wat\_pad=262,139)

\*\*18. However, if you want to set up HTTP configuration specific to that endpoint, toggle the Inherit configuration OFF. \*\*

![](https://ajeuwbhvhr.cloudimg.io/colony-recorder.s3.amazonaws.com/files/2023-03-07/27891695-83ec-4bf9-9632-5ea5cccf978b/ascreenshot.jpeg?tl\_px=1962,238\&br\_px=3455,1078\&sharp=0.8\&width=560\&wat\_scale=50\&wat=1\&wat\_opacity=0.7\&wat\_gravity=northwest\&wat\_url=https://colony-labs-public.s3.us-east-2.amazonaws.com/images/watermarks/watermark\_default.png\&wat\_pad=444,139)

**19. Once toggled OFF, you can specify a different HTTP configuration for this endpoint. Once you are done, select Save.**

![](https://ajeuwbhvhr.cloudimg.io/colony-recorder.s3.amazonaws.com/files/2023-03-07/b89754c6-06e2-470b-9d7c-355330809ea0/ascreenshot.jpeg?tl\_px=1962,0\&br\_px=3455,840\&sharp=0.8\&width=560\&wat\_scale=50\&wat=1\&wat\_opacity=0.7\&wat\_gravity=northwest\&wat\_url=https://colony-labs-public.s3.us-east-2.amazonaws.com/images/watermarks/watermark\_default.png\&wat\_pad=447,122)

\*\*20. For the sake of this example, let's toggle the Inherit configuration back ON. \*\*

![](https://ajeuwbhvhr.cloudimg.io/colony-recorder.s3.amazonaws.com/files/2023-03-07/fd85c6d5-7a13-4dd2-aab8-443fac87cabe/ascreenshot.jpeg?tl\_px=1962,286\&br\_px=3455,1126\&sharp=0.8\&width=560\&wat\_scale=50\&wat=1\&wat\_opacity=0.7\&wat\_gravity=northwest\&wat\_url=https://colony-labs-public.s3.us-east-2.amazonaws.com/images/watermarks/watermark\_default.png\&wat\_pad=443,139)

21\. Once you're done with your HTTP configuration, you can set up a health check for your endpoint. To learn more about setting up health checks, please refer to the "Health checks" section of this article.

![](https://ajeuwbhvhr.cloudimg.io/colony-recorder.s3.amazonaws.com/files/2023-03-07/78ed5ccd-93d8-41fb-a9c2-9f3790d8f7ce/ascreenshot.jpeg?tl\_px=1962,312\&br\_px=3455,1152\&sharp=0.8\&width=560\&wat\_scale=50\&wat=1\&wat\_opacity=0.7\&wat\_gravity=northwest\&wat\_url=https://colony-labs-public.s3.us-east-2.amazonaws.com/images/watermarks/watermark\_default.png\&wat\_pad=465,139)
