---
description: >-
  Allow browsers on other origins to call your API by configuring
  cross-origin resource sharing.
hidden: false
noIndex: false
---

# Configure CORS

The **CORS** page configures cross-origin access for this API. When CORS is enabled, the gateway adds `Access-Control-*` headers to responses and short-circuits preflight requests.

To open the page, follow these steps:

1. Click **API Proxies** in the module sidebar.
2. Select your API proxy.
3. Click **CORS** in the API proxy sidebar.

Changing any setting reveals the **Discard** and **Save changes** buttons.

<!-- TODO: Screenshot of the CORS page -->

<figure><img src="../../../.gitbook/assets/PLACEHOLDER-gamma-api-cors-page.png" alt=""><figcaption><p>The CORS page</p></figcaption></figure>

## Enable CORS

Turn on the **Enable CORS** switch. The remaining fields stay disabled until CORS is enabled.

## Set origins, methods, and headers

The **Origins, methods and headers** card carries the following fields. Use `*` to allow any value. Regular expressions are supported for origins.

| Field                              | Description                                                                              |
| ---------------------------------- | ---------------------------------------------------------------------------------------- |
| **Access-Control-Allow-Origin**    | Origins that may call this API. Scheme, domain, and port must match.                     |
| **Access-Control-Allow-Methods**   | HTTP methods that may be used in cross-origin requests.                                  |
| **Access-Control-Allow-Headers**   | Headers the client is allowed to send in the actual request.                             |
| **Access-Control-Expose-Headers**  | Headers from the response that the browser is allowed to surface to JavaScript.          |

{% hint style="warning" %}
Setting `*` as the allowed origin exposes this API to any website. The page shows the **Allowing all origins** warning, which reminds you to make sure authentication is enforced.
{% endhint %}

## Adjust the advanced settings

The **Advanced settings** card fine-tunes credentials handling, preflight cache duration, and how policies are evaluated:

* **Access-Control-Allow-Credentials**. Allow browsers to include cookies and HTTP authentication. Not compatible with `*` as the allowed origin.
* **Run policies on preflight**. By default, preflight `OPTIONS` requests bypass policies. Enable this toggle to enforce authentication or rate limiting on preflight requests too.
* **Max age (seconds)**. How long the browser may cache the preflight response. Use `-1` to disable caching.

## Verification

To verify CORS is working as expected, follow these steps:

1. Enable CORS, add an origin, and add the `GET` method.
2. Click **Save changes** and deploy the API.
3. Send a preflight request with `curl -X OPTIONS -H "Origin: <your-origin>" -H "Access-Control-Request-Method: GET" <your-api-url>`. The response carries the `Access-Control-Allow-Origin` header.

<!-- TODO: Screenshot of a preflight response with Access-Control headers -->

<figure><img src="../../../.gitbook/assets/PLACEHOLDER-gamma-api-cors-preflight.png" alt=""><figcaption><p>A preflight response with CORS headers</p></figcaption></figure>
