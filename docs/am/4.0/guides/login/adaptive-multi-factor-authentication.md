---
description: Overview of Adaptive.
---

# Adaptive Multi-factor Authentication

## Overview

Adaptive multi-factor authentication (A-MFA) requires users to produce additional forms of authentication after the login step.

When A-MFA is enabled, it allows the user to skip MFA, based on the following trusted information:

* The IP of the user.
* The number of times the user has logged in.
* The content of the request.

### Example use cases

A-MFA is often used in the following scenarios:

* A user fails to log in three times and succeeds on the fourth attempt.
* A user tries to log in from a different location (such as country, continent, or region).

You can use A-MFA in both cases to prevent account security breaches.

{% hint style="info" %}
To apply location rules, you must first install plugin [`gravitee-service-geoip`](https://download.gravitee.io/#plugins/services/gravitee-service-geoip/). This plugin loads the `geoip` databases in memory, so you need to adjust the JVM Heap settings of your AM Gateways accordingly.

The Gravitee Geoip Plugin uses MaxMind, make sure your AM instance is well provisioned in terms of resources.
{% endhint %}

## Configure A-MFA

1. In AM Console, select your application.
2. Click the **Settings** tab, then click **Multifactor Auth**.
3. Set the **Adaptive MFA** rule.
4. Click **SAVE**.

<figure><img src="https://docs.gravitee.io/images/am/current/graviteeio-am-userguide-mfa-adaptive-mfa-rule.png" alt=""><figcaption><p>Configuring A-MFA</p></figcaption></figure>
