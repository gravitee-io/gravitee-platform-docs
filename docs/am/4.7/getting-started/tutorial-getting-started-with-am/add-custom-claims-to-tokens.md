# Add Custom Claims to Tokens

## Overview

You can add custom claims to your Access Tokens or ID Tokens.

## Configure a custom claim

1. Log in to AM Console.
2. Click **Applications**, and then select an application.
3. In the **Settings** tab, click **OAuth 2.0 / OIDC**.
4. Navigate to the **Custom claims** section.
5.  Configure details of the custom claim, and then click **SAVE**.

    You can now request your tokens to retrieve your custom claims.

    <figure><img src="https://docs.gravitee.io/images/am/current/graviteeio-am-quickstart-tokens-custom-claims.png" alt=""><figcaption><p>Custom claims</p></figcaption></figure>

{% hint style="info" %}
The mapping here uses the Gravitee Expression Language to dynamically add custom data. To add more static information, you can also use raw values .
{% endhint %}

<figure><img src="https://docs.gravitee.io/images/am/current/graviteeio-am-quickstart-tokens-custom-claims-info.png" alt=""><figcaption><p>Create a claim</p></figcaption></figure>

To retrieve claims from the User Profile, use the following Gravitee Expression Language formats:

`{#context.attributes['user']['claims']['preferred_username']}` for attributes under the `additionalInformation` dict

\- or -

`{#context.attributes['user']['roles']}` for the `roles` attribute (array)

\- or -

`{#context.attributes['user']['username']}` for the `username` attribute.

{% hint style="info" %}
In the token the custom claims accept any kind of value types, it may a String, a numeric or even an Object or an Array. For example, if your user profile contains an address attribute which is an object, there is no issue to provide this object as value for a claim.&#x20;
{% endhint %}

To convert a list of elements from a String to a Array, you can use Expression Language to manipulate the String value. As an example, if a string contains a list of values separated by a coma, the conversion could be:

`{(T(java.lang.String).valueOf("value1, value2")).split(",")}`
