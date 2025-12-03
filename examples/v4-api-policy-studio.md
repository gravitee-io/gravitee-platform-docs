---
description: An overview about v4 api policy studio.
metaLinks:
  alternates:
    - >-
      https://app.gitbook.com/s/bGmDEarvnV52XdcOiV8o/create-and-configure-apis/apply-policies/v4-api-policy-studio
---

# v4 API Policy Studio

{% hint style="info" %}
**Product limitations**

The v4 Policy Studio can only be used to design flows for APIs using the v4 API definition. It supports applying policies at the message level or for pub/sub use cases. The v4 Policy Studio does not currently support Gravitee Debug mode.
{% endhint %}

## Overview

Gravitee defines a flow as the method to control where, and under what conditions, policies act on an API transaction. The v4 Policy Studio lets you perform the following actions:

* Create and manage all flows associated with your Gateway API
* Modify settings related to flow execution
* Define key-value pairs at the API level
* Configure global resources to support your flows

Flows are created when policies are added to the Request, Response, Publish, and/or Subscribe phases of an existing v4 API. A single API supports multiple flows, which can be applied to different phases and target either subscribers of an individual plan or all users of the API.

Policies are added to flows to enforce security, reliability, and proper data transfer. Examples of policies include traffic shaping, authentication/authorization, rate limiting, and dynamic routing.

<details>

<summary>Phases</summary>

The entrypoint(s) of a flow determine its phases. The phase a policy is added to dictates when the policy is applied and how the Gateway enforces it.

**Phases**

* **Request:** A policy is applied when the connection is established. It is enforced at the time of the request and before a client is given access to the API.
* **Response:** A policy is applied to the response from the initial connection. It is enforced after the request is allowed, but before the response is returned to the client.
* **Publish:** A policy is applied to messages sent to the endpoint. It is enforced when messages are published and before a client is given access to the API.
* **Subscribe:** A policy is applied to messages received by the entrypoint. It is enforced after messages are subscribed to, but before the response is returned to the client.

</details>

## Example: Create a flow and add a policy

The following example uses a v4 HTTP proxy API to demonstrate how to create a flow and add a policy.

{% hint style="info" %}
The flow and policy configuration options you are presented with differ based on API type and entrypoint/endpoint selections.
{% endhint %}

1. Log in to your APIM Console
2. Select **APIs** from the navigation
3. Select the API for which to design a flow
4. Select **Policies** from the inner menu
5.  To create a flow, you have the following to options:

    * To create a flow for a single existing plan, click the + icon next to that plan.
    * To create a flow that applies to all plans, click the + icon next to **All plans**.

    <figure><img src=".gitbook/assets/0 ps1 (1).png" alt=""><figcaption></figcaption></figure>
6.  Configure the flow using the **Create a new flow** module with the options shown below

    <div align="left"><figure><img src=".gitbook/assets/0 ps2 (1).png" alt="" width="375"><figcaption></figcaption></figure></div>

    * **Flow name:** Give your flow a descriptive name. Otherwise, a name will be automatically generated using the channel and operation.
    * **Path operator:** Apply this flow to requests with a path that **Equals** or **Starts with** the specified **Path**.
    * **Path:** Define the path to use in conjunction with the **Path operator** to determine if this flow should be applied.
    * Choose one or more of the following **Methods for your flow**: ALL, CONNECT, DELETE, GET, HEAD, OPTIONS, PATCH, POST, PUT, TRACE, OTHER.
    * **Condition:** Use [Gravitee's Expression Language (EL)](gravitee-expression-language.md) to define specific conditions that trigger flow execution.
7. Click **Create** in the modal, and then **Save** on the **Policies** page.
8.  To add a policy to your flow, click the **+** icon for the phase where the policy should be enforced.

    <figure><img src=".gitbook/assets/0 ps3 (1).png" alt=""><figcaption></figcaption></figure>
9. Select from the pre-populated policies that are valid for your specific entrypoints and endpoints.
10. In the policy configuration modal, enter the information appropriate to and required by the policy.
11. Click **Add policy**. The policy appears in the phase it was added to. For example, the following screenshot shows the API Key policy added to the Request phase of a v4 HTTP proxy API.

    <figure><img src=".gitbook/assets/0 ps4 (1).png" alt=""><figcaption></figcaption></figure>
12. Click **Save** on the **Policies** page, then redeploy your API to the Gateway for the changes to take effect.

{% hint style="info" %}
To edit a policy, click on the three vertical dots on its icon in the flow diagram.
{% endhint %}

### Policy Studio navigation tips

The Policy Studio is designed to help you easily distinguish between plans and flows. You can use the search field in the **Flows** panel to surface plans or flows that have names or paths that meet your search criteria. You can also search for a policy based on its name or description.

#### Plans vs flows

Individual plans are identified by the **Plan:** prefix, as shown in the following example. Each plan can contain one or more flows, where each flow appears as a box under the plan name. You have the option to name your flows and/or their respective paths. Flow names appear above path names, which are prefixed with "/".

<figure><img src=".gitbook/assets/0 ps9 (1) (1).png" alt=""><figcaption></figcaption></figure>

#### Find plans and flows

The single search box in the **Flows** panel can be used to find all plans and flows that meet your search criteria. A search query displays the following results:

*   **All of the flows of every plan whose name matches the search text.** In the following example, the search text "JWT" surfaces all of the flows that belong to the plan named **JWT**.

    <figure><img src=".gitbook/assets/00 ps2 (1).png" alt=""><figcaption></figcaption></figure>
*   **All of the flows with a path that matches the search text.** In the following example, the search text "foo" surfaces every flow whose path name includes **foo**.

    <figure><img src=".gitbook/assets/00 ps1 (1).png" alt=""><figcaption></figcaption></figure>
*   **All of the flows with names that match the search text.** In the following example, the search text "flow" surfaces a flow called **Named flow**.

    <div align="left"><figure><img src=".gitbook/assets/00 ps3 (1).png" alt="" width="375"><figcaption></figcaption></figure></div>

#### Find a policy

When you click a phase's **+** icon to add a policy to your flow, you can use the search field in the policy selection pop-up to find a policy. The search results surface all policies that include your search text in the policy name or description.

<figure><img src=".gitbook/assets/00 ps4 (1).png" alt=""><figcaption></figcaption></figure>

## Configure flow mode

To configure the flow mode, click the gear icon in the **Flows** panel to open the **Flow execution** module:

<div align="left"><figure><img src=".gitbook/assets/0 ps5 (1).png" alt="" width="375"><figcaption></figcaption></figure></div>

* **Default flow mode:** Use the drop-down menu to select **Default** or **Best Match**
* Enable **Fail on flow mismatch** to generate an error when there is no match between the request and any defined flow

## API properties

Properties are read only during the Gateway's execution of an API transaction. They can be accessed from within flows using Gravitee's Expression Language (EL) and the `#api.properties` statement.

### Add static properties

To configure API properties:

1. Log in to your APIM Console
2. Selecting **APIs** from the left nav
3. Select the API for which to design a flow
4. Select **Configuration** from the inner left nav
5.  Select the **Properties** tab

    <figure><img src=".gitbook/assets/0 ps6 (1).png" alt=""><figcaption></figcaption></figure>
6. To add static properties, either:
   * Click **Add property** and enter property definitions one at a time as a key-value pair
   * Click **Import** and enter property definitions as a list in `<key>=<value>` format

#### Encryption

{% hint style="warning" %}
Encrypted values can be used by API policies, but encrypted data should be used with care. APIM Gateway will automatically decrypt these values.
{% endhint %}

To encrypt a static API property value:

1.  Reset the default secret key in `gravitee.yml`. The secret must be 32 bytes in length.

    ```yaml
    # Encrypt API properties using this secret:
    api:
      properties:
        encryption:
             secret: vvLJ4Q8Khvv9tm2tIPdkGEdmgKUruAL6
     to provide the best security available.
    ```
2.  Enable the **Encrypt** toggle when adding a property via **Add property**. Once you click **Save**, you can no longer edit, modify, or view the value.

    <div align="left"><figure><img src=".gitbook/assets/0 ps7 (1).png" alt="" width="375"><figcaption></figcaption></figure></div>

### **Dynamic properties**

To configure dynamic properties:

1. Log in to your APIM Console
2. Selecting **APIs** from the left nav
3. Select the API for which to design a flow
4. Select **Configuration** from the inner left nav
5. Select the **Properties** tab
6.  Click the **Manage dynamically** button and define the configuration

    <figure><img src=".gitbook/assets/0 ps8 (1).png" alt=""><figcaption></figcaption></figure>

    * Toggle **Enabled** to ON
    * **Schedule:** A cron expression to schedule the health check
    * **HTTP Method:** The HTTP method that invokes the endpoint
    * **URL:** The target from which to fetch dynamic properties
    * **Request Headers:** The HTTP headers to add to the request fetching properties
    * **Request body:** The HTTP body content to add to the request fetching properties
    * (Optional) **Transformation (JOLT specification):** If the HTTP service doesn’t return the expected output, edit the JOLT transformation accordingly
    * Toggle **Use system proxy** ON to use the system proxy configured in your APIM installation
7. Click **Save**

After the first call, the resultant property is added to the list of global properties, where its value is continuously updated according to the `cron` schedule specified.

{% hint style="info" %}
Key-value pairs can also be maintained using a dictionary, e.g., if this information is stored independently of the API creation process or applies to multiple APIs.
{% endhint %}

## Resources

Some policies support the addition of [resources](resources.md), which can be used for actions such as authentication and schema registry validation. After you create resources, you will be able to reference them when designing policies. Policies that support resources include:

<table data-header-hidden><thead><tr><th width="242"></th><th></th></tr></thead><tbody><tr><td>Basic Authentication</td><td>Specify an LDAP Authentication Provider resource and/or an Inline Authentication Provider resource to authenticate users in memory</td></tr><tr><td>Cache</td><td>Specify a cache resource via the Cache or Cache Redis resources</td></tr><tr><td>HTTP Signature<br>Generate HTTP Signature</td><td>Specify your HTTP Authentication Provider resource</td></tr><tr><td>OAuth2</td><td>Specify a Generic OAuth2 Authorization Server resource or a Gravitee AM Authorization Server resource</td></tr><tr><td>OpenID Connect UserInfo</td><td>Specify a Keycloak Adapter resource to use Keycloak as your OpenID Connect resource</td></tr><tr><td>AVRO to JSON<br>AVRO to Protobuf<br>Protobuf to JSON</td><td>Specify your Confluent Schema Registry to retrieve serialization and deserialization schemas from a Confluent Schema registry</td></tr></tbody></table>

{% hint style="info" %}
Global resources are available to all flows associated with the Gateway API, but are not available to other Gateway APIs.
{% endhint %}

## Examples

<details>

<summary>Example 1: Dynamic routing</summary>

Configure a v4 proxy API to query the stock levels of shop databases, then dynamically reroute any API call containing a shop ID to its associated URL:

1.  Define a list of properties for the shops, where `<key>` is the unique shop ID and `<value>` is the shop URL

    <figure><img src=".gitbook/assets/example1_properties list (1).png" alt=""><figcaption></figcaption></figure>
2.  Configure a dynamic routing policy that builds new URLs dynamically through property matching via the `#api.properties` statement:

    <div align="left"><figure><img src=".gitbook/assets/example1_properties rule (1).png" alt="" width="375"><figcaption></figcaption></figure></div>

If the ID in the request header matches the key of one of the properties, it is replaced with the URL. The dynamic routing policy then reroutes the API call to the URL.

</details>

<details>

<summary>Example 2: Monetization via latency</summary>

To monetize data delivery, consider a v4 message API that sends an alert whenever inventory is added to an online store. Tier 1 customers pay for item availability alerts in true real-time, while Tier 2 customers are notified for free, but in less than real-time.

1.  Add a keyless flow to the Default Keyless Plan

    <figure><img src=".gitbook/assets/example2_keyless flow (1).png" alt=""><figcaption></figcaption></figure>
2.  Apply a latency policy to the Default Keyless Plan

    <div align="left"><figure><img src=".gitbook/assets/example2_latency (1).png" alt="" width="375"><figcaption></figcaption></figure></div>
3. Select **Consumers** from the inner left nav
4.  Under the **Plans** tab, click **+ Add new plan**

    <figure><img src=".gitbook/assets/example2_add plan (1).png" alt=""><figcaption></figcaption></figure>
5. Select **API Key** from the drop-down menu and configure an API Key plan

Tier 2 customers can use our API for free, but new merchandise alerts are delayed by 30 minutes. Tier 1 customers who purchase the API Key plan are given unlimited access to real-time data.

</details>
