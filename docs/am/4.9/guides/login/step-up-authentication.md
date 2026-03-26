---
description: Overview of Authentication.
---

# Step-up Authentication

## Overview

Step-up authentication requires users to produce additional forms of authentication when they are already authenticated with the first set of credentials.

Step-up authentication uses multi-factor authentication (MFA) and can include any number of authentication methods, such as a one-time code over SMS, knowledge-based authentication (KBA), and biometrics.

{% hint style="info" %}
While both step-up authentication and MFA require users to produce multiple forms of authentication, each has a slightly different purpose:

* The purpose of MFA is to increase confidence in a user’s identity.
* The purpose of step-up authentication is to increase the level of security when needed: you can use it to implement an adaptive authentication scheme that seeks to find the best balance between the risk level of a request and the confidence level of the authentication.

Step-up authentication helps you ensure that users can access non-sensitive resources with a lower level of authentication while prompting them for additional credentials when they request access to sensitive resources.
{% endhint %}

### Example use cases

Step-up authentication is often used in the following scenarios:

* Users want to modify their password.
* Users initiate a payment.
* Users want to delegate access to third parties.
  1. Log in to AM Console.
  2. Select your application
  3. Click **Settings > Multifactor Auth**.
  4. Select your MFA factor and set the **Step up authentication** rule.
  5.  Click **SAVE**.

      <figure><img src="https://docs.gravitee.io/images/am/current/graviteeio-am-userguide-mfa-step-up.png" alt=""><figcaption><p>Application settings</p></figcaption></figure>

You can leverage access control by asking your users to confirm their identity before making any sensitive actions. In this example, the sensitive action is represented by the `pisp` (Payment Initiation Service Provider) OAuth 2.0 scope.

In order to use the API endpoints for payment initiation, an OAuth 2 access token must be presented to the API with scope `psip`. This is the standard flow defined by the PSD2 and Open Banking protocols. Payment initiation requires a **consent process** and a **strong customer authentication**.

{% hint style="info" %}
MFA step-up authentication is based on our execution context and can be triggered according to the incoming request, the user profile, and more.
{% endhint %}
