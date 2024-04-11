---
description: >-
  This article describes how to design and enforce policy flows using the legacy
  v2 Policy Studio
---

# v2 API Policy Studio

{% hint style="warning" %}
**Legacy version**

The v2 Policy Studio can only be used to design flows for APIs using the v2 API definition and does not support applying policies at the message level or for pub/sub use cases. Instead, please refer to the [v4 Policy Studio](v4-api-policy-studio.md) documentation.
{% endhint %}

## Introduction

The v2 Policy Studio consists of the following sections:

* [**Design**](v2-api-policy-studio.md#design)**:** Manage all flows associated with your Gateway API
* [**Configuration**](v2-api-policy-studio.md#configure-flow-mode)**:** Modify settings related to flow execution
* [**Properties**](v2-api-policy-studio.md#api-properties)**:** Define key-value pairs at the API level
* [**Resources**](v2-api-policy-studio.md#resources)**:** Configure global resources to support your flows
* [**Debug**](v2-api-policy-studio.md#debug-mode)**:** Test and troubleshoot your Gateway APIs

## Design

Flows are created when policies are added to the request and/or response phases and targeted by path, HTTP method(s), or via [Gravitee's Expression Language](../gravitee-expression-language.md). A single API supports multiple flows, which can be set to target subscribers of an individual plan or all users of the API.&#x20;

To create a flow and add policies:

1. Log in to your APIM Console
2. Selecting **APIs** from the left nav
3. Select the API for which to design a flow
4. Select **Design** from the inner left nav
5.  In the **Flows** section, select the **+** icon, then configure the flow using the **Flow Configuration** module:&#x20;

    <figure><img src="../../.gitbook/assets/v2_flow_config (1).png" alt=""><figcaption><p>Sample flow configuration</p></figcaption></figure>

    * **Name:** Give your flow a descriptive name. Otherwise, a name will be automatically generated using the path and methods.
    * **Operator path:** For the provided **Path**, apply this flow to requests with a path that **Equals** or **Starts with** the same path.
    * **Path:** Define the path to use in conjunction with the **Operator path** to determine if this flow should be applied.
    * **Methods:** Define the HTTP methods for which you want the flow to be executed. If you leave this empty, the flow will be executed for every HTTP method, assuming the other conditions are met.
    * **Conditions:** Define specific conditions that will trigger flow execution using Gravitee's Expression Language (EL).
6. To add a policy to the flow, drag-and-drop the policy that you want to enforce onto either the request or response phase
7. To configure the policy, select it and use the menu beneath the flow map
8.  Select the **checkmark icon**, then click **Save** in the pop-up window&#x20;

    <figure><img src="../../.gitbook/assets/v2_policy_config (1).png" alt=""><figcaption><p>Configure a policy</p></figcaption></figure>
9. Redeploy your API to the Gateway for the changes to take effect

{% hint style="info" %}
* A policy added to the request phase will be enforced by the Gateway at the time of the request, before a client is given access to the API.&#x20;
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

Gravitee offers two flow modes: **DEFAULT** and **BEST\_MATCH**:

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
4. Select **Design** from the inner left nav
5. Select the **Configuration** tab&#x20;
6.  Change the **Flow Mode** to either **DEFAULT** or **BEST\_MATCH** using the drop-down menu&#x20;

    <figure><img src="../../.gitbook/assets/Configure flow mode (2).png" alt=""><figcaption><p>v2 Policy Studio: Configure flow mode</p></figcaption></figure>

## API properties

Properties are read-only during the Gateway's execution of an API transaction. They can be accessed from within flows using Gravitee's Expression Language (EL) and the `#properties` statement. To configure properties:

1. Log in to your APIM Console
2. Selecting **APIs** from the left nav
3. Select the API for which to design a flow
4. Select **Design** from the inner left nav
5. Select the **Properties** tab
6.  Specify properties one by one, or toggle from **Simple** to **Expert** mode and paste property definitions into the editor using `<key>=<value>` format&#x20;

    <figure><img src="../../.gitbook/assets/v2 properties.png" alt=""><figcaption><p>API properties: Expert format</p></figcaption></figure>

### Encryption

{% hint style="warning" %}
Encrypted values can be used by API policies and APIM Gateway will automatically decrypt these values. Use caution handling encrypted data in policies.
{% endhint %}

To encrypt an API property:

1.  Reset the default secret key in `gravitee.yml`. The secret must be 32 bytes in length.&#x20;

    ```yaml
    # Encrypt API properties using this secret:
    api:
      properties:
        encryption:
             secret: vvLJ4Q8Khvv9tm2tIPdkGEdmgKUruAL6
     to provide the best security available.
    ```
2.  Enable the **Encrypted** toggle next to the property. Once you click **Save**, you can no longer edit, modify, or view the value.&#x20;

    <figure><img src="../../.gitbook/assets/v2 encrypted property.png" alt=""><figcaption><p>Encrypted API property</p></figcaption></figure>

### **Dynamic properties**

To configure dynamic properties:

1.  Under the **Properties** tab, select **CONFIGURE DYNAMIC PROPERTIES**&#x20;

    <figure><img src="../../.gitbook/assets/v2 dynamic properties.png" alt=""><figcaption><p>Configure dynamic properties</p></figcaption></figure>
2. Specify the details of the property:
   * `cron` schedule
   * HTTP method(s)
   * URL
   * Request headers and body to include with the call
   * JOLT transformation to perform on the response
3. Toggle **Enabled** ON
4. Select the tick icon ![tick icon](https://docs.gravitee.io/images/icons/tick-icon.png) to save your changes
5. Select **SAVE**

After the first call, the resulting property is added to the list of global properties, where its value is continuously updated according to the `cron` schedule specified.

{% hint style="info" %}
Key-value pairs can also be maintained using a dictionary, e.g., if this information is stored independently of the API creation process or applies to multiple APIs.&#x20;
{% endhint %}

<details>

<summary>Example</summary>

Configure the Gateway API to query the stock levels of shop databases, then dynamically reroute any API call containing a shop ID to its associated URL:

1.  Define a list of properties for the shops, where `<key>` is the unique shop ID and `<value>` is the shop URL&#x20;

    <figure><img src="../../.gitbook/assets/v2 dynamic properties example 1.png" alt=""><figcaption><p>Add API properties</p></figcaption></figure>
2.  Configure a dynamic routing policy that builds new URLs dynamically through property matching via the `#properties` statement:&#x20;

    <figure><img src="../../.gitbook/assets/dynamic-routing-properties.png" alt=""><figcaption><p>Add a dynamic routing policy based on an API property</p></figcaption></figure>

    If the ID in the request header matches the key of one of the properties, it is replaced with the URL. The dynamic routing policy then reroutes the API call to the URL.

</details>

## Resources

Some policies support the addition of resources, which can be used for actions such as authentication and schema registry validation. After you create resources, you will be able to reference them when designing policies. Policies that support resources include:

<table data-header-hidden><thead><tr><th width="242"></th><th></th></tr></thead><tbody><tr><td><a href="../../reference/policy-reference/basic-authentication.md">Basic Authentication</a></td><td>Specify an LDAP Authentication Provider resource and/or an Inline Authentication Provider resource to authenticate users in memory</td></tr><tr><td><a href="../../reference/policy-reference/cache.md">Cache</a></td><td>Specify a cache resource via the Cache or Cache Redis resources</td></tr><tr><td><a href="../../reference/policy-reference/http-signature.md">HTTP Signature</a><br><a href="../../reference/policy-reference/generate-http-signature.md">Generate HTTP Signature</a></td><td>Specify your HTTP Authentication Provider resource</td></tr><tr><td><a href="../../reference/policy-reference/oauth2/">OAuth2</a></td><td>Specify a Generic OAuth2 Authorization Server resource or a Gravitee AM Authorization Server resource</td></tr><tr><td><a href="../../reference/policy-reference/openid-connect-userinfo.md">OpenID Connect Userinfo</a></td><td>Specify a Keycloak Adapter resource to use Keycloack as your OpenID Connect resource</td></tr><tr><td><a href="../../reference/policy-reference/avro-to-json.md">AVRO to JSON</a><br><a href="../../reference/policy-reference/avro-to-protobuf.md">AVRO to Protobuf</a><br><a href="../../reference/policy-reference/protobuf-to-json.md">Protobuf to JSON</a></td><td>Specify your Confluent Schema Registry to retrieve serialization and deserialization schemas from a Confluent Schema registry</td></tr></tbody></table>

<figure><img src="../../.gitbook/assets/Confluent schema registry.png" alt=""><figcaption><p>Resources: Confluent Schema Registry</p></figcaption></figure>

{% hint style="info" %}
Global resources are available to all flows associated with the Gateway API, but are not available to other Gateway APIs.
{% endhint %}

## Debug mode

{% hint style="warning" %}
Debug mode is an [Enterprise Edition](../../overview/gravitee-apim-enterprise-edition/) capability
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

Debug mode is a tool for troubleshooting your Gateway APIs running on Gravitee API Management. It provides detailed information about the behavior of each policy in your flows, as well as the overall execution order at runtime. With Debug mode, you can:

* Understand which policies are triggered by a specific request (including platform-level policies)
* Visualize which policies are executed or skipped (conditional policy)
* Understand the order of execution of your policies
* Trace transformations and changes made to headers, body, and execution context
* Easily troubleshoot and root-cause errors, misbehaviors, or performance issues

To debug your flows:

1. Select the **Debug** tab
2. Define the HTTP method, path, headers, and request bodies for the debug request
3. Select **Send**

Gravitee will initiate a test request, and then you will be presented with a timeline that shows the order of your flows and policies.

<figure><img src="../../.gitbook/assets/Debug mode timeline.png" alt=""><figcaption><p>Debug mode timeline</p></figcaption></figure>

### Understanding different indicators for policies

Gravitee Debug mode uses different indicators to indicate the status of policies:

* **Executed**: The policy has been executed properly
* **Skipped:** The policy contains a condition that has not been fulfilled. Refer to the input/output inspector for more details on the evaluation of the condition.
* **Error:** An error occurred during policy execution. Refer to the input/output inspector for more details on the error.

Select a specific policy in the timeline to access additional information regarding the input/output of the policy:

* Header
* Context attributes
* Body

The inspector relies on 3 colors to indicate the nature of changes:

* **Green:** Indicates an addition
* **Orange:** Indicates an edit
* **Red:** Indicates a deletion

### Understanding the timeline

The order in which the policies appear in the timeline reflects the exact order in which they have been executed by the Gateway at runtime.

Note that this order may differ from the order in which policies were placed in the Policy Studio during the design phase due to a performance optimization applied at runtime on the policy chain.

The Gateway always executes policies interacting with the HTTP header part of the request (onRequest, onResponse) before policies interacting with the body part of the request (onRequestContent, onResponseContent). A policy may appear twice in the timeline if it interacts with both the header and body of the request.

<figure><img src="https://docs.gravitee.io/images/apim/3.x/api-publisher-guide/design-studio/debug-mode/debug-mode-policy-chain.png" alt=""><figcaption></figcaption></figure>

### **Navigating the timeline**

You can scroll through the list of policies via the timeline. You can also quickly access a specific policy by selecting it in the **quick access** timeline.

<figure><img src="https://docs.gravitee.io/images/apim/3.x/api-publisher-guide/design-studio/debug-mode/debug-mode-timeline.png" alt=""><figcaption><p>Navigating debug timeline</p></figcaption></figure>

Select **Request Input** or **Request Output** to view the global transformation on the request and the difference between what has been received by the Gateway and what has been sent to the backend.

Select **Response Input** or **Response Output** to view the global transformation on the response and the difference between what has been received from the backend and what has been sent back to the client app.
