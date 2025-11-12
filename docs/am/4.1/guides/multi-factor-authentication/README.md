# Multi-factor Authentication

## Overview

Multi-factor authentication (MFA) provides a way to add additional steps during the login flow to enforce access control. This ensures that only valid users can access their accounts even if their credentials have been compromised.

It is split into 2 sections:

* **Enroll:** The end user inputs one or several **factors** that will allow them to secure their access.
* C**hallenge:** Once the enrollment step is done, the user challenges their configured factor in order to access their account.

## Enroll

Here is what the flow of the Multi-Factor authentication Enroll step looks like.

<figure><img src="https://docs.gravitee.io/images/am/current/graviteeio-am-userguide-mfa-enroll-flow.png" alt=""><figcaption><p>MFA enroll step</p></figcaption></figure>

The flow is pretty straightforward:

* We check first if we have factors configured in our application
* If so, we verify if the end-user has enrolled
* If not, we verify if they can skip Multi-Factor Authentication (not possible if enforced or if Step-Up is enabled)
* If the end user cannot or has not skipped the enroll process, we then proceed to display the enroll page with the available configured factors

## Challenge

Once the end-user has enrolled, we then proceed to the Challenge step.

<figure><img src="https://docs.gravitee.io/images/am/current/graviteeio-am-userguide-mfa-challenge-flow.png" alt=""><figcaption><p>MFA challenge step</p></figcaption></figure>

* As well as the enroll step, we primarily check if the application has factors.
* We then verify if the user has already challenged the factor
* If not we verify if the user can and has skipped Multi-Factor authentication

Having the 3 conditions above, the user then needs to challenge their factor in order to access their account.

{% hint style="info" %}
The first time the end user enrolled a factor implies to challenge at least once to activate their factor, regardless of your MFA configuration.
{% endhint %}

Prompt the MFA Challenge step to the end user will defer according to the following options you have enabled and configured on your application.

### Adaptive MFA

If [Adaptive MFA](docs/am/4.1/guides/login/adaptive-multi-factor-authentication.md) is active and the input rule **DOES NOT** match, the end user will be prompted the challenge page.

The evaluation takes precedence on Step-Up authentication and Remember Device

### Step Up Authentication

If [Step-Up Authentication](docs/am/4.1/guides/login/step-up-authentication.md) is active and the input rule **DOES** match while the end user is fully logged in (e.g.: logged in and challenged their factor after) the end user will be prompted to the challenge page.

The evaluation takes precedence on Remember Device

### Remember Device

If [Remember device](./#remember-device) is active and the user's device is not known, the end user will be prompted to the challenge page. They will also be presented to consent to register their device for a certain period of time which they can both refuse or accept. The latter option will save the device for a certain period of time which will be remembered at the next login, and skip the challenge page.

## Intelligent Adaptive Access

Intelligent Adaptive Access reinvents the way MFA is configured in AM. It allows you to configure Multi-Factor Authentication in a clearer way.

You can check out what’s new in Intelligent Adaptive Access [here](docs/am/4.1/guides/login/risk-based-mfa.md).
