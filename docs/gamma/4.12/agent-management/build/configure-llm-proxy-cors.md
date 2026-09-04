---
hidden: false
noIndex: false
description: Let browser-based clients on other origins call an LLM Proxy by enabling CORS and setting the allowed origins, methods, and headers. Follow the steps on the CORS page.
---

# Configure LLM Proxy CORS

From Gamma 4.12.18, the **CORS** page configures cross-origin access for an LLM Proxy. When CORS is enabled, the gateway adds the `Access-Control-*` headers to the responses of the proxy and answers browser preflight requests itself. CORS is off until you enable it, so a proxy created before the page existed keeps its behavior.

## Prerequisites

Before you begin, confirm that you have the following:

* An LLM Proxy. For more information, see [Create an LLM Proxy](create-an-llm-proxy.md).
* Permission to update the API definition of the proxy. Without it, the page is read-only: the **Enable CORS** switch and the other fields stay disabled, and the **Save changes** button never appears.

To open the page, follow these steps:

1. From the Gamma console sidebar, select **Agent Management**.
2. Under **Secure**, select **LLM Proxies**.
3. Select your LLM Proxy.
4. Under **General**, click **CORS**.

<!-- TODO: Screenshot of the CORS page of an LLM Proxy on a Gamma 4.12.18 stack, with CORS enabled and one allowed origin -->

<figure><img src="../../.gitbook/assets/PLACEHOLDER-gamma-aim-llm-proxy-cors-4-12.png" alt=""><figcaption><p>The CORS page</p></figcaption></figure>

## Enable CORS

Turn on the **Enable CORS** switch. The other settings on the page stay disabled until CORS is enabled.

## Set the origins, methods, and headers

The **Origins, methods and headers** card carries four list fields. Type a value and press Enter or a comma to add it, and click the cross on a value to remove it. The buttons under a field add a common value with one click. Use `*` to allow any value.

| Field                             | Description                                                                                                                                                                                                                                                       |
| --------------------------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **Access-Control-Allow-Origin**   | Origins allowed to call this proxy, such as `https://app.example.com`. Scheme, domain, and port must all match. A value that contains `(`, `[`, or `*` is also evaluated as a regular expression.                                                             |
| **Access-Control-Allow-Methods**  | HTTP methods allowed in cross-origin requests. The buttons offer `GET`, `POST`, `PUT`, `PATCH`, `DELETE`, `HEAD`, and `OPTIONS`.                                                                                                                                  |
| **Access-Control-Allow-Headers**  | Headers the caller may send in the actual request. The buttons offer `Accept`, `Authorization`, `Content-Type`, `Origin`, `X-API-Key`, and `X-Requested-With`.                                                                                                     |
| **Access-Control-Expose-Headers** | Response headers the browser may surface to JavaScript. The buttons offer `Content-Length`, `Content-Range`, `X-Request-Id`, and the `X-LLM-Proxy-*` headers that the LLM Proxy entrypoint adds to its responses.                                                 |

Header names are saved in lowercase, so `Content-Type` reads back as `content-type` after you save. Enter methods in uppercase: the gateway compares the method of a preflight request with the saved values exactly.

An origin is refused when you save if it's neither `*`, `null`, an origin of the form `scheme://host` with an optional port, nor a valid regular expression. The page then shows **`<value>` is not valid as an 'allow origin' value**.

{% hint style="warning" %}
Adding `*` as an allowed origin shows the **Allowing all origins** alert, because `*` exposes the proxy to any website. Make sure that authentication is enforced. While `*` is listed, the **Access-Control-Allow-Credentials** switch is disabled.
{% endhint %}

## Adjust the advanced settings

The **Advanced settings** card covers credentials, the preflight cache duration, and policy execution.

* **Access-Control-Allow-Credentials**. Lets browsers send cookies and HTTP authentication with cross-origin requests. When the switch is on, the gateway adds `Access-Control-Allow-Credentials: true` to the responses. The switch isn't compatible with `*` as the allowed origin.
* **Run policies on preflight**. By default, the gateway answers a preflight `OPTIONS` request as soon as the CORS checks pass, without running the flows of the proxy. Turn the switch on to run the policies of the flows on preflight requests too. The preflight request is still answered by the gateway and never reaches a model provider, and the security chain of the plans is skipped for preflight requests whether the switch is on or off.
* **Max age (seconds)**. How long the browser may cache the preflight response. The default, `-1`, sends no `Access-Control-Max-Age` header. The field accepts values from `-1` to `2147483647`, and a value above `600` shows the **Long preflight cache** warning.

## Save and deploy

A change on the page shows the **Discard** and **Save changes** buttons at the top of the page. Click **Save changes** to apply, or **Discard** to revert. A successful save shows **CORS settings saved**. When the save is refused, the page shows the message returned by the API.

Saving with the **Enable CORS** switch off empties the saved origins, methods, and headers: they read back empty when you turn CORS on again.

Saving updates the API definition but doesn't deploy it. The **This deployable is out of sync.** banner appears at the top of the detail view. Click **Deploy** to push the change to the gateway.

## Verification

To verify that the gateway applies the settings, follow these steps:

1. Enable CORS, add the origin `https://app.example.com`, add the `POST` method, and add the `Content-Type` header. Click **Save changes**, and then click **Deploy** in the **This deployable is out of sync.** banner.
2. Send a preflight request to a URL of the proxy:

    ```bash
    curl -i -X OPTIONS <proxy-url> \
      -H "Origin: https://app.example.com" \
      -H "Access-Control-Request-Method: POST" \
      -H "Access-Control-Request-Headers: content-type"
    ```

    The response carries `Access-Control-Allow-Origin: https://app.example.com`, `Access-Control-Allow-Methods`, and `Access-Control-Allow-Headers`.
3. Send the same request with an origin you didn't allow, such as `https://other.example.com`. The gateway refuses the preflight with status `400` and no `Access-Control-*` headers.

An actual cross-origin request from an allowed origin gets `Access-Control-Allow-Origin` in its response and, when you set exposed headers, `Access-Control-Expose-Headers`. From an origin that isn't allowed, the proxy still handles the request, but the gateway strips `Access-Control-Allow-Origin`, `Access-Control-Allow-Credentials`, and `Access-Control-Expose-Headers` from the response.

## Next steps

* [Configure an LLM Proxy](configure-an-llm-proxy.md). Add guardrails, security plans, and policies.
* [Publish your LLM Proxy](../publish/publish-your-llm-proxy.md). Deploy the proxy and check consumer access.
