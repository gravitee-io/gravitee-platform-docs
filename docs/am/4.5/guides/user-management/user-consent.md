# User Consent

## User consent

As described in [RFC 6819](https://tools.ietf.org/html/rfc6819#section-5.1.3), users should always be in control of authorization processes and have the necessary information to make informed decisions.

If you want users to acknowledge and accept that they are giving an app access to their data, you can configure AM to display a consent page during the OAuth 2.0/OIDC authentication flow.

{% hint style="info" %}
You can change the look and feel of the user consent form. See [custom pages](../branding/#custom-pages) for more information.
{% endhint %}

## Revoke user consent

You can view a list of applications for which each user has provided consent. To revoke access to an application:

1. Log in to AM Console.
2. Click **Settings > Users**.
3.  Select the user and in the **Authorized Apps** tab, revoke the application.

    <figure><img src="https://docs.gravitee.io/images/am/current/graviteeio-am-userguide-um-consent.png" alt=""><figcaption><p>Revoke user's authorized applications</p></figcaption></figure>

{% hint style="info" %}
Revoking consent can also be done via the [AM Management API](docs/am/4.5/reference/am-api-reference.md).
{% endhint %}
