---
description: The complexity rules APIM applies to passwords for locally managed accounts, and how to change them.
---

# Password Policy

## Overview

APIM Console and the Developer Portal share a single user store, so one password policy covers both. The policy is a regular expression that the Management API applies whenever a user sets a password. Passwords are stored hashed with BCrypt.

{% hint style="info" %}
This policy applies only to accounts that APIM manages itself. Users who sign in through an external identity provider — OpenID Connect, LDAP, Gravitee Access Management, GitHub, or Google — have no password stored in APIM, so their provider's own policy applies instead. See [Authentication Providers](authentication-providers.md).
{% endhint %}

## Default policy

By default, a password must:

* Be between 12 and 128 characters long
* Contain at least one digit
* Contain at least one uppercase letter
* Contain at least one lowercase letter
* Contain no more than two identical characters in a row
* Contain at least one special character from the following set:

```
! ~ < > . , ; : _ = ? / * + - # " ' & § ` £ € % ° ( ) | [ ] $ ^ @
```

These rules are expressed as the following default pattern:

```
^(?=.*[0-9])(?=.*[A-Z])(?=.*[a-z])(?=.*[!~<>.,;:_=?/*+\-#\"'&§`£€%°()|\[\]$^@])(?!.*(.)\1{2,}).{12,128}$
```

## Where the policy is enforced

Validation runs server-side in the Management API. It applies when a user:

* Completes registration, whether they self-registered or an administrator pre-registered them
* Resets their password
* Accepts a group invitation

A password that does not match the pattern is rejected with an HTTP `400` response and the error code `passwordFormat.invalid`.

{% hint style="warning" %}
The sign-up form itself only checks that the password field is filled in and that both entries match. All complexity checking happens in the Management API, so a user sees the rejection only after submitting the form.
{% endhint %}

## Change the policy

Override `user.password.policy.pattern` with your own regular expression. Use the tab that matches your deployment method.

{% tabs %}
{% tab title="gravitee.yaml" %}
{% code title="gravitee.yml" %}
```yaml
user:
  password:
    policy:
      pattern: ^(?=.*[0-9])(?=.*[A-Z])(?=.*[a-z]).{16,128}$
```
{% endcode %}
{% endtab %}

{% tab title=".env" %}
```bash
gravitee_user_password_policy_pattern=^(?=.*[0-9])(?=.*[A-Z])(?=.*[a-z]).{16,128}$
```
{% endtab %}

{% tab title="Helm values.yaml" %}
The APIM Helm chart passes the `api.user.password` block straight through to the Management API `gravitee.yml`:

```yaml
api:
  user:
    password:
      policy:
        pattern: ^(?=.*[0-9])(?=.*[A-Z])(?=.*[a-z]).{16,128}$
```
{% endtab %}
{% endtabs %}

The new pattern takes effect after you restart the Management API. It applies only to passwords set from that point onward; existing passwords are not re-validated.

{% hint style="warning" %}
The default policy follows OWASP recommendations. Gravitee strongly recommends against reducing its complexity, particularly if you allow users to self-register. See [Production best practices](../../../prepare-a-production-environment/production-best-practices/authentication.md).
{% endhint %}

{% hint style="info" %}
A `user.password.policy.description` property also appears alongside `pattern` in the shipped `gravitee.yml`, with a comment stating that it is shown to users whose password does not match the policy. No APIM component reads this property, so setting it has no effect. Only `pattern` is applied.
{% endhint %}
