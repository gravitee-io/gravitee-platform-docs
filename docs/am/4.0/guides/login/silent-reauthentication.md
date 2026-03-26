---
description: >-
  Overview of To lower authentication friction from third parties which can t
  maintain a session with Gravitee Access Management AM the use of the OpenID
  Connect ID Token let you request new tokens in a silent manner.
---

# Silent Reauthentication

To lower authentication friction from third parties which can’t maintain a session with Gravitee Access Management (AM), the use of the OpenID Connect ID Token let you request new tokens in a silent manner.

To trigger the silent re-authentication, your application must call the [authorization endpoint](https://github.com/gravitee-io/gravitee-platform-docs/tree/main/docs/am/4.0/guides/auth-protocols/oauth-2.0) with the following parameters :

* **id\_token\_hint**: ID Token previously issued by the Authorization Server being passed as a hint about the End-User’s current or past authenticated session with the application.
* **prompt**: Value must be `none` to disable interactive login flow.

If the ID token is valid, the end user will be (re)connected and AM will respond with an authorization code, otherwise `login_required` error will be sent to your application.

To enable silent re-authentication feature :

1. Log in to AM Console.
2. Select your application and click **Settings > General**.
3. Switch on **Silent re-authentication** and click **SAVE**.
