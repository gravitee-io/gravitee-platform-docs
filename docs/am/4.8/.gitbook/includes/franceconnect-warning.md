---
title: FranceConnect warning
---

{% hint style="danger" %}
When you register your application on the FranceConnect portal, v2 APIs require the declaration of the redirect URIs for login and for logout actions.&#x20;

* For the sign in redirect URL,  provide the /login/callback of your domain. For example, _`https://gateway.hostname/my-domain/login/callback` ._
* For the sign out redirect URL, provide the /logout/callback of your domain. For example, _`https://gateway.hostname/my-domain/logout/callback`_. Also, provide the /login/callback. For example, _`https://gateway.hostname/my-domain/login/callback` ._

**Why do I need to define the sign in redirect URI in the list of sign out URI ?**

The FranceConnect identity provider plugin proposes a "Session Management" option to specify the expected state of the FranceConnect session once the user is authenticated on AccessManagement.

If you are using the option "Session Management" with the value "Close session after user authentication", a logout is triggered on FranceConnect immediately after the user authentication. In this scenario, the `post_logout_redirect_uri` is set by AM to target the AM login callback to continue the authentication flow on AM.
{% endhint %}
