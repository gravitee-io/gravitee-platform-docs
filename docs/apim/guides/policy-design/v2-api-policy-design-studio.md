---
description: >-
  This article walks through how to design and enforce policy flows using the
  legacy v2 Policy Design Studio.
---

# v2 API Policy Design Studio

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

