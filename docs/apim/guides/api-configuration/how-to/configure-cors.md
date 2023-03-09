---
description: >-
  This article focuses on how to configure the General Proxy settings for an
  API, which includes Entrypoints, CORS, Deployments, and Response Templates
  configurations.
---

# Configure General Proxy settings

### Introduction

In Gravitee, there is a **General** subsection of the **Proxy** section. In the **General** section, you can configure the following settings per API:

* Entrypoints
* CORS
* Deployments
* Response Templates

This article walks through how to configure each of the above.

### Configure Entrypoints

To configure Entrypoints, follow the below interactive tutorial, or, follow the numbered steps below.

{% @arcade/embed flowId="4353kgHZvdMRtEEL5xy9" url="https://app.arcade.software/share/4353kgHZvdMRtEEL5xy9" %}

If you prefer to use a written list of steps, follow these steps:

1\. Log in to the Gravitee API Management UI.

2\. In the **APIs** menu, select the API for whom you want to configure Entrypoints.

![](https://d3q7ie80jbiqey.cloudfront.net/media/image/zoom/665c071d-8767-48ce-8690-c3261769fda0/1/24.166666666667/22.11524135876?0)

3\. Select the **Edit API** icon.

![](https://d3q7ie80jbiqey.cloudfront.net/media/image/zoom/0c8fd2c2-43d7-4985-9b69-31dc00f385d8/1/96.666666666667/58.377719010727?0)

4\. Find the **Proxy** section in the left-hand nav. Select **General**.

![](https://d3q7ie80jbiqey.cloudfront.net/media/image/zoom/e7e8492f-4889-42ec-a420-5dcc08d39a15/1/20/61.144219308701?0)

5\. The **Entrypoints** tab is automatically selected.

![](https://d3q7ie80jbiqey.cloudfront.net/media/image/zoom/e2d81981-357a-4d7d-a985-0eff3aba449d/1/50.166666666667/11.084624553039?0)

6\. Define your **Context path**. This is the URL location of your API. So if your URL is \[https://apim-master-gateway.team-apim.gravitee.dev/myAPI], then \[/myAPI] is the context path.

{% hint style="info" %}
This is the path where your API is exposed. It must start with a '/' and can only contain any letter, capitalized letter, number, dash, or underscore.
{% endhint %}

![](https://d3q7ie80jbiqey.cloudfront.net/media/image/zoom/5d7e90d7-3bf8-4abd-b7eb-3c0a3dbab79c/1/57.771484375/42.353247914184?0)

{% hint style="success" %}
Select **Save**. You've now configured your Entrypoints.
{% endhint %}

### Configure CORS

CORS is a mechanism that allows resources on a web page to be requested from another domain. For background information on CORS, take a look at the [CORS specification](https://www.w3.org/TR/cors). This article will focus on how to configure CORS for your API. If you want to know more about CORS at the conceptual level, refer to the CORS "Concepts" article. If you want to learn more about CORS at a conceptual level, we recommend referring to the [CORS section](../concepts.md#cors) of the "Concepts" article for this section.

To configure CORS for an API, follow these steps:

1\. Log into your Gravitee API Management UI.

2\. Select the **APIs** menu. Find the API for which you want to configure CORS.

![](https://dubble-prod-01.s3.amazonaws.com/assets/6121e44d-f50d-411b-8194-4ae9a611d2f8.png?0)

3\. Select the **Edit API** icon.

![](https://d3q7ie80jbiqey.cloudfront.net/media/image/zoom/0cceaf2b-d55e-4d94-84ec-eb9a2f0cf227/1.5/95.833333333333/49.307436790506?0)

4\. In the **Proxy** section, select **General**.

![](https://d3q7ie80jbiqey.cloudfront.net/media/image/zoom/08ef1ea0-f0b6-4864-871c-6485c36da949/1/13.888888888889/51.083591331269?0)

5\. Select the **CORS** tab.

![](https://d3q7ie80jbiqey.cloudfront.net/media/image/zoom/673f58c2-755c-43b9-8d99-f9c447cb7c57/1.5/39.467592592593/9.5975232198142?0)

6\. Toggle **Enable CORS** ON.

![](https://d3q7ie80jbiqey.cloudfront.net/media/image/zoom/ad4c811b-6b25-46a2-9ed5-6ea23d2922eb/1.5/36.082175925926/25.077399380805?0)

7\. If you want to allow origins, enter **\*** in the **Allow Origins** field. This will define the one or multiple origins that can access the resource.

{% hint style="danger" %}
We do _not_ recommend this configuration for production environments. By allowing cross-origin requests, a server may inadvertently expose sensitive information to unauthorized parties. For example, if a server includes sensitive data in a response that is accessible via CORS, an attacker could use a malicious website to extract that data.
{% endhint %}

![](https://d3q7ie80jbiqey.cloudfront.net/media/image/zoom/b47f940f-9f12-41f3-a8e3-a0384bd89b0f/1.2507598784195/64.178240740741/40.041279669763?0)

8. In the **Access-Control-Allow-Methods** field, define the method or methods allowed to access the resource. This is used in response to a preflight request.

![](https://d3q7ie80jbiqey.cloudfront.net/media/image/zoom/147983dc-6642-4edb-86b3-7fef719710b0/1.1441484300666/63.715277777778/60.108681630547?0)

9\. In the **Access-Control-Request-Headers** drop down, define which headers will be allowed in your requests. Typically, your request header will include `Access-Control-Request-Headers`, which relies on the CORS configuration to allow its values.

![](https://d3q7ie80jbiqey.cloudfront.net/media/image/zoom/55c5eab5-8152-40a1-a714-6497076f9c01/1.3094240837696/64.178240740741/89.869549793602?0)

10\. If you want to allow the response to the request to be exposed when the credentials flag is true, toggle **Access-Control-Allow-Credentials** ON.

![](https://d3q7ie80jbiqey.cloudfront.net/media/image/zoom/0ac57e83-1116-4a83-92a7-25e5845468a3/2/35.619212962963/55.575174148607?0)

11\. In the **Access-Control-Allow-Max-Age** field, define how long the results of preflight requests can be cached. This is optional, and `-1` will be the value if this is disabled.

![](https://d3q7ie80jbiqey.cloudfront.net/media/image/zoom/c2704a8a-aa9b-4e00-beca-2789cbe40a34/1.2507598784195/64.178240740741/55.93072755418?0)

12\. In the **Access-Control-Expose-Headers** field, you can define a list of headers that browsers are allowed to access.

![](https://d3q7ie80jbiqey.cloudfront.net/media/image/zoom/a45c9e34-8b63-44f3-a4ca-9394d148a8c2/1.2507598784195/64.178240740741/70.663215944272?0)

13\. If you want the API Gateway to execute policies for preflight-requests, toggle **Run policies for preflight requests** ON. By default, this is not enabled.

![](https://d3q7ie80jbiqey.cloudfront.net/media/image/zoom/869aea62-91f0-4929-8471-4a10b0193fbd/2/60.345262096774/93.644675510936?0)

{% hint style="success" %}
You've configured your CORS settings for your API. When you are done, select **Save.**.&#x20;
{% endhint %}

{% hint style="info" %}
**Troubleshooting CORS**

All requests rejected because of CORS issues will generate logs that you can view in the `Analytics` section of your API logs.

![](<../../../.gitbook/assets/graviteeio-troubleshooting-cors (1).png>)
{% endhint %}

### Configure Deployments

The **Deployments** tab is where you can choose to use Sharding tags to control where your API is deployed. For more information on Sharding tags, what they are useful for, and how to configure them, please refer to our "How-to" article on configuring Sharding tags.

To choose Sharding tags, follow the below interactive tutorial, or, follow the numbered steps below.

{% @arcade/embed flowId="d6TOgaGsnGu4ycqJ4PUr" url="https://app.arcade.software/share/d6TOgaGsnGu4ycqJ4PUr" %}

1\. Log in to the API Management UI.

![](https://dubble-prod-01.s3.amazonaws.com/assets/c21bd268-c8c7-4716-a0b4-897b5ff9a96b.png?0)

2\. Select the **APIs** menu.

![](https://d3q7ie80jbiqey.cloudfront.net/media/image/zoom/9ab2716a-118b-4eb0-b1f1-b0961edf401a/1/1.3333333333333/23.301549463647?0)

3\. Select the API for which you want to configure Deployments.

![](https://d3q7ie80jbiqey.cloudfront.net/media/image/zoom/8f848b27-8130-4f2a-9b4b-979e61138eee/1/24.166666666667/22.11524135876?0)

4\. Select the **Edit API** icon.

![](https://d3q7ie80jbiqey.cloudfront.net/media/image/zoom/0c93469f-f6a1-45cf-a30e-98abaa26b355/1/96.666666666667/58.377719010727?0)

5\. Under **Proxy**, select **General**.

![](https://d3q7ie80jbiqey.cloudfront.net/media/image/zoom/9203d84f-2fdc-4448-a42f-a8688d989a4a/1/20/61.144219308701?0)

6\. Select the **Deployments** tab.

![](https://d3q7ie80jbiqey.cloudfront.net/media/image/zoom/04d84637-14ed-4147-ab3a-ad01a01de22e/1.5/83.5/11.084624553039?0)

7\. Select the **Sharding tags** drop down menu.

![](https://d3q7ie80jbiqey.cloudfront.net/media/image/zoom/2b14b4dd-bbb5-4f59-95c8-5b4966ff8ee0/1.5/98.26953125/31.236032479142?0)

8\. Choose the Sharding tag that you want to assign to the API. This will dictate where it is deployed.

![](https://d3q7ie80jbiqey.cloudfront.net/media/image/zoom/d019ecb2-ac33-417e-abe5-76a8f04dcabb/1.5/41.708333333333/53.003016984505?0)

{% hint style="success" %}
Select Save. You will have successfully configured your API deployment settings via choosing a sharding tag.
{% endhint %}

### Configure Response Templates

If you want to define your own response templa
