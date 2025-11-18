---
description: >-
  This article describes how to design and enforce flows using the v4 Policy
  Studio
---

# v4 API Policy Studio

{% hint style="info" %}
**Product limitations**

The v4 Policy Studio can only be used to design flows for APIs using the v4 API definition and supports applying policies at the message level or for pub/sub use cases. The v4 Policy Studio does not currently support Gravitee Debug mode.
{% endhint %}

## Introduction

Gravitee defines a flow as the method to control where, and under what conditions, policies act on an API transaction. The v4 Policy Studio is a no-code tool used to create and manage flows. The details of its purpose and functionality are described in the following sections:

* [**Design**](v4-api-policy-studio.md#design)**:** Manage all flows associated with your Gateway API
* [**Configuration**](v4-api-policy-studio.md#configure-flow-mode)**:** Modify settings related to flow execution
* [**Properties**](v4-api-policy-studio.md#api-properties)**:** Define key-value pairs at the API level
* [**Resources**](v4-api-policy-studio.md#resources)**:** Configure global resources to support your flows

## Design

Flows are created when policies are added to the Request, Response, Publish, and/or Subscribe phases of an existing v4 API. A single API supports multiple flows, which can be applied to different phases and target either subscribers of an individual plan or all users of the API.\
\
Policies are added to flows to enforce security, reliability, and proper data transfer. Examples of policies include traffic shaping, authentication/authorization, rate limiting, and dynamic routing.

<details>

<summary>Phases</summary>

Phases are available based on a flow's entrypoint(s). When a policy is applied and how it is enforced by the Gateway depends on the phase:

* **Request:** A policy is applied during connection establishment and enforced at the time of the request, before a client is given access to the API.
* **Response:** A policy is applied to the response from the initial connection and enforced after the request is allowed, but before the response is returned to the client.
* **Publish:** A policy is applied to messages sent to the endpoint and enforced when messages are published, before a client is given access to the API.
* **Subscribe:** A policy is applied to messages received by the entrypoint and enforced after messages are subscribed to, but before the response is returned to the client.

</details>

To create a flow and add policies:

1. Log in to your APIM Console
2. Selecting **APIs** from the left nav
3. Select the API for which to design a flow
4. Select **Policies** from the inner left nav
5.  Click the **+** icon for a plan or **Common flows** to create a flow

    <figure><img src="../../../../../../.gitbook/assets/flow_add flow (1).png" alt=""><figcaption><p>Create a flow</p></figcaption></figure>
6.  Configure the flow using the **Create a new flow** module with the options shown below

    <figure><img src="../../../../../../.gitbook/assets/flow_configure flow (1).png" alt=""><figcaption><p>Configure a new flow</p></figcaption></figure>

    * **Flow name:** Give your flow a descriptive name. Otherwise, a name will be automatically generated using the channel and operation.
    * **Operator:** Apply this flow to requests with a path that **Equals** or **Starts with** the specified **Channel**.
    * **Channel:** Define the path to use in conjunction with the **Operator** to determine if this flow should be applied.
    * **Entrypoints:** Select the entrypoint(s) for which the flow will be executed. If none are selected, the flow will be executed for all possible entrypoints, assuming required conditions are met.
    * **Entrypoints supported operations:** Select **Publish** and/or **Subscribe** as the operation(s) supported by the entrypoint(s). If none are selected, both will be supported.
    * **Condition:** Use [Gravitee's Expression Language (EL)](../gravitee-expression-language.md) to define specific conditions that will trigger flow execution.
7. Click **Create** in the modal, then **Save** on the **Policies** page
8.  To add a policy, click the **+** icon to the phase where the policy should be enforced

    <figure><img src="../../../../../../.gitbook/assets/flow_add policy (1).png" alt=""><figcaption><p>Add a policy</p></figcaption></figure>

    * Select the **Initial connection** tab to add policies to the Request and/or Response phase(s)
    * Select the **Event messages** tab to add policies to the Publish and/or Subscribe phase(s)
9. Select from the pre-populated policies that are valid by the entrypoints and endpoints
10. In the policy configuration modal, enter the information appropriate to and required by the policy
11. Click **Add policy**. The policy will appear in the flow diagram of the phase it was added to.

    <figure><img src="../../../../../../.gitbook/assets/flow_policy in flow (1).png" alt=""><figcaption><p>Policy added to flow</p></figcaption></figure>
12. Click **Save** on the **Policies** page, then redeploy your API to the Gateway for the changes to take effect

{% hint style="info" %}
To edit a policy, click on the three vertical dots on its icon in the flow diagram
{% endhint %}

## Configure flow mode

To configure the flow mode, click the gear icon in the **Flows** panel to open the **Flow execution** module

<figure><img src="../../../../../../.gitbook/assets/flow_execution (1).png" alt=""><figcaption><p>Configure flow mode</p></figcaption></figure>

* **Default flow mode:** Use the drop-down menu to select **Default** or **Best Match**
* **Fail on flow mismatch:** Enable to generate an error when there is no match between the request **Channel** and any defined flow

## API properties

Properties are read-only during the Gateway's execution of an API transaction. They can be accessed from within flows using Gravitee's Expression Language (EL) and the `#api.properties` statement. To configure properties:

To configure API properties:

1. Log in to your APIM Console
2. Selecting **APIs** from the left nav
3. Select the API for which to design a flow
4. Select **Configuration** from the inner left nav
5.  Select the **Properties** tab

    <figure><img src="../../../../../../.gitbook/assets/api properties_tab (1).png" alt=""><figcaption><p>Add API properties</p></figcaption></figure>
6. To add hardcoded properties, either:
   * Click **Add property** and enter property definitions one at a time as a key-value pair
   * Click **Import** and enter property definitions as a list in `<key>=<value>` format

### Encryption

{% hint style="warning" %}
Encrypted values can be used by API policies, but encrypted data should be used with care. APIM Gateway will automatically decrypt these values.
{% endhint %}

To encrypt a hardcoded API property value:

1.  Reset the default secret key in `gravitee.yml`. The secret must be 32 bytes in length.

    ```yaml
    # Encrypt API properties using this secret:
    api:
      properties:
        encryption:
             secret: vvLJ4Q8Khvv9tm2tIPdkGEdmgKUruAL6
     to provide the best security available.
    ```
2. Enable the **Encrypt** toggle when adding a property via **Add property**. Once you click **Save**, you can no longer edit, modify, or view the value. ![](<../../../../../../.gitbook/assets/api properties_add (1).png>)

### **Dynamic properties**

To configure dynamic properties:

1. Log in to your APIM Console
2. Selecting **APIs** from the left nav
3. Select the API for which to design a flow
4. Select **Configuration** from the inner left nav
5. Select the **Properties** tab
6.  Click the **Manage dynamically** button and define the configuration

    <figure><img src="../../../../../../.gitbook/assets/api properties_dynamically manage (1).png" alt=""><figcaption><p>Configure dynamic properties</p></figcaption></figure>

    * Toggle **Enabled** to ON
    * **Schedule:** A cron expression to schedule the health check
    * **HTTP Method:** The HTTP method that invokes the endpoint
    * **URL:** The target from which to fetch dynamic properties
    * **Request Headers:** The HTTP headers to add to the request fetching properties
    * **Request body:** The HTTP body content to add to the request fetching properties
    * (Optional) **Transformation (JOLT specification):** If the HTTP service doesn’t return the expected output, edit the JOLT transformation accordingly
    * Toggle **Use system proxy** ON to use the system proxy configured in APIM installation
7. Click **Save**

After the first call, the resultant property is added to the list of global properties, where its value is continuously updated according to the `cron` schedule specified.

{% hint style="info" %}
Key-value pairs can also be maintained using a dictionary, e.g., if this information is stored independently of the API creation process or applies to multiple APIs.
{% endhint %}

## Resources

Some policies support the addition of [resources](../configuring-apis-with-the-gravitee-api-management/resources.md), which can be used for actions such as authentication and schema registry validation. After you create resources, you will be able to reference them when designing policies. Policies that support resources include:

<table data-header-hidden><thead><tr><th width="242"></th><th></th></tr></thead><tbody><tr><td><a href="policies-for-you-apis/a-c/basic-authentication.md">Basic Authentication</a></td><td>Specify an LDAP Authentication Provider resource and/or an Inline Authentication Provider resource to authenticate users in memory</td></tr><tr><td><a href="policies-for-you-apis/a-c/cache.md">Cache</a></td><td>Specify a cache resource via the Cache or Cache Redis resources</td></tr><tr><td><a href="policies-for-you-apis/d-h/http-signature.md">HTTP Signature</a><br><a href="policies-for-you-apis/d-h/generate-http-signature.md">Generate HTTP Signature</a></td><td>Specify your HTTP Authentication Provider resource</td></tr><tr><td><a href="policies-for-you-apis/l-p/oauth2/">OAuth2</a></td><td>Specify a Generic OAuth2 Authorization Server resource or a Gravitee AM Authorization Server resource</td></tr><tr><td><a href="policies-for-you-apis/l-p/openid-connect-userinfo.md">OpenID Connect Userinfo</a></td><td>Specify a Keycloak Adapter resource to use Keycloak as your OpenID Connect resource</td></tr><tr><td><a href="policies-for-you-apis/a-c/avro-to-json.md">AVRO to JSON</a><br><a href="policies-for-you-apis/a-c/avro-to-protobuf.md">AVRO to Protobuf</a><br><a href="policies-for-you-apis/l-p/protobuf-to-json.md">Protobuf to JSON</a></td><td>Specify your Confluent Schema Registry to retrieve serialization and deserialization schemas from a Confluent Schema registry</td></tr></tbody></table>

{% hint style="info" %}
Global resources are available to all flows associated with the Gateway API, but are not available to other Gateway APIs.
{% endhint %}

## Examples

<details>

<summary>Example 1: Dynamic routing</summary>

Configure a v4 proxy API to query the stock levels of shop databases, then dynamically reroute any API call containing a shop ID to its associated URL:

1. Define a list of properties for the shops, where `<key>` is the unique shop ID and `<value>` is the shop URL ![](<../../../../../../.gitbook/assets/example1_properties list (1).png>)
2. Configure a dynamic routing policy that builds new URLs dynamically through property matching via the `#api.properties` statement: ![](<../../../../../../.gitbook/assets/example1_properties rule (1).png>)

If the ID in the request header matches the key of one of the properties, it is replaced with the URL. The dynamic routing policy then reroutes the API call to the URL.

</details>

<details>

<summary>Example 2: Monetization via latency</summary>

To monetize data delivery, consider a v4 message API that sends an alert whenever inventory is added to an online store. Tier 1 customers pay for item availability alerts in true real-time, while Tier 2 customers are notified for free, but in less than real-time.

1. Add a keyless flow to the Default Keyless Plan ![](<../../../../../../.gitbook/assets/example2_keyless flow (1).png>)
2. Apply a latency policy to the Default Keyless Plan ![](<../../../../../../.gitbook/assets/example2_latency (1).png>)
3. Select **Consumers** from the inner left nav
4. Under the **Plans** tab, click **+ Add new plan** ![](<../../../../../../.gitbook/assets/example2_add plan (1).png>)
5. Select **API Key** from the drop-down menu and configure an API Key plan

Tier 2 customers can use our API for free, but new merchandise alerts are delayed by 30 minutes. Tier 1 customers who purchase the API Key plan are given unlimited access to real-time data.

</details>
