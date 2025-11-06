---
description: >-
  These configuration settings and recommendations are critical to the security
  of your production environment
---

# Production Best Practices

## Overview

The default settings created during APIM installation can be useful for testing your new instance. However, some may not be suitable for a production environment, where security is more of a consideration. This guide highlights the APIM settings that require special attention when migrating to a production environment.&#x20;

## Security checklist

The following high-level checklist links to the details of how and why you would enforce each list item.&#x20;

{% hint style="info" %}
The objective is not to apply all of the recommendations, but to ensure that all configurations have been made with caution.
{% endhint %}

<details>

<summary>Security checklist</summary>

1. Internal APIs

* [ ] [Disable or enforce the security of the internal API](internal-apis.md)

2. Deployment

* [ ] [Review the exposition of the console and developer portal to the outside world](deployments.md#console-and-portal-apis)
* [ ] [Ensure the console and developer portal rest APIs are accessible through HTTPS](deployments.md#enable-https)

3. Authentication

* [ ] [Configure authentication using an identity provider](authentication.md#identity-providers)
* [ ] [Enable authentication to access the Developer Portal](authentication.md#developer-portal-authentication)
* [ ] [Remove all the default users](authentication.md#default-users)
* [ ] [Remove the admin user or enforce the admin user password](authentication.md#admin-user)
* [ ] [Disable user self-registration for bot console and portal](authentication.md#user-self-registration)
* [ ] [Disable auto-validation of self-registered users (if self-registration is enabled)](authentication.md#user-self-registration)
* [ ] [Change the user session signing secret and validity duration](authentication.md#user-session)
* [ ] [Disable default application creation](authentication.md#other-user-options)
* [ ] [Set the registration link validity to 1 day](authentication.md#other-user-options)
* [ ] [Change the user reference secret](authentication.md#other-user-options)

4. Brute-force and browser protection

* [ ] [Configure brute force protection](protections.md#brute-force-protection) ([ReCaptcha](protections.md#recaptcha) or [Fail2ban](protections.md#fail2ban))
* [ ] [Enable CSRF protection](protections.md#enable-csrf-protection)
* [ ] [Configure CORS for Console and Portal REST APIs](protections.md#configure-cors)

5. Configuration settings

* [ ] [Change the property encryption secret](general-recommendations/property-encryption.md#property-encryption)
* [ ] [Enable documentation page sanitizer](general-recommendations/documentation-sanitizer.md#documentation-sanitizer)
* [ ] [Disable Webhook notifier or configure an authorized list of URLs](general-recommendations/notifiers.md#notifiers)

6. APIM best practices

* [ ] [Apply best practices when designing and deploying APIs](general-recommendations/api-design.md#api-design)

</details>

{% hint style="warning" %}
**Configuring APIM**

APIM includes many other configuration options and every environment is unique. However you configure new settings (via the `gravitee.yml` file, APIM Console, or environment and system variables) it is important to understand that one configuration type can override another.
{% endhint %}
