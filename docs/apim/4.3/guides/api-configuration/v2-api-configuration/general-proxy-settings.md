---
description: This article describes how to configure v2 API proxy settings
---

# Proxy Settings

## Introduction

To configure the **Proxy** settings for a v2 API:

1. Log in to your APIM Console
2. Select APIs from the left nav
3. Select your API
4. Under the Proxy section of the inner left nav, select from the following:
   * [Entrypoints](general-proxy-settings.md#entrypoints)
   * [CORS](general-proxy-settings.md#cors)
   * [Deployments](general-proxy-settings.md#deployments)
   * [Response templates](general-proxy-settings.md#response-templates)
   * [Properties](general-proxy-settings.md#properties)&#x20;
   * [Resources](general-proxy-settings.md#resources)

## Entrypoints

To configure the API entrypoints:&#x20;

1.  Select **Entrypoints** from the inner left nav&#x20;

    <figure><img src="../../../.gitbook/assets/v2 proxy_entrypoints.png" alt=""><figcaption><p>Configure v2 API entrypoints</p></figcaption></figure>



    * Edit your **Context-path** or create a new one via **Add context-path**
    * Toggle **Enable virtual hosts** ON or OFF
2. Click **Save**

## CORS

CORS is a mechanism that allows resources on a web page to be requested from another domain. To configure CORS for your API:

1.  Select **CORS** from the inner left nav&#x20;

    <figure><img src="../../../.gitbook/assets/v2 proxy_CORS.png" alt=""><figcaption><p>Configure CORS</p></figcaption></figure>
2.  Set the following parameters:

    * **Enable CORS:** Toggle to ON to enable CORS.
    * **Access-Control-Allow-Origin:** Define a URI that can access the resource. Enter \* to allow all requests, regardless of origin.

    {% hint style="danger" %}
    A value of \* is not recommended for production environments. By allowing cross-origin requests, a server may inadvertently expose sensitive information to unauthorized parties. For example, if a server includes sensitive data in a response that is accessible via CORS, an attacker could use a malicious website to extract that data.
    {% endhint %}

    * **Access-Control-Allow-Methods:** Select the method(s) allowed when accessing the resource, which is used in response to a preflight request: `GET`, `DELETE`, `PATCH`, `POST`, `PUT`, `OPTIONS`, `TRACE`, and/or `HEAD`.
    * **Access-Control-Allow-Headers:** Select the HTTP header(s) that can be used when making the actual request, in response to a preflight request. Typically, your request header will include `Access-Control-Request-Headers`, which relies on the CORS configuration to allow its values.
    * **Access-Control-Allow-Credentials:** Toggle ON or OFF to indicate whether the response to the request can be exposed when the credentials flag is true.
    * **Max Age:** Specify how long (in seconds) the results of a preflight request can be cached. This is optional, and a value of `-1` indicates it is disabled.
    * **Access-Control-Expose-Headers:** Define a list of headers that browsers are allowed to access.
    * **Run policies for preflight requests:** Toggle ON for the API Gateway to execute policies for preflight-requests. By default, this is not enabled.
3. Click **Save**

{% hint style="info" %}
**Troubleshooting CORS**

All requests rejected because of CORS issues will generate logs that you can view in the `Analytics` section of your API logs.

<img src="../../../.gitbook/assets/graviteeio-troubleshooting-cors.png" alt="" data-size="original">
{% endhint %}

## Deployments

**Deployments** is where you can choose to use [sharding tags](../../../getting-started/configuration/apim-gateway/sharding-tags.md) sharding tags to control where your API is deployed. To configure sharding tags for your API:

1.  Select **Deployments** from the inner left nav&#x20;

    <figure><img src="../../../.gitbook/assets/v2 proxy_deployments.png" alt=""><figcaption><p>Configure sharding tags</p></figcaption></figure>
2. From the **Sharding tags** drop-down menu, choose one or more sharding tags
3. Click **Save**

## Response templates

Response templates are used to override the default values sent in response to consumer calls to an API. Response template overrides are triggered by error keys, which are specific to policies. Responses can be templatized if the errors raised during the request/response phase(s) are associated with overridable policy keys. Each response template defines the new values to be returned for one or more status codes when the template is triggered.

### Prerequisites

Prior to defining a response template, verify:

* Which policies have been applied to the API. This can be viewed in the [API's plan](../../api-exposure-plans-applications-and-subscriptions/plans/README.md).
* Which error keys can be overridden per policy associated with your API.&#x20;

Below are the policy error keys that you can override by configuring response templates:

<table><thead><tr><th width="417">Key</th><th>Policy</th></tr></thead><tbody><tr><td><code>API_KEY_MISSING</code></td><td>API key</td></tr><tr><td><code>API_KEY_INVALID</code></td><td>API key</td></tr><tr><td><code>QUOTA_TOO_MANY_REQUESTS</code></td><td>Rate limiting</td></tr><tr><td><code>RATE_LIMIT_TOO_MANY_REQUESTS</code></td><td>Rate limiting</td></tr><tr><td><code>REQUEST_CONTENT_LIMIT_TOO_LARGE</code></td><td>Request content limit</td></tr><tr><td><code>REQUEST_CONTENT_LIMIT_LENGTH_REQUIRED</code></td><td>Request content limit</td></tr><tr><td><code>REQUEST_TIMEOUT</code></td><td>Mock, Callout HTTP, Request validation</td></tr><tr><td><code>REQUEST_VALIDATION_INVALID</code></td><td>Request validation</td></tr><tr><td><code>RESOURCE_FILTERING_METHOD_NOT_ALLOWED</code></td><td>Resource filtering</td></tr><tr><td><code>RBAC_INVALID_USER_ROLES</code></td><td>Role-based access control</td></tr><tr><td><code>RESOURCE_FILTERING_FORBIDDEN</code></td><td>Resource filtering</td></tr><tr><td><code>RBAC_FORBIDDEN</code></td><td>Role-based access control</td></tr><tr><td><code>RBAC_NO_USER_ROLE</code></td><td>Role-based access control</td></tr><tr><td><code>OAUTH2_MISSING_SERVER</code></td><td>OAuth2</td></tr><tr><td><code>OAUTH2_MISSING_HEADER</code></td><td>OAuth2</td></tr><tr><td><code>OAUTH2_MISSING_ACCESS_TOKEN</code></td><td>OAuth2</td></tr><tr><td><code>OAUTH2_INVALID_ACCESS_TOKEN</code></td><td>OAuth2</td></tr><tr><td><code>OAUTH2_INSUFFICIENT_SCOPE</code></td><td>OAuth2</td></tr><tr><td><code>OAUTH2_INVALID_SERVER_RESPONSE</code></td><td>OAuth2</td></tr><tr><td><code>OAUTH2_SERVER_UNAVAILABLE</code></td><td>OAuth2</td></tr><tr><td><code>HTTP_SIGNATURE_INVALID_SIGNATURE</code></td><td>HTTP Signature</td></tr><tr><td><code>JWT_MISSING_TOKEN</code></td><td>JWT</td></tr><tr><td><code>JWT_INVALID_TOKEN</code></td><td>JWT</td></tr><tr><td><code>JSON_INVALID_PAYLOAD</code></td><td>JSON validation</td></tr><tr><td><code>JSON_INVALID_FORMAT</code></td><td>JSON validation</td></tr><tr><td><code>JSON_INVALID_RESPONSE_PAYLOAD</code></td><td>JSON validation</td></tr><tr><td><code>JSON_INVALID_RESPONSE_FORMAT</code></td><td>JSON validation</td></tr><tr><td><code>GATEWAY_INVALID_REQUEST</code></td><td>All</td></tr><tr><td><code>GATEWAY_INVALID_RESPONSE</code></td><td>All</td></tr><tr><td><code>GATEWAY_OAUTH2_ACCESS_DENIED</code></td><td>All</td></tr><tr><td><code>GATEWAY_OAUTH2_SERVER_ERROR</code></td><td>All</td></tr><tr><td><code>GATEWAY_OAUTH2_INVALID_CLIENT</code></td><td>All</td></tr><tr><td><code>GATEWAY_MISSING_SECURITY_PROVIDER</code></td><td>All</td></tr><tr><td><code>GATEWAY_PLAN_UNRESOLVABLE</code></td><td>All</td></tr><tr><td><code>GATEWAY_POLICY_INTERNAL_ERROR</code></td><td>All</td></tr></tbody></table>

### Create a response template

When creating response templates, you can define:

* Multiple templates for one API (for multiple policies and/or multiple error keys sent by the same policy)
* Multiple template definitions for the same error key in a single template (for different content types or status codes)

To configure a response template:

1. Select **Response Templates** from the inner left nav
2. Click on the **Add new Response Template** button
3.  Customize the **Create a new Response Template** form&#x20;

    <figure><img src="../../../.gitbook/assets/create response template.png" alt=""><figcaption><p>Configure a new response template</p></figcaption></figure>

    * **Template key:** Choose the template key via the **Template key** drop-down.
    * **Accept header to match:** Specify the requests header that should trigger use of the response template. The default value is `*/*`. To send the template override values only for JSON or XML requests, specify `JSON` or `XML.`
    * **Status code:** Specify the status code that to send to the API consumer via the **Status code** drop-down.
    * Specify the override values to send to the API consumer. These can either be:
      * One or more HTTP headers to include in the response
      * A response template body
4. Click **Create**

## Properties

Properties are read-only during the Gateway's execution of an API transaction. They can be accessed from within flows using Gravitee's Expression Language (EL) and the `#api.properties` statement. To configure properties:

To configure API properties:

1.  Select **Properties** from the inner left nav&#x20;

    <figure><img src="../../../.gitbook/assets/v2 proxy_properties.png" alt=""><figcaption><p>Add API properties</p></figcaption></figure>
2. To add hardcoded properties, either:
   * Click **Add property** and enter property definitions one at a time as a key-value pair
   * Click **Import** and enter property definitions as a list in `<key>=<value>` format&#x20;

### Encryption

{% hint style="warning" %}
Encrypted values can be used by API policies, but encrypted data should be used with care. APIM Gateway will automatically decrypt these values.
{% endhint %}

To encrypt a hardcoded API property value:

1.  Reset the default secret key in `gravitee.yml`. The secret must be 32 bytes in length.&#x20;

    ```yaml
    # Encrypt API properties using this secret:
    api:
      properties:
        encryption:
             secret: vvLJ4Q8Khvv9tm2tIPdkGEdmgKUruAL6
     to provide the best security available.
    ```
2. Enable the **Encrypt** toggle when adding a property via **Add property**. Once you click **Save**, you can no longer edit, modify, or view the value. ![](<../../../.gitbook/assets/api properties\_add (1).png>)

### **Dynamic properties**

To configure dynamic properties:

1.  Click the **Manage dynamically** button and define the configuration&#x20;

    <figure><img src="../../../.gitbook/assets/v2 proxy_properties dynamic.png" alt=""><figcaption><p>Configure dynamic properties</p></figcaption></figure>

    * Toggle **Enabled** to ON
    * **Schedule:** A cron expression to schedule the health check
    * **HTTP Method:** The HTTP method that invokes the endpoint
    * **URL:** The target from which to fetch dynamic properties
    * **Request Headers:** The HTTP headers to add to the request fetching properties
    * **Request body:** The HTTP body content to add to the request fetching properties
    * (Optional) **Transformation (JOLT specification):** If the HTTP service doesn’t return the expected output, edit the JOLT transformation accordingly
    * Toggle **Use system proxy** ON to use the system proxy configured in APIM installation
2. Click **Save**

After the first call, the resultant property is added to the list of global properties, where its value is continuously updated according to the `cron` schedule specified.

{% hint style="info" %}
Key-value pairs can also be maintained using a dictionary, e.g., if this information is stored independently of the API creation process or applies to multiple APIs.&#x20;
{% endhint %}

## Resources

Some policies support the addition of [resources](../resources.md), which can be used for actions such as authentication and schema registry validation. After you create resources, you will be able to reference them when designing policies. Policies that support resources include:

<table data-header-hidden><thead><tr><th width="242"></th><th></th></tr></thead><tbody><tr><td><a href="../../../reference/policy-reference/basic-authentication.md">Basic Authentication</a></td><td>Specify an LDAP Authentication Provider resource and/or an Inline Authentication Provider resource to authenticate users in memory</td></tr><tr><td><a href="../../../reference/policy-reference/cache.md">Cache</a></td><td>Specify a cache resource via the Cache or Cache Redis resources</td></tr><tr><td><a href="../../../reference/policy-reference/http-signature.md">HTTP Signature</a><br><a href="../../../reference/policy-reference/generate-http-signature.md">Generate HTTP Signature</a></td><td>Specify your HTTP Authentication Provider resource</td></tr><tr><td><a href="../../../reference/policy-reference/oauth2/">OAuth2</a></td><td>Specify a Generic OAuth2 Authorization Server resource or a Gravitee AM Authorization Server resource</td></tr><tr><td><a href="../../../reference/policy-reference/openid-connect-userinfo.md">OpenID Connect Userinfo</a></td><td>Specify a Keycloak Adapter resource to use Keycloak as your OpenID Connect resource</td></tr><tr><td><a href="../../../reference/policy-reference/avro-to-json.md">AVRO to JSON</a><br><a href="../../../reference/policy-reference/avro-to-protobuf.md">AVRO to Protobuf</a><br><a href="../../../reference/policy-reference/protobuf-to-json.md">Protobuf to JSON</a></td><td>Specify your Confluent Schema Registry to retrieve serialization and deserialization schemas from a Confluent Schema registry</td></tr></tbody></table>

{% hint style="info" %}
Global resources are available to all flows associated with the Gateway API, but are not available to other Gateway APIs.
{% endhint %}
