# Account Linking

## Overview

{% hint style="warning" %}
Account Linking is a Gravitee Enterprise Edition feature that is available in the default EE distribution. To learn more about Gravitee Enterprise and what's included in various enterprise packages:

* [Refer to the EE vs OSS documentation](../../overview/open-source-vs-enterprise-am/)
* [Book a demo](http://127.0.0.1:5000/o/8qli0UVuPJ39JJdq9ebZ/s/rYZ7tzkLjFVST6ex6Jid/)
* [Check out the pricing page](https://www.gravitee.io/pricing)
{% endhint %}

By default, Gravitee Access Management associates each user identity with a unique user account. For example, if a user first logs in against the Gravitee AM database and then via Google or Facebook, Gravitee AM determines that these logins were initiated by two different users.

A new user is prompted to provide identity attributes during account registration. The Account Linking feature automatically links user accounts from various identity providers to this primary account if the user attributes are identical. A user who is recognized and associated with an existing profile is allowed to authenticate from other accounts without having to re-enroll.

{% hint style="info" %}
When a user is linked to a primary account, it may be useful to access to the user information provided by the identity provider in expression language expressions. For doing so, the Access Management context give you access to the latest identiy information and to the list of all identities linked to the primary account. 

To directly have access to the information provided by the identity provider used by the user, you can use the `lastIdentityInformation` attribute.(ex `{#context.attributes['user']['lastIdentityInformation']['test-key']}`)

To access to information from a specific provider, you can use the `identitiesAsMap` attributes that will give you access to a map of object identified by the identity provider id. (ex `{#context.attributes['user']['identitiesAsMap']['a826b06e-9f55-42eb-a6b0-6e9f5502eb99']['additionalInformation']['test-key']}` )
{% endhint %}

## Activate Account Linking

The Account Linking feature can be activated at the application level or at the security domain level.&#x20;

### Link at the application level

To activate the Account Linking feature for a particular application:

1. In the AM Console, click on **Applications** in the left sidebar.
2. Select the application.
3. Click on **Design** in the inner left sidebar.
4. Select **Flows** from the page header tabs.
5. Click on the CONNECT flow.
6. Drag the Account Linking policy onto the CONNECT flow to add it.
7. Configure the CONNECT flow with the following options:&#x20;
   1. **Description:** Identify the flow step with a meaningful description.
   2. **Condition:** Execute the flow step if this condition is met (supports [Expression Language](../am-expression-language.md)).
   3. **Exit if no account:** Toggle ON to terminate the request if no account has been found.
   4. **Exit if multiple accounts found:** Toggle ON to terminate the request if multiple accounts have been found.
   5. **User attributes to find matching results:** Define which user attributes must match to enable the linking process.
      1. **Attribute name:** Username, email, etc.
      2. **Attribute value:** Supports Expression Language

<figure><img src="../../.gitbook/assets/account linking at app level.png" alt=""><figcaption><p>Apply account linking at the application level</p></figcaption></figure>

{% hint style="success" %}
Multiple accounts with the same attributes are now considered to represent the same user.
{% endhint %}

### Link at the security domain level

To activate the Account Linking feature for the security domain:

1. In the AM Console, click on **Settings** in the left sidebar.
2. Click on **Flows** in the inner left sidebar.
3. Select **Flows** from the page header tabs.
4. Click on the CONNECT flow.
5. Drag the Account Linking policy onto the CONNECT flow to add it.&#x20;
6. Configure the CONNECT flow with the following options:&#x20;
   1. **Description:** Identify the flow step with a meaningful description.
   2. **Condition:** Execute the flow step if this condition is met (supports [Expression Language](../am-expression-language.md)).
   3. **Exit if no account:** Toggle ON to terminate the request if no account has been found.
   4. **Exit if multiple accounts found:** Toggle ON to terminate the request if multiple accounts have been found.
   5. **User attributes to find matching results:** Define which user attributes must match to enable the linking process.
      1. **Attribute name:** Username, email, etc.
      2. **Attribute value:** Supports Expression Language

<figure><img src="../../.gitbook/assets/account linking_flows.png" alt=""><figcaption><p>Apply account linking at the security domain level</p></figcaption></figure>

{% hint style="success" %}
Multiple accounts with the same attributes are now considered to represent the same user.
{% endhint %}
