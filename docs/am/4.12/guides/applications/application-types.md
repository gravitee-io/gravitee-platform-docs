# Application types

## Overview

*Applications* act on behalf of the user to request tokens, hold user identity information, and retrieve protected resources from remote services and APIs.

Application definitions apply at the *security domain* level.

AM supports multiple application types, including a specialized **AGENT** type for AI agents and autonomous services. Agent applications are managed separately from the Applications area and have distinct personas (User-Embedded, Hosted Delegated, Autonomous). See the [Agents](../agents/) section for details on creating and managing agent applications.

## Create an application

### AM Console

1. Log in to AM Console.
2. If you want to create your application in a different security domain, select the domain from the user menu at the top right.
3. Click **Applications**.
4. Click the plus icon <img src="https://128066588-files.gitbook.io/~/files/v0/b/gitbook-x-prod.appspot.com/o/spaces%2FbGmDEarvnV52XdcOiV8o%2Fuploads%2FR4vk3bTTm3nNj9lAynM3%2Fimage.png?alt=media&#x26;token=704ca395-1cf0-48ba-baeb-05ba669ddab5" alt="" data-size="line">.
5. Select the [application type](../applications/application-types.md) and click **Next**.

   <figure><img src="https://128066588-files.gitbook.io/~/files/v0/b/gitbook-x-prod.appspot.com/o/spaces%2FbGmDEarvnV52XdcOiV8o%2Fuploads%2FBUA3LgGgCOdrW4VrUn6u%2Fimage.png?alt=media&#x26;token=f8e06806-b745-43ae-b641-19bfee0c580e" alt=""><figcaption><p>Select application type</p></figcaption></figure>
6. Specify the application details and click **Create**.

   <figure><img src="https://128066588-files.gitbook.io/~/files/v0/b/gitbook-x-prod.appspot.com/o/spaces%2FbGmDEarvnV52XdcOiV8o%2Fuploads%2FCIwunUNnCyI15nkVzi1d%2Fimage.png?alt=media&#x26;token=df4a9be5-3f9f-43a8-ae5a-50543bc3095d" alt=""><figcaption><p>Create Application form</p></figcaption></figure>

### AM API

{% code overflow="wrap" %}

```sh
curl -H "Authorization: Bearer :accessToken" \
     -H "Content-Type:application/json;charset=UTF-8" \
     -X POST \
     -d '{"name":"My App", "type": "SERVICE"}' \
     http://GRAVITEEIO-AM-MGT-API-HOST/management/organizations/DEFAULT/environments/DEFAULT/domains/:domainId/applications
```

{% endcode %}

### Configure the application

After you have created the new application, you will be redirected to the application’s `Overview` page, which contains some documentation and code samples to help you start configuring the application.

<figure><img src="https://128066588-files.gitbook.io/~/files/v0/b/gitbook-x-prod.appspot.com/o/spaces%2FbGmDEarvnV52XdcOiV8o%2Fuploads%2F8B7YJu6HZjqpnGIBNbOo%2Fimage.png?alt=media&#x26;token=998cf94f-866c-4b54-92bb-56e05fd585aa" alt="Application Overview"><figcaption><p>Application Overview</p></figcaption></figure>

### Test the application

The quickest way to test your newly created application is to request an OAuth2 access token, as described in [set up your first application](https://documentation.gravitee.io/apim/~/changes/337/broken-reference). If you manage to retrieve an access token, your application is all set.


<figure><img src="../../.gitbook/assets/guide-applications-readme-83.png" alt=""><figcaption><p>Application Identity Provider selection options</p></figcaption></figure>
## Application Identity Providers

AM allows your application to use different identity providers (IdPs). If you haven’t configured your providers yet, visit the [Identity Provider guide.](https://documentation.gravitee.io/apim/~/changes/337/broken-reference)

The application identity providers are separated into two sections:

* The regular Identity Providers (called also **internal**) that operate inside and AM without redirecting to another provider
* The Social/Enterprise Identity Providers that require an external service to perform authentication (usually via SSO)

<figure><img src="https://128066588-files.gitbook.io/~/files/v0/b/gitbook-x-prod.appspot.com/o/spaces%2FbGmDEarvnV52XdcOiV8o%2Fuploads%2FII76ZE16ZrLHjkHZXnyR%2Fimage.png?alt=media&#x26;token=05e294b1-2987-4f4d-8ad9-5a574e4a47ce" alt="Configure Identity Providers for your Application"><figcaption><p>Configure Identity Providers for your Application</p></figcaption></figure>

You can enable/disable them to include them within your authentication flow.

## Dynamic client registration

Another way to create applications in AM is to use the OpenID Connect Dynamic Client Registration endpoint. This specification enables Relying Parties (clients) to register applications in the OpenID Provider (OP).

# enable Dynamic Client Registration
curl -X PATCH \
  -H 'Authorization: Bearer :accessToken' \
  -H 'Content-Type: application/json' \
  -d '{ "oidc": {
        "clientRegistrationSettings": { \
            "isDynamicClientRegistrationEnabled": true,
            "isOpenDynamicClientRegistrationEnabled": false
      }}}' \
  http://GRAVITEEIO-AM-MGT-API-HOST/management/domains/:domainId
```

# Register a new Relying Party (client)
curl -X POST \
  -H 'Authorization: Bearer :accessToken' \
  -H 'Content-Type: application/json' \
  -d '{ \
        "redirect_uris": ["https://myDomain/callback"], \
        "client_name": "my web application", \
        "grant_types": [ "authorization_code","refresh_token"], \
        "scope":"openid" \
      }' \
  http://GRAVITEEIO-AM-GATEWAY-HOST/::domain/oidc/register
```

{% hint style="info" %}
`response_types` metadata is not required here as the default value (code) corresponds to the `authorization_code` grant type.
{% endhint %}

**Register Single Page Application (SPA) example**

As a SPA does not use a backend, we recommend you use the following implicit flow:

```sh
# Register a new Relying Party (client)
curl -X POST \
  -H 'Authorization: Bearer :accessToken' \
  -H 'Content-Type: application/json' \
  -d '{ \
        "redirect_uris": ["https://myDomain/callback"], \
        "client_name": "my single page application", \
        "grant_types": [ "implicit" ], \
        "response_types": [ "token" ], \
        "scope":"openid" \
      }' \
  http://GRAVITEEIO-AM-GATEWAY-HOST/::domain/oidc/register
```

{% hint style="info" %}
`response_types` metadata must be set to token in order to override the default value.
{% endhint %}

**Register Server to Server application example**

Sometimes you may have a bot/software that needs to be authenticated as an application and not as a user.\
For this, you need to use a `client_credentials` flow:

```sh
# Register a new Relying Party (client)
curl -X POST \
  -H 'Authorization: Bearer :accessToken' \
  -H 'Content-Type: application/json' \
  -d '{ \
        "redirect_uris": [], \
        "application_type": "server", \
        "client_name": "my server application", \
        "grant_types": [ "client_credentials" ], \
        "response_types": [ ] \
      }' \
  http://GRAVITEEIO-AM-GATEWAY-HOST/::domain/oidc/register
```

{% hint style="warning" %}
`response_types` metadata must be set as an empty array in order to override the default value.\
`redirect_uris` is not needed, but this metadata is required in the [specification](https://openid.net/specs/openid-connect-registration-1_0.html), so it must be set as an empty array.\
**We strongly discourage you from using this flow in addition to a real user authentication flow. The recommended approach is to create multiple clients instead.**
{% endhint %}

**Register mobile application example**

For a mobile app, the `authorization_code` grant is recommended, in addition to [Proof Key for Code Exchange](https://tools.ietf.org/html/rfc7636):

```sh
# Register a new Relying Party (client)
curl -X POST \
  -H 'Authorization: Bearer :accessToken' \
  -H 'Content-Type: application/json' \
  -d '{ \
        "redirect_uris": ["com.mycompany.app://callback"], \
        "application_type": "native", \
        "client_name": "my mobile application", \
        "grant_types": [ "authorization_code","refresh_token" ], \
        "response_types": [ "code" ] \
      }' \
  http://GRAVITEEIO-AM-GATEWAY-HOST/::domain/oidc/register
```

#### Read/update/delete client information

The `register` endpoint also allows you to GET/UPDATE/PATCH/DELETE actions on a `client_id` that has been registered through the `registration` endpoint.\
To do this, you need the access token generated during the client registration process, provided in the response in the `registration_access_token` field.

{% hint style="info" %}
The UPDATE http verb will act as a full overwrite, whereas the PATCH http verb will act as a partial update.
{% endhint %}

This access token contains a `dcr` scope which can not be obtained, even if you enable the `client_credentials` flow. In addition, rather than using the OpenID registration endpoint together with the `client_id`, the DCR specifications recommend you use the `registration_client_uri` given in the register response instead.

A new registration access token is generated each time the client is updated through the Dynamic Client Registration URI endpoint, which will revoke the previous value.

```sh
# Update a registered Relying Party (client)
curl -X PATCH \
  -H 'Authorization: Bearer :accessToken' \
  -H 'Content-Type: application/json' \
  -d '{ "client_name": "myNewApplicationName"}' \
  http://GRAVITEEIO-AM-GATEWAY-HOST/::domain/oidc/register/:client_id
```

#### Renew client secret

To renew the `client_secret`, you need to concatenate `client_id` and `/renew_secret` to the registration endpoint and use the POST HTTP verb.

{% hint style="info" %}
The `renew_secret` endpoint can also be retrieved through the OpenID discovery endpoint `registration_renew_secret_endpoint` property. You will then need to replace the `client_id` with your own.\
The `renew_secret` endpoint does not need a body.
{% endhint %}

When you update a client, a new registration access token is generated each time you renew the client secret.

```sh
# Renew the client secret of a registered Relying Party (client)
curl -X POST \
  -H 'Authorization: Bearer :accessToken' \
  http://GRAVITEEIO-AM-GATEWAY-HOST/::domain/oidc/register/:client_id/renew_secret
```

#### Scope Management

You can whitelist which scopes can be requested, define some default scopes to apply and force a specific set of scopes.

**Allowed scopes (scope list restriction)**

By default, no scope restrictions are applied when you register a new application.\
However, it is possible to define a list of allowed scopes through the **Allowed scopes** tab.\
To achieve this, you need to first enable the feature and then select the allowed scopes.

You can also enable this feature using AM API:

```sh
# Enable Allowed Scopes feature.
curl -X PATCH \
  -H 'Authorization: Bearer :accessToken' \
  -H 'Content-Type: application/json' \
  -d '{ "oidc": {
        "clientRegistrationSettings": { \
            "isAllowedScopesEnabled": true,
            "allowedScopes": ['your','scope','list','...']
      }}}' \
  http://GRAVITEEIO-AM-MGT-API-HOST/management/domains/:domainId
```

**Default scopes**

The [specification](https://tools.ietf.org/html/rfc7591#section-2) states that if scopes are omitted while registering an application, the authorization server may set a default list of scopes.\
To enable this feature, you simply select which scopes you want to be automatically set.

You can also enable this feature using AM API:

```sh
# Enable Default Scopes feature
curl -X PATCH \
  -H 'Authorization: Bearer :accessToken' \
  -H 'Content-Type: application/json' \
  -d '{ "oidc": {
        "clientRegistrationSettings": { \
            "defaultScopes": ['your','scope','list','...']
      }}}' \
  http://GRAVITEEIO-AM-MGT-API-HOST/management/domains/:domainId
```

**Force the same set of scopes for all client registrations**

If you want to force all clients to have the same set of scopes, you can enable the allowed scopes feature with an empty list and then select some default scopes.

{% hint style="info" %}
Enabling the allowed scopes feature with an empty list will remove all requested scopes from the client registration request.\
Since there is no longer a requested scope in the request, the default scopes will be applied.
{% endhint %}

You can also enable this feature using AM API:

```sh
# Force set of scopes on each client registration
curl -X PATCH \
  -H 'Authorization: Bearer :accessToken' \
  -H 'Content-Type: application/json' \
  -d '{ "oidc": {
        "clientRegistrationSettings": { \
            "isAllowedScopesEnabled": true,
            "allowedScopes": [],
            "defaultScopes": ['your','scope','list','...']
      }}}' \
  http://GRAVITEEIO-AM-MGT-API-HOST/management/domains/:domainId
```

# enable Dynamic Client Registration
curl -X PATCH \
  -H 'Authorization: Bearer :accessToken' \
  -H 'Content-Type: application/json' \
  -d '{ "oidc": {
        "clientRegistrationSettings": { \
            "isDynamicClientRegistrationEnabled": true,
            "isClientTemplateEnabled": true
      }}}' \
  http://GRAVITEEIO-AM-MGT-API-HOST/management/domains/:domainId
```

#### Define which client must be used as a template

In the Dynamic Client Registration **Client templates** tab, enable this feature to be used as a template in the client:

<figure><img src="https://128066588-files.gitbook.io/~/files/v0/b/gitbook-x-prod.appspot.com/o/spaces%2FbGmDEarvnV52XdcOiV8o%2Fuploads%2F3X8Q9cjacCh38w1S79cj%2Fimage.png?alt=media&#x26;token=bbb88c68-2e57-436e-9f44-f0d2f30b48e6" alt=""><figcaption></figcaption></figure>

You can also enable this feature using AM API:

```sh
# enable Dynamic Client Registration
curl -X PATCH \
  -H 'Authorization: Bearer :accessToken' \
  -H 'Content-Type: application/json' \
  -d '{"template":true}' \
  http://GRAVITEEIO-AM-MGT-API-HOST/management/domains/:domainId/clients/:clientId
```

{% hint style="warning" %}
Once a client is set up as a template, it can no longer be used for authentication purposes.
{% endhint %}

#### Register call with template example

You need to retrieve the `software_id` of the template, which is available under the `registration_templates_endpoint` provided by the OpenID discovery endpoint.

```sh
# Register a new Relying Party (client)
curl -X POST \
  -H 'Authorization: Bearer :accessToken' \
  -H 'Content-Type: application/json' \
  -d '{ \
        "software_id": "", \
        "redirect_uris": ["https://myDomain/callback"], \
        "client_name": "my single page application from a template" \
      }' \
  http://GRAVITEEIO-AM-GATEWAY-HOST/::domain/oidc/register
```

You can override some properties of the template by filling in some metadata, such as `client_name` in the example above.

Some critical information is not copied from the template (e.g. `client_secret` and `redirect_uris`). This is why in the example above, we need to provide valid `redirect_uris` metadata, since in the example, the template we are using is a Single Page Application.
