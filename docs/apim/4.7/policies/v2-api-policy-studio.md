# v2 API Policy Studio

{% hint style="warning" %}
**Legacy version**

The v2 Policy Studio can only be used to design flows for APIs using the v2 API definition and does not support applying policies at the message level or for pub/sub use cases. Instead, please refer to the [v4 Policy Studio](v4-api-policy-studio.md) documentation.
{% endhint %}

## Overview

The v2 Policy Studio consists of the following sections:

* [**Design**](v2-api-policy-studio.md#design)**:** Manage all flows associated with your Gateway API
* [**Configuration**](v2-api-policy-studio.md#configure-flow-mode)**:** Modify settings related to flow execution
* [**Debug**](v2-api-policy-studio.md#debug-mode)**:** Test and troubleshoot your Gateway APIs

## Design

Flows are created when policies are added to the request and/or response phases and targeted by path, HTTP method(s), or via [Gravitee's Expression Language](../getting-started/gravitee-expression-language.md). A single API supports multiple flows, which can be set to target subscribers of an individual plan or all users of the API.

To create a flow and add policies:

1. Log in to your APIM Console
2. Selecting **APIs** from the left nav
3. Select the API for which to design a flow
4. Select **Policy Studio** from the inner left nav
5. Select the **Design** tab
6.  In the **Flows** section, select the **+** icon, then configure the flow:

    <figure><img src="../../../../.gitbook/assets/v2 design (1).png" alt=""><figcaption><p>Configure a flow</p></figcaption></figure>

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

    <figure><img src="../../../../.gitbook/assets/v2 PS configuration (1).png" alt=""><figcaption><p>Configure Flow Mode</p></figcaption></figure>

## Debug mode

{% hint style="warning" %}
Debug mode is an [Enterprise Edition](../overview/enterprise-edition.md) capability
{% endhint %}

{% hint style="info" %}
**Debug mode limitations**

* Cannot be used with v4 APIs.
* Does not support testing the following policies and features:
  * **Rate Limit policies**
  * **Cache policy:** Not testable with in-memory cache since cache is created and destroyed with the API
  * **IP Filtering policy:** Calls are emitted by the Gateway and cannot be emulated from another IP (IP used to issue requests is 127.0.0.1)
  * **Health-check**
  * **Virtual hosts:** The first host is always selected
  * **Encrypted properties:** For security, you cannot clear encrypted properties (e.g., this could impact use in a condition)
{% endhint %}

Debug mode is a troubleshooting tool that enables insights into policy order of execution and triggering by specific requests (including platform-level policies), visualization of conditional policy behavior, tracing of transformations and changes made to headers / body / execution context, and root-causing of errors and performance issues.

To debug your flows:

1. Log in to your APIM Console
2. Selecting **APIs** from the left nav
3. Select the API for which to design a flow
4. Select **Policy Studio** from the inner left nav
5.  Select the **Debug** tab

    <div align="left"><figure><img src="../../../../.gitbook/assets/v2 debug (1).png" alt="" width="375"><figcaption><p>Configure Debug</p></figcaption></figure></div>
6. Define the HTTP method, path, headers, and request bodies for the debug request
7.  Select **Send** to prompt Gravitee to initiate a test request and present you with a timeline showing the order of your flows and policies

    <figure><img src="../../../../.gitbook/assets/Debug mode timeline (1).png" alt=""><figcaption><p>Debug mode timeline</p></figcaption></figure>

<details>

<summary>Policy indicators</summary>

The status of a policy is represented by one of the following indicators:

* **Executed**: The policy has been executed properly
* **Skipped:** The policy contains a condition that has not been fulfilled. Refer to the input/output inspector for more details on the evaluation of the condition.
* **Error:** An error occurred during policy execution. Refer to the input/output inspector for more details on the error.

Select a specific policy in the timeline to access additional information regarding the input/output of the policy header, context attributes, and body.

The inspector relies on 3 colors to indicate the nature of changes:

* **Green:** Indicates an addition
* **Orange:** Indicates an edit
* **Red:** Indicates a deletion

</details>

<details>

<summary>Debug mode timeline</summary>

The order in which the policies appear in the timeline reflects the exact order in which they were executed by the Gateway at runtime. This order may differ from the order in which policies were placed during the design phase due to a performance optimization applied on the policy chain at runtime.

The Gateway executes policies interacting with the HTTP header part of the request (onRequest, onResponse) before policies interacting with the body part of the request (onRequestContent, onResponseContent). A policy may appear twice in the timeline if it interacts with both the header and body of the request.

To navigate the timeline:

* Scroll through the list of policies via the timeline or jump to a specific policy by selecting it in the **quick access** timeline
* Select **Request Input** or **Request Output** to view the global transformation on the request and the difference between what has been received by the Gateway and what has been sent to the backend
* Select **Response Input** or **Response Output** to view the global transformation on the response and the difference between what has been received from the backend and what has been sent back to the client app

</details>
