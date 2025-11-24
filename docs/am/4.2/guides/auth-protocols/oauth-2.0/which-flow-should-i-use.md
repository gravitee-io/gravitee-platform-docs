---
description: Overview of Which Flow Should.
---

# Which Flow Should I Use?

Deciding which OAuth 2.0 flow to use depends mainly on the type of client the end user will be using and the level of trust between AM authorization server and your clients.

{% hint style="info" %}
An OAuth 2.0 client is an application (such as web, mobile or native) requesting access to a protected resource (API) on behalf of the resource owner (end user).
{% endhint %}

## Client acts on its own (machine-to-machine)

If the party requested for access does not involve an end user, for example a batch program or an API calling another API, the flow to use is the [client credentials grant type.](./#client-credentials)

## Client is a web application with a backend server

If the party requested for access is a web app running on server (such as an Java, PHP or .NET app), the[ authorization code](./#authorization-code) grant type is the best match. With this kind of application, the access and refresh tokens can be securely stored without risking exposure.

## Client is running on a web browser (single-age app or SPA)

If the party requested for access is an SPA (such as an Angular, React or Vue app) the recommended option is to use the [authorization code ](./#authorization-code)grant type with the [PKCE](proof-key-for-code-exchange-pkce.md) extension.

{% hint style="info" %}
The [implicit](./#implicit) grant type was previously used for SPA applications but has been deprecated for security reasons.
{% endhint %}

## Client is a mobile/native application

If the party requested for access is a mobile or native application, the [authorization code](./#authorization-code) grant type with the [PKCE](proof-key-for-code-exchange-pkce.md) extension is your best option.

## Client is highly trustable

If the party requested for access is able to use the [authorization code](./#authorization-code) grant type and deal with HTTP browser redirection, the end user will need to set their credentials in the client application and the client will send this information to the AM server.

{% hint style="info" %}
Due to the fact that user credentials are propagated between the client and AM, you need to ensure that there is a highly trusted communication level between those parties.
{% endhint %}

## Your APIs are accessed by third parties

If a partner or third party wants to access your protected resources (APIs) which are secured by AM server, it’s possible to ask your partners to exchange their own tokens for AM tokens. You can use the [JWT Bearer](extension-grants.md) grant type for this purpose.
