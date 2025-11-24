---
description: Configuration guide for Configure.
---

# Configure a Flow

## Overview

You can use flows to extend AM’s standard functionality.

This section walks you through using flows to enhance the information displayed in the [End user agreement](../../guides/user-management/user-consent.md) by calling a remote service before rendering the HTML page. The example in this section uses the Gravitee Echo API.

For more information about flows, see [Flows](../../guides/flows.md) in the User Guide.

{% hint style="info" %}
AM flows are available from version 3.5 and replace extension points.
{% endhint %}

## Before you begin

You must [set up your first application](set-up-your-first-application.md) before performing these steps.

### Use the HTTP Callout Policy

{% hint style="info" %}
In this example, we will retrieve the username from the execution context `{#context.attributes['user'].username}` and pass it to our remote service which responds with new information **X-Custom-Variable** (`{#jsonPath(#calloutResponse.content, '$.headers.X-Custom-Header')}`). We will be using this **X-Custom-Variable** in the End User consent HTML page.
{% endhint %}

1. Log in to AM Console.
2. Click **Settings > Flows**.
3. Select the **CONSENT** flow and drag the **HTTP Callout** policy to the **Pre Consent** step.
4.  Give your policy a **Name** and the following configuration:

    * HTTP Method: `GET`
    * URL: [`https://api.gravitee.io/echo`](https://api.gravitee.io/echo)
    * Header: **Name** — `X-Custom-Header` **Value** — `{#context.attributes['user'].username}`
    * Variable: **Name** — `X-Custom-Variable` **Value** — `{#jsonPath(#calloutResponse.content, '$.headers.X-Custom-Header')}`

    <figure><img src="https://docs.gravitee.io/images/am/current/graviteeio-am-quickstart-policies.png" alt=""><figcaption><p>Policy Studio</p></figcaption></figure>

{% code overflow="wrap" %}
```
  ],
  "post":[

  ],
  "enabled":true,
  "type":"root"
```
{% endcode %}
