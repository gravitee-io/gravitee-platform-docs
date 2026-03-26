---
description: Overview of Access Tokens.
---

# Add Custom Claims to Tokens

## Overview

You can add custom claims to your Access Tokens or ID Tokens.

## Configure a custom claim

1. Log in to AM Console.
2. Click **Applications**, then select an application.
3. In the **Settings** tab, click **OAuth 2.0 / OIDC**.
4. Scroll down to the **Custom claims** section.
5.  Configure details of the custom claim and click **SAVE**.

    You can now request your tokens to retrieve your custom claims.

    <figure><img src="https://docs.gravitee.io/images/am/current/graviteeio-am-quickstart-tokens-custom-claims.png" alt=""><figcaption><p>Custom claims</p></figcaption></figure>

{% hint style="info" %}
The mapping here uses the Gravitee Expression Language to dynamically add custom data. You can also use raw values to add more static information.
{% endhint %}

<figure><img src="https://docs.gravitee.io/images/am/current/graviteeio-am-quickstart-tokens-custom-claims-info.png" alt=""><figcaption><p>Create a claim</p></figcaption></figure>

To retrieve claims from the User Profile, use the following Gravitee Expression Language formats:

\
`{#context.attributes['user']['claims']['preferred_username']}` for attributes under the `additionalInformation` dict

\
\- or -

\
`{#context.attributes['user']['roles']}` for the `roles` attribute (array)

\
\- or -

\
`{#context.attributes['user']['username']}` for the `username` attribute.\\
