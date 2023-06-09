---
description: >-
  This article walks through how to design and enforce policy flows using the
  legacy v2 Policy Design Studio.
---

# v2 API Policy Design Studio

{% @arcade/embed flowId="w2EIKB74a9xXG3sXcQVI" url="https://app.arcade.software/share/w2EIKB74a9xXG3sXcQVI" fullWidth="true" %}

## Introduction

The Gravitee Policy Design Studio allows you to design "flows," or policy enforcement sequences that protect, transform, or otherwise alter how APIs are consumed. Gravitee comes with many different baked in policies, some that come with the community version and some that are only available in Gravitee Enterprise. For more information on specific policies, please refer to the [Policy Reference documentation](policy-reference.md).&#x20;

The rest of this article provides a walk through of the v2 API Policy Design studio.&#x20;

{% hint style="info" %}
Legacy version

The v2 Policy Design Studio can only be used to design flows for APIs using the v2 API definition. The v2 Policy Design studio does not support applying policies at the message level or for pub/sub use cases. If you want to design and enforce policy flows at the message level or for pub/sub use cases, please refer to the [v4 Policy Design studio documentation.](v4-api-policy-design-studio.md)
{% endhint %}

## Design a flow with the Policy Design Studio

Flows can only be designed for already v2 APIs. So, head to the API list by selecting **APIs** in the left-hand nav. Then, select the API for which you want to design a flow.

You'll be taken to the API's **General** details page. Select Design in the left-hand nav.

You're now in the Design section of the Policy Design Studio. Here, you can create flows, search for policies, filter policies, and then build flows by adding policies on to the request and/or response phases. You can create multiple flows, each with different policies. You can also associate flows and policies with specific plans.

### Create a flow, and add policies

First, let's create a flow. To do so, find the **Flows** section, and select the **+** icon. This will create your flow. Before adding policies to your flow, you'll need to configure the flow using the **Flow Configuration** module. You can:

* Give your flow a descriptive name. If you don't, a name will be automatically generated using the path and methods.
* Define the Operator Path and the Path.&#x20;
* Define the HTTP methods at/during which you want the flow to be executed. If you leave this empty, the flow will be executed with every HTTP method.
* Define conditions: this enables you to define specific conditions that will trigger flow execution. You will need to use the Gravitee Expression Language here. More information can be found in the [Gravitee Expression language documentation](gravitee-expression-language.md).&#x20;

Now, it's time to add policies to that flow.

To add a policy, find the policy that you want to enforce, and then drag and drop that policy onto either the request or response phase. If you add a policy at the Request phase, the policy will be enforced by the Gateway at the time of the request, before a client is given access to the API that they are trying to call. If you add a policy on the response phase, the Gateway will enforce the policy after the request is allowed, but as/before the response is allowed, depending on the policy enforced.

Once you've added your policy, you can edit that policy by selecting the policy, and using the configuration menu below the flow map. After you configure the policy, select the checkmark icon, and then Save in the pop-up to save the policy settings.

Anytime after you finish configuring a policy, or editing a flow, you'll need to redeploy your API to the Gateway for the changes to take effect. You'll see a bar appear at the top of the flow designer, that says **API out of sync, deploy your API.** Select the hyperlinked deploy your API text, and you'll be met with a pop-up that asks you to provide a label to define and describe your deployment. when you are done, select OK to deploy/redeploy your API with the new flow and policy.

#### Example: add a Rate limit policy

For example, if I wanted to limit the number of requests that a client could make using the HTTP GET method to five GET requests per second, I would:

1. Create a new flow using the steps above
2. Configure the flow to execute only at the HTTP GET method
3. Find the Rate Limit policy in the policy menu
4. Drag n' drop the Rate Limit policy onto the Request phase
5. Give my Rate Limit a description
6. Add any conditions using the Gravitee EL
7. Enable or disable non-strict mode
8. Enable or disable Rate-Limit response headers in the HTTP response
9. Define a Key that will be used to identify consumers against whom the rate limit policy should be enforced. Otherwise, you can leave this blank, and the rate limit will be applied to any consumer that has subscribed to that API's plan.
10. Set the Max requests (static) as 5
11. Set the time duration as 1
12. Set the time unit as SECONDS
13. Select the checkmark icon to save my rate limit settings.
14. Select Save.
15. Select **deploy your API**
16. In the pop-up, give the deployment a label
17. Select **OK**

At this point, the Rate Limit policy has been applied at five requests per second on the HTTP GET request.

## Configure flow mode

Gravitee offers two flow modes: **default** and **best match**. If you keep the flow mode as default, your flow will be selected and executed based on the operator defined in the flow itself (see documentation above). If you choose best match, Gravitee will choose the flow that is associated to the closest matching path.

When using **best match** mode, a best match flow is chosen if the request matches the flow. A plain text part of the path will take precedence over a path parameter.

This means, reading from left to right, each part of the path is compared, keeping the better matching. Strict equality between part of the request path and the flow path prevails over a path parameter.

For example, with these flows configured:

* `/test/:id`
* `/test/subtest`

If the request is `/test/55`, the resulting flow will be `/test/:id`. If the request is `/test/subtest`, the resulting flow will be `/test/subtest`.

To make this change, select the **Configuration** tab, and change the **Flow Mode** to either **DEFAULT** or **BEST\_MATCH** using the **Flow Mode** drop-down.&#x20;

<figure><img src="../../.gitbook/assets/Configure flow mode.png" alt=""><figcaption><p>v2 Policy Design studio: Configure flow mode</p></figcaption></figure>

## Define API properties for your API flows

If you want to retrieve and query property values with certain API calls as a part of your flow, you can configure that in the **Properties** tab. Here, you can specify properties as key-value pairs. You can specify them one by one, or toggle from **Simple** to **Expert** mode and paste property definitions into an editor in format `<key>=<value>`.

You can also configure dynamic properties by clicking **CONFIGURE DYNAMIC PROPERTIES**. Dynamic properties are fetched with a URL on a regular schedule and subsequently updated according to the details you specify.

<figure><img src="../../.gitbook/assets/API properties.png" alt=""><figcaption><p>v2 Policy Design studio: API properties</p></figcaption></figure>

When you add new policies to your API flows which include [Expression Language](https://docs.gravitee.io/apim/3.x/apim\_publisherguide\_expression\_language.html#api) fields as part of their configuration (such as the dynamic routing policy), you can retrieve and query property values with the `#properties` statement. For more details, see the [Example](https://docs.gravitee.io/apim/3.x/apim\_publisherguide\_design\_studio\_create.html#example) below.

### **Example: Dynamic properties**

For example, let's configure dynamic properties that will retrieve properties from a remote server with a URL and update them according to the details you specify. To do so, follow these steps:

1. In the **Properties** tab, select **CONFIGURE DYNAMIC PROPERTIES**.
2. Specify the details of the property:
   * `cron` schedule
   * URL
   * request headers and body to include with the call
   * JOLT transformation to perform on the response
3. Toggle **Enabled** ON.
4. Select the tick icon ![tick icon](https://docs.gravitee.io/images/icons/tick-icon.png) to save your changes.
5. Select **SAVE**.

After the first call, the resulting property is added to the list of global properties, where its value is continuously updated according to the `cron` schedule specified.\


