# Session Management

## Overview

When a user is signing in, AM stores the fact that the user is authenticated for a certain period of time in what we call an **HTTP Session**.

This mechanism avoids the need for the user to re-authenticate every time he wants to perform some actions. The same principle applies to your application or when you use an external identity provider such as Facebook, Twitter, etc.

{% hint style="info" %}
By default the session last 30 minutes, you can change this value via the gravitee.yml of the gateway, see [configuration section.](../getting-started/configuration/configure-am-gateway/README.md)
{% endhint %}

### Session layers

There are three-session layers you need to consider when you want to sign-out your users:

1. **Application session**: This layer lies in your application after your users have been authenticated from AM. For traditional web applications, this session is stored via HTTP cookies (JSESSIONID, PHPSESSID, ASP.NET\_SessionId). For SPA applications this information can be stored in memory or via storage. It’s up to you to clean everything if you want to log out your users.
2. **GraviteeAM session**: A session is created for every authenticated user and this information is inside an HTTP cookie. This cookie acts as Single Sign-on (SSO) cookie and lets you remember your users and automatically silently authenticate your users across applications.

{% hint style="info" %}
To automatically authenticate your user across applications (SSO), your applications must share the same identity provider.
{% endhint %}

3. **Identity Provider session**: If your application is configured to use a [social identity provider](identity-providers/social-identity-providers/README.md) to authenticate a user, the identity provider will create a session in addition to the AM one. When users attempt to sign in with any of these providers and they are already signed into the provider, they will not be prompted again to sign in.

### Invalidate session

For the application session layer, it is up to you to clean everything if you want to log out your users.

For the AM and identity provider sessions, you can read the logout section below to learn how to invalidate them.

## Logout

### Invalidate session

Authenticated users who want to invalidate their session can call the following URL: `https://AM_GATEWAY_HOST/{domain}/logout`.

{% hint style="info" %}
By default, access tokens and refresh tokens are not revoked. You can add the `invalidate_tokens=true` query parameter to the request to invalidate current user tokens.
{% endhint %}

### Redirect users after logout

You can specify the `post_logout_redirect_uri=http://myApp/logoutCallback` or `target_url=http://myApp/logoutCallback` query parameter to redirect the user to your application after logout.

{% hint style="info" %}
You can define a signedlist of allowed URLs where the user will be redirected after being sign out. It prevents some vulnerabilities like being redirected to unsafe websites.
{% endhint %}

### Single logout

Single logout lets your end users sign out of both their Gravitee AM session and the social identity provider (configured in your application) with a single action.

To enable the single logout feature :

1. Log in to AM Console.
2. Select your application and click **Settings > General**.
3. Switch on **Single Sign Out** and click **SAVE**.

Call the default logout endpoint and your users will be logout at both places.

#### Limitations

Currently, only the following identity providers are compatible with the Single Sign Out feature :

* Certified OpenID Connect provider
* Azure AD
