---
description: An overview about v2 api policy studio.
metaLinks:
  alternates:
    - >-
      https://app.gitbook.com/s/bGmDEarvnV52XdcOiV8o/create-and-configure-apis/apply-policies/v2-api-policy-studio
---

# v2 API Policy Studio

{% hint style="warning" %}
**Legacy version**

The v2 Policy Studio can only be used to design flows for APIs using the v2 API definition and does not support applying policies at the message level or for pub/sub use cases. Instead, please refer to the [v4 Policy Studio](v4-api-policy-studio.md) documentation.
{% endhint %}

## Overview

The v2 Policy Studio consists of the following sections:

* [**Design**](v2-api-policy-studio.md#design)**:** Manage all flows associated with your Gateway API
* [**Configuration**](v2-api-policy-studio.md#configure-flow-mode)**:** Modify settings related to flow execution
* [**Debug**](debug-mode.md#debug-mode)**:** Test and troubleshoot your Gateway APIs

## Design

Flows are created when policies are added to the request and/or response phases and targeted by path, HTTP method(s), or via [Gravitee's Expression Language](../../gravitee-expression-language.md). A single API supports multiple flows, which can be set to target subscribers of an individual plan or all users of the API.

To create a flow and add policies:

1. Log in to your APIM Console
2. Selecting **APIs** from the left nav
3. Select the API for which to design a flow
4. Select **Policy Studio** from the inner left nav
5. Select the **Design** tab
6.  In the **Flows** section, select the **+** icon, then configure the flow:

    <figure><img src="../../.gitbook/assets/v2 design (1).png" alt=""><figcaption><p>Configure a flow</p></figcaption></figure>

    * **Name:** Give your flow a descriptive name. Otherwise, a name will be automatically generated using the path and methods.
    * **Operator path:** For the provided **Path**, apply this flow to requests with a path that **Equals** or **Starts with** the same path.
    * **Path:** Define the path to use in conjunction with the **Operator path** to determine if this flow should be applied.
    * **Methods:** Define the HTTP methods for which you want the flow to be executed. If you leave this empty, the flow will be executed for every HTTP method, assuming the other conditions are met.
    * **Conditions:** Define specific conditions that will trigger flow execution using Gravitee's Expression Language (EL).
7. To add a policy to the flow, drag-and-drop the policy that you want to enforce onto either the request or response phase
8. To configure the policy, select it and use the menu beneath the flow map
9. Select the **checkmark icon**, then click **Save** in the pop-up window
10. Redeploy your API to the Gateway for the changes to take effect

{% hint style="info" %}
* A policy added to the request phase will be enforced by the Gateway at the time of the request, before a client is given access to the API.
* If a policy is added to the response phase, the Gateway will enforce the policy after the request is allowed, but before the response is returned to the client.
{% endhint %}

<details>

<summary>Example: Add a Rate Limit policy</summary>

Limit the number of requests that a client can make using the HTTP GET method to five per second:

1. Create a new flow via the steps above
2. Configure the flow to execute only on the HTTP GET method
3. From the policy menu, drag-and-drop the Rate Limit policy onto the request phase
4. Give the rate limit a description
5. Add conditions using the Gravitee EL
6. Enable or disable non-strict mode and rate limit response headers in the HTTP response
7. Define a Key that will be used to identify consumers against whom the Rate Limit policy should be enforced. If this is left blank, the rate limit will be applied to any consumer that has subscribed to the API's plan.
8. Set the max requests (static) to 5, the time duration to 1, and the time unit to SECONDS
9. Select the checkmark icon and click **Save**
10. Redeploy your API

</details>

## Configure flow mode

Gravitee offers two flow modes: **DEFAULT** and **BEST\_MATCH**.

{% tabs %}
{% tab title="DEFAULT" %}
Allows for the execution of multiple flows, where each is determined independently based on the **Operator path** defined in the flow
{% endtab %}

{% tab title="BEST_MATCH" %}
The Gateway chooses a single flow with the closest match to the path of the API request. From left to right, each part of the path is compared, where strict equality between parts of the request and flow paths takes precedence over a path parameter.
{% endtab %}
{% endtabs %}

<details>

<summary>Example of best match</summary>

Consider the flows `/test/:id` and `/test/subtest`:

* If the request is `/test/55`, the resulting flow will be `/test/:id`
* If the request is `/test/subtest`, the resulting flow will be `/test/subtest`

</details>

To modify the flow mode:

1. Log in to your APIM Console
2. Selecting **APIs** from the left nav
3. Select the API for which to design a flow
4. Select **Policy Studio** from the inner left nav
5. Select the **Configuration** tab
6.  Change the **Flow Mode** to either **DEFAULT** or **BEST\_MATCH** using the drop-down menu

    <figure><img src="../../.gitbook/assets/v2 PS configuration (1).png" alt=""><figcaption><p>Configure Flow Mode</p></figcaption></figure>
