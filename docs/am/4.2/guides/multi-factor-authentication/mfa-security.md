# MFA Security

## Overview

Gravitee Access Management (AM) enhances MFA security further by introducing three new security features - an MFA Challenge policy, MFA Rate Limit, and Brute Force Detection. This new functionality is designed to make the multi-factor authentication process more resilient to bad actor attacks. The new features enable you to:

* Add an MFA step to account actions to protect a user account.
* Specify the maximum number of MFA challenges the application can request to obtain SMS or Email verification code.
* Enforce the maximum attempts of MFA code verification.

## MFA Challenge policy

The MFA Challenge policy is an [Enterprise Edition](../../overview/open-source-vs-enterprise-am/README.md) policy plugin. It allows a security domain or application owner to apply an MFA step during password reset or account unlock, etc., to enforce security and ensure that the user account has not been compromised. You can specify which MFA Factor will be used to do the challenge step.

For example, consider an end user who wants to reset their password. After clicking on the RESET PASSWORD email link, the user must complete the form on the MFA Challenge page before their password can be changed.

<figure><img src="../../.gitbook/assets/mfa challenge policy.png" alt=""><figcaption><p>Password reset triggers MFA Challenge</p></figcaption></figure>

## MFA Rate Limit

The MFA Rate Limit feature enables you to configure and limit the number of challenges a user is allowed to send within a specific time period. This could be useful when managing factors (such as SMS or email) that could incur unwanted costs due to the nature of the services involved, or factors that can only provide a limited number of available requests within a certain time period.

The rate limit configuration is available in the `gravitee.yaml` file of the AM Gateway under the `mfa_rate` section. The configuration is disabled by default. The code example below shows an enabled sample configuration, which is self-explanatory. The `timeUnit` value could be `Hours`, `Minutes`, or `Seconds`.

```yaml
mfa_rate:
  enabled: true
  limit: 5
  timePeriod: 15
  timeUnit: Minutes
```

You can define these properties in the `values.yaml` file of the AM Helm Chart as well.

```yaml
gateway:
  mfa_rate:
    enabled: true
    limit: 5
    timePeriod: 15
    timeUnit: Minutes
```

Gravitee AM monitors the MFA challenge request based on the enabled rate limit configuration.

If a user exceeds the rate limit, a "user rate limit exceeded" message is shown and the user must wait for a certain amount of time before making a new successful request. For example, if the rate limit is set to 2 for a 1-minute time period and the user has already sent 2 requests, the user must wait for another 30 seconds before being able to send another request. The screenshot below shows the challenge step with an exhausted rate limit:

<figure><img src="https://docs.gravitee.io/images/am/current/graviteeio-am-userguide-mfa-ratelimit-exceed.png" alt=""><figcaption><p>Rate limit exceeded UI</p></figcaption></figure>

{% hint style="info" %}
You can customize the error message by modifying the value of the `mfa_challenge.rate.limit.error` property in the **messages\_en.properties** or **messages\_fr.properties** file.
{% endhint %}

## Brute Force Detection

The Brute Force Detection feature enables you to configure and limit the number of verification requests a user is allowed to send within a specific time period. You can configure Brute Force Detection at domain level or at application level. Follow the steps below to configure the **Brute Force** feature at domain level.

1. Log in to the AM Console.
2. Select **User Accounts** under **SECURITY**.
3. Enable **Brute Force Detection** in the **MFA** section.
4.  Define your **Brute Force Detection** preferences.

    <figure><img src="https://docs.gravitee.io/images/am/current/graviteeio-am-userguide-mfa-security.png" alt=""><figcaption><p>Brute force detection preferences</p></figcaption></figure>

Once the number of maximum attempts is reached, the user will be notified with an error message.

<figure><img src="https://docs.gravitee.io/images/am/current/graviteeio-am-userguide-mfa-brute-max.png" alt=""><figcaption><p>Brute force error message</p></figcaption></figure>

A new log event, `MFA_VERIFY_LIMIT_EXCEED`, is available to log brute force attempts.

{% hint style="info" %}
You can override domain-level Brute Force Detection settings at the application level from **App > Settings > accounts**. To customize the error message, modify the value of the `mfa_challenge.verify.limit.error` property in the **messages\_en.properties** or **messages\_fr.properties** file.
{% endhint %}
