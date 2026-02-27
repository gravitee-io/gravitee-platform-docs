# Aggregating multiple responses

## Overview

You can use Gravitee to initiate multiple back-end calls and aggregate all responses into a single response to the consumer, while keeping the front-end API exposed as a single API in Gravitee.

Gravitee provides various options to perform this task, but this guide focuses on a REST API using the HTTP Callout and Assign Content policies.

The high-level steps are:

1. [Create your API](aggregating-multiple-responses.md#create-your-api)
2. [Test #1](aggregating-multiple-responses.md#test-1) :Verify that you receive a response from the API
3. [Add the HTTP Callout and Assign Content policies](aggregating-multiple-responses.md#add-the-http-callout-and-assign-content-policies)
4. [Test #2](aggregating-multiple-responses.md#test-2) :Verify that you receive an aggregated response formed from multiple backend responses

## Prerequisites&#x20;

* A running Gravitee API Management instance
* An existing API that proxies a backend service (or follow the [Create an API guide ](https://documentation.gravitee.io/apim/getting-started/create-and-publish-your-first-api/create-an-api)to create one)
* Access to the API's **Policies** in the Gravitee Console

### Create your API

You first need an API that already proxies an existing service.  You just need to proxy a single endpoint at this stage.

If you do not yet have an API, review the[ Create an API guide](https://documentation.gravitee.io/apim/getting-started/create-and-publish-your-first-api/create-an-api), otherwise skip to the next step.

### Test #1

Ensure you can make a successful request to your API.

If you proxied one of the Gravitee testing APIs (such as `https://api.gravitee.io/echo`) you should see the following response to a `HTTP GET` request:

```json
{
    "headers": {
        "Host": "api.gravitee.io",
        "Accept": "*/*",
        "Postman-Token": "7f7b9a21-b95a-4644-ab73-d9074b97adf3",
        "User-Agent": "PostmanRuntime/7.51.1",
        "X-Gravitee-Request-Id": "7089a83c-5614-4640-89a8-3c5614e64090",
        "X-Gravitee-Transaction-Id": "c8a0c208-0738-4994-a0c2-080738199419",
        "accept-encoding": "deflate, gzip"
    },
    "query_params": {},
    "bodySize": 0
}
```

### Add the HTTP Callout and Assign Content policies

To make a second request, or multiple requests, to additional backend services, use the HTTP Callout policy. This policy stores the response in a defined variable, used later to aggregate the responses into a single response to the consumer.

Within your APIs' _Policies_ page, ensure you have created a _Flow_.  If not, then click on the + icon next to your Plan, and click on the Create button

<figure><img src="../../.gitbook/assets/image (1) (1).png" alt="" width="375"><figcaption><p>Click on the [+] button to create a new Flow under your Plan</p></figcaption></figure>

<figure><img src="../../.gitbook/assets/image (2) (1).png" alt="" width="375"><figcaption><p>Now click on the [Create] button to create your flow</p></figcaption></figure>

#### Configuring the HTTP Callout policy

1. Click the \[+] button (within the **Request phase**) to add a new Policy into your Flow.

<figure><img src="../../.gitbook/assets/image (4) (1).png" alt=""><figcaption><p>Click on the [+] button - within the Request phase - to add a new HTTP Callout Policy into the Flow</p></figcaption></figure>

2. Browse the list of policies for the HTTP Callout policy, and click Select.
3. Provide the necessary information, such as the HTTP method and URL. Optional fields include the request headers and request body.
4. To store the response from this HTTP Callout, you need to specify one or more **Context variables**. &#x20;
   1. In the example screenshot below, the full response (from the HTTP Callout) is stored in the `whattimeis_response` context variable.  E.g: `{#calloutResponse.content}`
   2. Other syntax is available, such as the built-in [`jsonPath`](https://docs.spring.io/spring-integration/reference/spel.html#built-in-spel-functions) function to obtain a specific value of a field from this response.  E.g.: `{#jsonPath(#calloutResponse.content, '$.headers.User-Agent)}`

{% hint style="info" %}
In Gravitee, a **context variable** (often called a _context attribute_) is a key-value pair stored in the execution context during a request or authentication flow. Policies can create or update these variables, and other policies or templates can then read them using the [Gravitee Expression Language](../../gravitee-expression-language.md).
{% endhint %}

5. Click Save.

<figure><img src="../../.gitbook/assets/image (6).png" alt=""><figcaption><p>HTTP Callout policy - configured to GET a response from <code>https://api.gravitee.io/whattimeisit</code>, and store the full response into the context attribute called 'whattimeisit_response'</p></figcaption></figure>

<details>

<summary>For demonstration purposes, an example response from <code>https://api.gravitee.io/whattimeisit</code> can be found here</summary>

```json
{
  "timestamp" : 1770907543520,
  "date" : "12/02/2026 14:45:43.520"
}
```

</details>

#### Configuring the Assign Content policy

1. Click the + button within the response phase to add a new policy to your flow.

<figure><img src="../../.gitbook/assets/image (7).png" alt=""><figcaption><p>Click on the [+] button - within the Response phase - to add a new Assign Content Policy into the Flow</p></figcaption></figure>

2. Browse the list of policies for the Assign Content policy, and click Select.
3. You now need to provide the **Body content**, which is compatible with the [Freemarker](https://freemarker.apache.org/) template engine thereby allowing complex transformations.
   1. In the example screenshot below, the 'Body content' has been configured to output just the `X-Gravitee-Transaction-Id` header value (from the endpoint response) as well as the `date` field from the HTTP Callout response.  Additionally, only for demonstration purposes, both the full responses from the endpoint and HTTP Callout policy are included too.&#x20;

{% code title="Example 'Body content' using Freemaker" lineNumbers="true" %}
```
<#assign endpoint_response = response.content?eval>
<#assign http_callout_response = context.attributes['whattimeisit_response']?eval_json>
{
  "transaction": "${endpoint_response.headers['X-Gravitee-Transaction-Id']}",
  "date": "${http_callout_response.date}",
  "original_endpoint_content": ${response.content},
  "original_whattimeisit_content": ${context.attributes['whattimeisit_response']}
}
```
{% endcode %}

{% hint style="info" %}
Notice the use of **`$`**`{...}` instead of **`#`**`{...}` when referencing Gravitee Expression Language objects. This is needed for compatibility with the Freemarker template engine.
{% endhint %}

4. The following walks through the body content Freemarker code, line by line:

> **Line 1:** Assign the first endpoint response `response.content` value into a Freemarker variable called `endpoint_response`&#x20;
>
> **Line 2:** Assign the HTTP Callout response value (that you stored as 'whattimeisit\_response' context variable/attribute) into a Freemarker variable called `http_callout_response`&#x20;
>
> **Line 3:** Start your new response, such as a JSON object in this example.
>
> **Line 4:** Create a new 'transaction' JSON attribute with the value sourced from the 'X-Gravitee-Transaction-Id' field of the first endpoint response.
>
> **Line 5:** Create a new 'date' JSON attribute with the value sourced from the 'date' field of the HTTP Callout response.
>
> **Line 6 and 7:** Only for demonstration purposes, both the full responses from the endpoint and HTTP Callout policy are included too.&#x20;
>
> **Line 8:** Close your JSON object.

4. Click Save.

<figure><img src="../../.gitbook/assets/image (10).png" alt=""><figcaption><p>Assign Content policy - configured to overwrite the final response to the consumer.  The 'Body content' has been configured to output just the <code>X-Gravitee-Transaction-Id</code> header value (from the endpoint response) as well as the <code>date</code> field from the HTTP Callout response.  Additionally, only for demonstration purposes, both the full responses from the endpoint and HTTP Callout policy are included too.</p></figcaption></figure>

5. Click the Flow Save button, and then click **Deploy API** to apply your changes to the Gateway.

<figure><img src="../../.gitbook/assets/image (13).png" alt=""><figcaption></figcaption></figure>

### Test #2

Now that the API includes one or more HTTP Callout policies and the Assign Content policy, verify that the API returns an aggregated response formed from the initial endpoint response and the HTTP Callout responses.

As in [Test #1](aggregating-multiple-responses.md#test-1), perform the same HTTP GET request to your API. The aggregated response now appears.&#x20;

If you followed this exact guide and used `https://api.gravitee.io/echo` and `https://api.gravitee.io/whattimeisit` the following response appears for an HTTP GET request:

```json
{
    "transaction": "77aaf79b-443c-41c4-aaf7-9b443c41c4e1",
    "date": "12/02/2026 14:50:09.699",
    "original_endpoint_content": {
        "headers": {
            "Host": "api.gravitee.io",
            "Accept": "*/*",
            "Postman-Token": "525cb226-f36a-48c5-ba70-e7e327fb1936",
            "User-Agent": "PostmanRuntime/7.51.1",
            "X-Gravitee-Request-Id": "e648378d-4912-4921-8837-8d4912492175",
            "X-Gravitee-Transaction-Id": "77aaf79b-443c-41c4-aaf7-9b443c41c4e1",
            "accept-encoding": "deflate, gzip"
        },
        "query_params": {},
        "bodySize": 0
    },
    "original_whattimeisit_content": {
        "timestamp": 1770907809699,
        "date": "12/02/2026 14:50:09.699"
    }
}
```
