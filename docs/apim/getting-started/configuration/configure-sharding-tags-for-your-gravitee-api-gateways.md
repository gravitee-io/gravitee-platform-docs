---
description: >-
  This article describes how to configure sharding tags when customizing
  deployments via your API proxy settings.
---

# Sharding tags

{% hint style="warning" %}
**Enterprise only**

As of Gravitee 4.0, the sharding tags feature is an Enterprise Edition capability. To learn more about Gravitee EE and what's included in various enterprise packages:

* [Refer to the EE vs OSS documentation](../../overview/introduction-to-gravitee-api-management-apim/ee-vs-oss.md)
* [Book a demo](http://127.0.0.1:5000/o/8qli0UVuPJ39JJdq9ebZ/s/rYZ7tzkLjFVST6ex6Jid/)
* [Check out the pricing page](https://www.gravitee.io/pricing)
{% endhint %}

{% hint style="info" %}
**v4 API limitations**

As of Gravitee 4.0, you cannot implement sharding tags for v4 APIs using the APIM Console. This can only be done via the [Management API](../../reference/management-api-reference/).&#x20;
{% endhint %}

## Introduction

Sharding tags allow you to “tag” a Gateway with a specific keyword. Once a Gateway is tagged, you are able to deploy an API to a Gateway with the selected sharding tag. To learn more about how to deploy APIs to specific Gateways based on sharding tags, refer to [this documentation](../../guides/api-configuration/v2-api-configuration/configure-cors.md#configure-deployments).

### Configure sharding tags for your Gravitee API Gateways

Our discussion of sharding tag configuration assumes that the architecture includes both DMZ Gateways and internal, corporate Gateways. We want to tag these Gateways as external only and internal only, respectively, per the corresponding diagram below:

<figure><img src="../../.gitbook/assets/Example architecture (1).png" alt=""><figcaption></figcaption></figure>

Before you can define sharding tags in the Gravitee API Management Console, you will need to modify your API Gateway `gravitee.yaml` file. To assign a Gravitee API Gateway to a specific sharding tag for the above scenario and architecture, make the following changes in the `gravitee.yaml` file:

```
DMZ Gateways: 
tags: ‘external’
```

```
Internal Network Gateways:
tags: ‘internal’
```

Gateways can be tagged with one or more sharding tags, and you can add more nuance to the tagging strategy by specifying exclusion rules via the`!` symbol before the tag name. For example, imagine you have Gateways tagged as “external” and also as “partner." If you wanted to configure a Gateway so that it can host external APIs that are not dedicated to partners, you would define the sharding tag like this:

```
tags: ‘product,store,!partner’
```

Once the Gateways have been tagged, you will need to define the same sharding tags within API Manager:

1. Log in to your API Management Console.

![](https://dubble-prod-01.s3.amazonaws.com/assets/c04ad6f1-b85c-4196-bb64-dbcb62c22c97.png?0)

2. In the left-hand nav, select **Organization**.

![](https://d3q7ie80jbiqey.cloudfront.net/media/image/zoom/ed080e94-c73d-48a0-8c1c-6170de95b250/1/3.7037037037037/88.486842105263?0)

3. On the Organization page, select **Sharding tags**.

![](https://d3q7ie80jbiqey.cloudfront.net/media/image/zoom/ef5532a2-ba56-49ae-b438-041ed3ff5c9d/1.5/0.34722222222222/42.47618558114?0)

4. Click **+ Add a tag.**

![](https://d3q7ie80jbiqey.cloudfront.net/media/image/zoom/50391eb9-7eda-480f-97ce-4f86d6bfb9d7/1.5/84.548611111111/24.835526315789?0)

5. Create the same tags that you created in the `gravitee.yaml` file and ensure that the names are an exact match. First, let's create the "internal" tag using the **Name** field.

![](https://d3q7ie80jbiqey.cloudfront.net/media/image/zoom/71721c67-2277-400a-b577-790311e3d38d/2.5/50/43.23516310307?0)

6. (Optional) You can choose to restrict groups. This restricts usage of the tag to certain groups, as defined in Gravitee user administration. We'll skip this.

![](https://d3q7ie80jbiqey.cloudfront.net/media/image/zoom/56135924-46cc-45a5-baf2-69e0e937ef5a/2.5/50/54.913651315789?0)

7. Click **Ok**.

![](https://d3q7ie80jbiqey.cloudfront.net/media/image/zoom/a27f351a-c1c3-44a5-ac8c-f6d15b4a7eba/2.5/60.272442853009/75.206448739035?0)

8. Let's add the "external" tag. Follow the same steps as you did for the "internal" tag.

![](https://d3q7ie80jbiqey.cloudfront.net/media/image/zoom/ca600fb5-e338-48a4-ab61-9a12292442d9/2.5/84.548611111111/24.835526315789?0)

Gravitee also provides a way to automatically apply a sharding tag to APIs based on the entrypoint. This instructs Gravitee API Manager to apply the “external” tag to all APIs with this entrypoint so the APIs will be deployed on your chosen Gateway. To do so, follow these steps:

1. &#x20;Select **+ Add a mapping**.

![](https://d3q7ie80jbiqey.cloudfront.net/media/image/zoom/8c0374a0-999f-43f2-bccb-61c507a001c8/1.5/84.548611111111/49.819401444788?0)

2. &#x20;In the **Entrypoint url** field, enter your Entrypoint URL.

![](https://d3q7ie80jbiqey.cloudfront.net/media/image/zoom/397a968c-5ae8-4d85-9b4c-5f534a0d9132/2/50/49.980650154799?0)

3. In the **Sharding tags** drop down menu, select the tag that you want mapped to your entrypoints. For this example, let's choose the "internal test" tag.

![](https://d3q7ie80jbiqey.cloudfront.net/media/image/zoom/505ea3bc-5fb0-4bbe-8d8b-229e67f1f7c7/1/50/50?0)

4. Click **Ok**.

![](https://d3q7ie80jbiqey.cloudfront.net/media/image/zoom/23db58e8-6576-49aa-a51f-9fdcd37073cb/1.5/60.272442853009/69.892447110423?0)

You'll see your entrypoint mapping in the **Entrypoint mappings** section.

<figure><img src="../../.gitbook/assets/image (2) (1) (1).png" alt=""><figcaption></figcaption></figure>

{% hint style="success" %}
You've now learned how to configure sharding tags for your Gravitee API Gateways. To apply sharding tags to APIs in order to control where those APIs are deployed, refer to [this documentation](../../guides/api-configuration/v2-api-configuration/configure-cors.md#configure-deployments).
{% endhint %}
