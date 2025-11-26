---
description: >-
  This article walks through how to design and enforce flows using the v4 Policy
  Studio.
---

# v4 API Policy Studio

{% hint style="info" %}
**Product limitations**

The v4 Policy Studio can only design flows for APIs using the v4 API definition. Unlike the legacy v2 Policy Studio, the v4 Policy Studio supports designing and enforcing flows at the message level or for pub/sub use cases.

\
The v4 Policy Studio does not currently support Gravitee Debug mode. Support for this is planned for future releases.
{% endhint %}

## Introduction

Gravitee defines a flow as the method to control where, and under what conditions, policies act on an API transaction. The v4 Policy Studio is a no-code tool used to create and manage flows. The details of its purpose and functionality are broken into the following sections::

* **Design:** Manage all flows associated with your Gateway API
* **Configuration:** Modify settings around flow execution
* **Properties:** Define key-value pairs at the API level. These properties are read-only during the Gateway's execution of an API transaction.
* **Resources:** Configure global resources to support your Gateway API's flows

## Design

Flows can be added to existing v4 APIs, which are accessed by selecting **APIs** in the left-hand nav. Next, select the API for which you want to design a flow. You'll be taken to the API's **General** **Info** page. Select **Policy Studio** from the inner left-hand nav.

In the Policy Studio, you can create a flow, then add one or more policies to the Request, Response, Publish, and/or Subscribe phases. These phases are available based on a flow's chosen entrypoint(s), with Request and Response appearing under the **Initial connection** tab and Subscribe and Publish appearing under the **Event messages** tab. When a policy is applied and how it is enforced depends on the phase:

* **Request phase:** A policy is applied during the connection establishment. The Gateway enforces the policy at the time of the request, before a client is given access to the API that they are trying to call.
* **Response phase:** A policy is applied to the response from the initial connection. The Gateway enforces the policy after the request is allowed, but before the response is returned to the client.
* **Publish phase:** A policy is applied on messages sent to the endpoint. The Gateway enforces the policy when messages are published, before a client is given access to the API that they are trying to call.
* **Subscribe phase:** A policy is applied on messages received by the entrypoint. The Gateway enforces the policy after messages are subscribed to, but before the response is returned to the client.

You can create multiple policies for a single flow, each with a different configuration and applied to a different phase of the API. Flows can also be associated with specific plans or exist at the API level as common flows.

The sample Gateway API shown below has three plans: Keyless, API Key, and JWT. Flows can be set to target subscribers of any of these three plans, like the "sample API Key flow", or they can target all users of the API, such as the "sample HTTP Get flow" and "sample Websocket flow".

<figure><img src="../../.gitbook/assets/policy studio_flow.png" alt=""><figcaption><p>Sample v4 Policy Studio</p></figcaption></figure>

### Create a flow

As an example, let's create a flow that targets all users of the API.

First, click the **+** icon on the **Common flows** button to create a flow. Before adding policies to the flow, you'll need to configure the flow using the **Create a new flow** module with the options shown below.

<figure><img src="../../.gitbook/assets/create a new flow.png" alt=""><figcaption><p><strong>Create a new flow</strong> module</p></figcaption></figure>

Define the following:

* **Flow name:** Give your flow a descriptive name. If you don't, a name will be automatically generated using the channel and operation.
* **Operator:** Apply this flow to requests with a path that **Equals** or **Starts with** the specified **Channel**.
* **Channel:** Define the path to use in conjunction with the **Operator** to determine if this flow should be applied.
* **Entrypoints:** Select the entrypoint(s) for which you want the flow to be executed. If none are selected, the flow will be executed for all possible entrypoints, assuming required conditions are met. Available entrypoints are **HTTP GET**, **HTTP POST**, **Websocket**, **Server-Sent Events**, and **Webhook**.
* **Entrypoints supported operations:** Select **Publish** and/or **Subscribe** as the operation(s) supported by the entrypoint(s). If none are selected, both will be supported.
* **Condition:** Define specific conditions that will trigger flow execution using [Gravitee's Expression Language (EL)](../gravitee-expression-language.md).

Once you've clicked **Create** to add a flow, be sure to also click **Save** in the upper right of the Policy Studio.

### Add policies

Policies are added to flows to enforce security, reliability, and proper data transfer. Examples of policies include traffic shaping, authentication/authorization, rate limiting, and dynamic routing.

To add a policy to a flow, click the **+** icon in the phase where you want the policy enforced. The module that appears is pre-populated with only the selections that are valid and/or supported based on the entrypoints and endpoints chosen for the flow. For example, below are the possible policies to configure for the **Request phase** of the "sample HTTP Get flow" shown above:

<figure><img src="../../.gitbook/assets/sample add policy.png" alt=""><figcaption><p>Sample policy selection</p></figcaption></figure>

Clicking on one of the available policies will open a configuration module. After you have made the selections and filled in the information appropriate to and required by your policy, click **Add policy**. The policy will appear in the flow diagram of the phase it was added to.

For example, adding a **Latency** policy to the **Request phase** of the "sample HTTP Get flow" also adds **Latency** policy elements to the corresponding flow diagram.

<figure><img src="../../.gitbook/assets/latency policy.png" alt=""><figcaption><p>Sample policy applied</p></figcaption></figure>

Once you've clicked **Add policy** to add a policy, be sure to also click **Save** in the upper right of the Policy Studio. To edit a policy, click on the three vertical dots on its icon in the flow diagram.

Whenever you add or edit a flow or policy, you'll need to redeploy your API to the Gateway for the changes to take effect. You'll see a red, circular icon above **Policy Studio** in the inner left nav that has the tooltip message "API out of sync".

## Configure flow mode

Gravitee offers two flow modes: **Default** and **Best Match**. The **Default** flow selection is based on the **Operator** defined for your flow and whether it **Equals** or **Starts with** the specified path, or **Channel**. Choose the **Best Match** option to select the flow that's the closest match to the API request path.

To select the flow mode, click the gear icon in the **Flows** panel to open the **Flow execution** module, then use the drop-down menu. You can also toggle **Fail on flow mismatch** to ON to generate an error when there is no match between the request **Channel** and any defined flow.

<figure><img src="../../.gitbook/assets/flow modes.png" alt=""><figcaption><p>v4 Policy Studio: Configure flow mode</p></figcaption></figure>

## API properties

Properties are key-value pairs you can define at the Gateway API level to implement different logic in your flows and policies. Properties are read-only during the Gateway's execution of an API transaction but can be accessed from within a flow using Gravitee's Expression Language (EL) and the `#api.properties` statement.

To configure API properties, select **Properties** from the inner left nav. To hardcode properties, either specify properties one at a time or toggle from **Simple** to **Expert** mode and enter property definitions in `<key>=<value>` format.

<figure><img src="../../.gitbook/assets/policy studio_properties expert.png" alt=""><figcaption><p>API properties expert mode</p></figcaption></figure>

### Encryption

Gravitee supports encryption to protect sensitive or confidential data stored as hardcoded property values. The encryption method for API properties is based on the default secret key in the `gravitee.yml` config file. Before using encryption, you must override the secret key to ensure proper security.

{% hint style="warning" %}
The secret must be 32 bytes in length.
{% endhint %}

{% code title="gravitee.yml" %}
```yaml
# Encrypt API properties using this secret:
api:
  properties:
    encryption:
         secret: vvLJ4Q8Khvv9tm2tIPdkGEdmgKUruAL6
 to provide the best security available.
```
{% endcode %}

To encrypt an API property, enable the adjacent **Encrypted** toggle. The property value will remain unencrypted and editable until you save your changes. Once you select **Save**, you can no longer edit, modify, or view the value.

{% hint style="danger" %}
Encrypted values can be used by API policies, but encrypted data should be used with care. **APIM Gateway will automatically decrypt these values**.
{% endhint %}

<figure><img src="../../.gitbook/assets/policy studio_encryption.png" alt=""><figcaption><p>Encrypted API property</p></figcaption></figure>

### **Dynamic properties**

In addition to hardcoded properties, Gravitee supports dynamic properties. The dynamic properties associated with a Gateway API are fetched from a remote server on a regular schedule and subsequently updated according to the details you specify.

To access the dynamic properties module, select **Properties** from the inner left nav and click **CONFIGURE DYNAMIC PROPERTIES**.

<figure><img src="../../.gitbook/assets/policy studio_dynamic properties.png" alt=""><figcaption><p>Configure dynamic properties</p></figcaption></figure>

To configure dynamic properties:

1. Specify the details of the property:
   * `cron` schedule
   * HTTP method(s)
   * Service URL
   * Whether to use a system proxy
   * Request headers and body to include with the call
   * JOLT transformation to perform on the response
2. Toggle **Enabled** ON
3. Click the tick icon ![tick icon](https://docs.gravitee.io/images/icons/tick-icon.png) to save your changes
4. Click **Save**

After the first call, the resultant property is added to the list of global properties, where its value is continuously updated according to the `cron` schedule specified.

{% hint style="info" %}
**Dictionaries vs API properties**

The list of shop IDs and URLs could also be maintained using a dictionary, e.g., in organizations where the administrator maintains this information independently of the API creation process or if the list needs to be available to multiple APIs. See [Dictionaries](../../getting-started/configuration/the-gravitee-api-gateway/dictionaries.md) for more information.
{% endhint %}

## Resources

Some policies support the addition of resources, which can be used for authentication and schema registry validation, etc. Policies and the resources they support or rely on are shown in the table below.

| Policy type                                          | Resource(s)                                                                         |
| ---------------------------------------------------- | ----------------------------------------------------------------------------------- |
| Cache                                                | <p>Cache<br>Cache Redis</p>                                                         |
| OAuth2                                               | <p>OAuth2 - Gravitee Access Management<br>OAuth2 - Generic Authorization Server</p> |
| OpenID Connect - Userinfo                            | Keycloak Adapter                                                                    |
| Serialization & deserialization (e.g., Avro <> JSON) | Confluent Schema Registry                                                           |
| HTTP signature                                       | HTTP Authentication Provider                                                        |
| Basic authentication                                 | <p>LDAP Authentication Provider<br>Inline Authentication Provider</p>               |

After these resources are created, you will be able to reference them when designing policies using the **Policy Studio**. Refer to the [Resources](../api-configuration/resources.md) and [Policy Reference](README.md#v4) documentation for more information on resources and how they are used by policies.

{% hint style="info" %}
Global resources are globally available to all flows associated with the Gateway API. However, they will not be available to other Gateway APIs.
{% endhint %}

## Examples

### Example 1: Dynamic routing

{% hint style="info" %}
This example applies to v4 APIs using the [**Proxy Upstream Protocol**](../create-apis/the-api-creation-wizard/v4-api-creation-wizard.md#step-2-entrypoints) backend exposure method.
{% endhint %}

In this example, we want our Gateway API to query our shop databases to check their stock levels. We will dynamically reroute any API call containing a shop ID to its associated URL.

The first step is to define a list of properties for the shops. For each property, enter a unique shop ID for the key and the URL of the shop for the value.

<figure><img src="../../.gitbook/assets/example1_properties.png" alt=""><figcaption></figcaption></figure>

We then configure a dynamic routing policy for the API via a routing rule that builds a new URL dynamically through property matching. The URL is created with a `#api.properties` statement that matches properties returned by querying the request header that contains the shop ID.

<figure><img src="../../.gitbook/assets/example1_dynamic routing.png" alt=""><figcaption></figcaption></figure>

If the ID in the request header matches the key of one of the properties, it is replaced with the URL. The dynamic routing policy then reroutes the API call to the URL.

### Example 2: Monetization via latency

{% hint style="info" %}
This example applies to v4 APIs using the [**Introspect Messages from Event-Driven Backend**](../create-apis/the-api-creation-wizard/v4-api-creation-wizard.md#step-2-entrypoints) backend exposure method.
{% endhint %}

In this example, our Gateway API sends an alert whenever inventory is added to our online store that sells limited edition designer merchandise at discount prices. Casual shoppers pay a certain amount to learn about item availability in slightly less than real-time, while our best customers pay more to access this data in true real-time.

To monetize data delivery, we can use the Keyless and API Key plans introduced [above](v4-api-policy-studio.md#design). First, we add a "sample Keyless flow" to our Keyless plan.

<figure><img src="../../.gitbook/assets/sample keyless flow.png" alt=""><figcaption></figcaption></figure>

Next, we apply a latency policy to our Keyless plan.

<figure><img src="../../.gitbook/assets/sample keyless policy.png" alt=""><figcaption></figcaption></figure>

Customers can use our API for free, but new merchandise alerts are delayed by 30 minutes. However, customers who purchase our API Key plan are given unlimited access to real-time data.
