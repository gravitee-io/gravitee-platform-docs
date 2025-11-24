# Configure MFA for an Application

## Overview

Multi-factor authentication behaviour is configured on application level in Access Management. MFA is mainly split into two components, enrollment and challenge.

Gravitee Access Management MFA is built to let you tailor exactly which factor each user type should be able to use, and if the user should be proposed enroll a factor or forced to always be challenged for each login.

Note that not all sections are mandatory to fulfill a successful MFA rollout to your users.

Each section is complemented with a flow chart showing the sections part in the overall MFA flow evaluation.

## Section 1 - Factors

The first step is to enable factors. This section allows you to control which factors that are enabled for the application, which users that should use each factor, and lastly which factor that should be default factor for users.

<figure><img src="../../../4.3/.gitbook/assets/conf mfa 1.png" alt="" width="375"><figcaption><p>Flow chart for evaluating enabled factors, selection rules and default factor.</p></figcaption></figure>

### Enable factors

The first step to set up MFA is to choose which factors the application should use.

{% hint style="info" %}
If you have not already created at least one factor, visit Security Domain settings to create one. ([Managing Factors](managing-factors/README.md))
{% endhint %}

1.  Click on **Select Factors**

    <figure><img src="../../../4.3/.gitbook/assets/conf mfa 2.png" alt=""><figcaption></figcaption></figure>
2.  Select one to many factors, then click **Add Selected**

    <figure><img src="../../../4.3/.gitbook/assets/conf mfa 3.png" alt=""><figcaption></figcaption></figure>
3.  You should now have the selected factors enabled for the application

    <figure><img src="../../../4.3/.gitbook/assets/conf mfa 4.png" alt=""><figcaption></figcaption></figure>

### Selection rules

If you want to control which factor users can use, you can leverage the factor Selection Rules.

For example, maybe you run a global service and offer national identity MFA methods to your users. By settings selections rules for factors, users will only see the factors they actually can use. This enhances UX for the end users.

The selection rule supports Expression Language (EL) and allows you to make decisions based on the end users profile attributes.

1.  Click on Selection Rule icon for one factor

    <figure><img src="../../../4.3/.gitbook/assets/conf mfa 5.png" alt=""><figcaption></figcaption></figure>
2.  Add a Selection Rule and click on **Save**

    <figure><img src="../../../4.3/.gitbook/assets/conf mfa 6.png" alt=""><figcaption></figcaption></figure>
3.  Only users matching the Selection Rule will be able to enroll using the factor

    <figure><img src="../../../4.3/.gitbook/assets/conf mfa 7.png" alt=""><figcaption></figcaption></figure>

### Default factor

Adding Selection Rules to factor may lead to an inconvenient situation where one user may not match any Selection Rule.

To remediate this risk, there is a concept of a Default factor. This factor will be available for all users that does not meet any configured Selection Rule.

Default factor is managed by choosing the factor with a radio button.

<figure><img src="../../../4.3/.gitbook/assets/conf mfa 7.png" alt=""><figcaption></figcaption></figure>

## Section 2 - MFA enrollment

MFA enrollment is the concept of associating a multi-factor authenticator to a users profile in Access Management. For example, setting up email MFA, or creating a one-time-password entry in your OTP authenticator application.

An enrollment always requires the user to be challenged the first time to collect the factor. However if the users should be challenged each following login completely depends on [MFA challenge](configure-mfa-for-an-application.md#mfa-challenge) configuration.

Gravitee Access Management lets you configure the MFA enrollment step using three different ways: Optional, Required, or Conditional enrollment.

<figure><img src="../../../4.3/.gitbook/assets/conf mfa 9.png" alt=""><figcaption><p>Flow chart for how different components of MFA enrollment flow is evaluated.</p></figcaption></figure>

### Optional enrollment

With optional enrollments users will be given the option to enroll with MFA when signing in. You can specify the period of time during which enrollment can be skipped. Once the timer has ended, users will be asked to enroll.

<figure><img src="../../../4.3/.gitbook/assets/conf mfa 10.png" alt=""><figcaption></figcaption></figure>

### Required enrollment

With required enrollment, all users will be required to enroll with MFA during sign in.

<figure><img src="../../../4.3/.gitbook/assets/conf mfa 11.png" alt=""><figcaption></figcaption></figure>

### Conditional enrollment

With conditional enrollment, you will be able to control which users that should or should not be forced to enroll with MFA. This is done by writing Conditional Rules with Expression Language (EL).

<figure><img src="../../../4.3/.gitbook/assets/conf mfa 12.png" alt=""><figcaption></figcaption></figure>

#### Allow users to skip Conditional enrollment (Extra flexibility)

You may use conditional enrollment in combination with optional enrollment. This is done by enabling Allow users to skip Conditional Enrollment toggle. You may then add an additional rule that allows some users to skip MFA enrollment for some time even if the matched the first conditional rule.

<figure><img src="../../../4.3/.gitbook/assets/conf mfa 13.png" alt=""><figcaption></figcaption></figure>

## Section 3 - MFA challenge

MFA challenge is the concept of leveraging the enrolled factor to challenge the user to use it as part of the sign in flow.

Gravitee Access Management lets you tailor the challenge experience so you can have the balanced approach between security and UX. This is done by using three different ways: Risk-based, Required, or Conditional MFA challenge.

<figure><img src="../../../4.3/.gitbook/assets/conf mfa 14.png" alt=""><figcaption><p>Flow chart for how different components of MFA enrollment flow is evaluated.</p></figcaption></figure>

### Risk-based challenge

Risk-based MFA challenge lets you leverage known data points and the end users behavior to determine confidence on users identity and if the user should be challenged with MFA.

This is determined by setting thresholds for three different risk assessments.

* Associated devices determined if the user's device is known or not.
* IP Reputation Score compares the users IP against a malicious IPs.
* Geolocation Velocity will calculate the speed end user has travelled between sign in A and B. This to determined impossible traveling and hence unlikeliness of being the same end user.

<figure><img src="../../../4.3/.gitbook/assets/conf mfa 15.png" alt=""><figcaption></figcaption></figure>

### Required challenge

With required enrollment, all users will be required to enroll with MFA during sign in.

<figure><img src="../../../4.3/.gitbook/assets/conf mfa 16.png" alt=""><figcaption></figcaption></figure>

### Conditional challenge

With conditional challenge, you will be able to control which users that should or should not be forced to be challenged with MFA. This is done by writing Conditional Rules with Expression Language (EL).

<figure><img src="../../../4.3/.gitbook/assets/conf mfa 17.png" alt=""><figcaption></figcaption></figure>

## Section 4 - Remember device

If Remember device is active and the user's device is not known, the end user will be prompted to the challenge page. They will also be presented to consent to register their device for a certain period of time which they can both refuse or accept. The latter option will save the device for a certain period of time which will be remembered at the next login, and skip the challenge page. Please refer to flow chart for MFA Challenge to see how Remember device is being evaluated.

Remember device also require you to configure a [Device Identifier](../device-identifier.md) on the Security Domain.

<figure><img src="../../../4.3/.gitbook/assets/conf mfa 18.png" alt=""><figcaption></figcaption></figure>

## Section 5 - Step-up authentication

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
5. Click **SAVE**.

<figure><img src="../../../4.3/.gitbook/assets/conf mfa 19.png" alt=""><figcaption></figcaption></figure>

You can leverage access control by asking your users to confirm their identity before making any sensitive actions. In this example, the sensitive action is represented by the `pisp` (Payment Initiation Service Provider) OAuth 2.0 scope.

In order to use the API endpoints for payment initiation, an OAuth 2 access token must be presented to the API with scope `psip`. This is the standard flow defined by the PSD2 and Open Banking protocols. Payment initiation requires a **consent process** and a **strong customer authentication**.

{% hint style="info" %}
MFA step-up authentication is based on our execution context and can be triggered according to the incoming request, the user profile, and more.
{% endhint %}
