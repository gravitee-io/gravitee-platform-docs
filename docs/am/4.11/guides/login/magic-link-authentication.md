## Overview

Magic Link Authentication enables passwordless login by sending users a time-limited authentication link using email. When users click the link, they are authenticated without entering a password. This feature is designed for API administrators configuring authentication flows and developers integrating passwordless login into applications.

The Magic Link authentication method follows the following challenge-response flow:
1. The user attempts to access a protected application.
2. The application redirects the user to Access Management (AM) for authentication.
3. AM presents a login page with the **Email Magic Link** option.
4. The user enters their username. For example, their email address or login identifier.
5. AM searches for the user's registered email in the associated user directory, and then sends a magic link to that address.
6. The user clicks the link in the their inbox, or the user pastes the link into their browser.
7. AM validates the link, establishes the session, and then redirects the user back to the application.

The magic link is **single-use** and **time-limited**. If you click the link or the link expires, you cannot use that link again.

{% hint style="info" %}
For the best security posture, open the magic link in the same browser where authentication was initiated. AM binds the link to the originating session. If the link is opened in a different browser or device, AM rejects it and prompts the user to request a new magic link.
{% endhint %}

### Key concepts

#### Magic Link Token

A JWT token embedded in the authentication email link. The token includes standard claims (issuer, subject, audience, expiration, issued-at and session_id claim). Tokens expire after 15 minutes by default.

#### Email Template System

Magic Link authentication requires two templates: an email template (`MAGIC_LINK`) containing the authentication link, and a form template (`MAGIC_LINK_LOGIN`) where users enter their email address. Both templates are available only when Magic Link authentication is enabled in login settings.

#### Audit Event Type

Successful Magic Link authentications generate a `USER_MAGIC_LINK_LOGIN` audit event. Analytics support includes a `magic_link` field type for reporting and filtering authentication events.

## Prerequisites

Before configuring Magic Link authentication, ensure the following requirements are met:

* Email service configured and operational
* User accounts with valid email addresses
* Domain or application login settings accessible for configuration

## Install the gravitee-am-authenticator-magiclink plugin

By default, the enterprise plugin [gravitee-am-authenticator-magiclink`](https://download.gravitee.io/#graviteeio-ee/am/plugins/authenticator/magic-link//gravitee-am-authenticator-magiclink/). When the plugin loads successfully, the following entry appears in the server's standard output:

```bash
INFO  i.g.p.c.internal.PluginRegistryImpl - 	> magiclink-am-authenticator [1.0.0] has been loaded
...
INFO  i.g.a.p.a.p.AuthenticatorPluginHandler - Plugin 'magiclink-am-authenticator' installed.
```

## Gateway configuration

### Email service properties

Configure the following properties to control Magic Link email behavior:

| Property | Description | Default |
|:---------|:------------|:--------|
| `user.magic.link.login.email.subject` | Subject line for magic link emails | `"Sign in"` |
| `user.magic.link.login.time.value` | Token expiration time value | `15` |
| `user.magic.link.login.time.unit` | Token expiration time unit | `MINUTES` |

### Login settings

| Property | Description | Default |
|:---------|:------------|:--------|
| `magicLinkAuthEnabled` | Enable or disable Magic Link authentication | `false` |

## Enable Magic Link authentication

You can enable MagicLink in either of the following locations:
* [Enable Magic Link for all applications in a domain](#enable-magic-link-for-all-applications-in-a-domain)
* [Enable Magic Link for a specific application](#enable-magic-link-for-a-specific-application)

### Enable Magic Link for all applications in a domain
1. Sign in to the AM Console 
2. Navigate to **Settings**, and then select **Login**.
3. In the **Passwordless** section, enable **Passwordless Magic Link Authentication**.

### Enable Magic Link for a specific application

1. Sign in to the AM COnsole
2. Navigate to **Applications**, and then select the application that you want to enable the Magic Link for.
3. Navigate to **Settings**, and then select the **login** tab.
4. Disable the **Inherit configuartion**.
5. In the **Passwordless** section, enable **Passwordless Magic Link Authentication**.

## User authentication flow

Users authenticate with Magic Link using the following process:

1. On the AM login page, there is a **Sign in with Magic Link** button.
2. The user is redirected to the Magic Link page.
3. The user enters their email address, and then clicks next.
4. The user clicks the link in the email.
5. The user is redirected to the application.

## Configure the email template
The configure the email template, the template is eitable like other emails. The Magic Link URL is available through the `url` variable.
```bash
<a href="${url}">
```
