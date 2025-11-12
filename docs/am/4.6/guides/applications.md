# Applications

## Overview

_Applications_ act on behalf of the user to request tokens, hold user identity information, and retrieve protected resources from remote services and APIs.

Application definitions apply at the _security domain_ level.

## Create an application

### AM Console

1. Log in to AM Console.
2. If you want to create your application in a different security domain, select the domain from the user menu at the top right.
3. Click **Applications**.
4. Click the plus icon ![plus icon](https://docs.gravitee.io/images/icons/plus-icon.png).
5.  Select the application type and click **Next**.

    <figure><img src="https://docs.gravitee.io/images/am/current/quickstart-create-application.png" alt=""><figcaption><p>Select application type</p></figcaption></figure>
6.  Specify the application details and click **Create**.

    <figure><img src="https://docs.gravitee.io/images/am/current/quickstart-create-application2.png" alt=""><figcaption><p>Application Settings</p></figcaption></figure>

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

<figure><img src="https://docs.gravitee.io/images/am/current/graviteeio-am-userguide-client-settings.png" alt=""><figcaption><p>Application overview</p></figcaption></figure>

### Test the application

The quickest way to test your newly created application is to request an OAuth2 access token, as described in [set up your first application](docs/am/4.6/getting-started/tutorial-getting-started-with-am/set-up-your-first-application.md). If you manage to retrieve an access token, your application is all set.

## Application identity providers

AM allows your application to use different identity providers (IdPs). If you haven’t configured your providers yet, visit the [Identity Provider guide.](identity-providers/)

The application identity providers are separated into two sections:

* The regular Identity Providers (called also **internal**) that operate inside and AM without redirecting to another provider
* The Social/Enterprise Identity Providers that require an external service to perform authentication (usually via SSO)

<figure><img src="https://docs.gravitee.io/images/am/current/graviteeio-am-userguide-application-identity-providers.png" alt=""><figcaption><p>Application identity providers</p></figcaption></figure>

You can enable/disable them to include them within your authentication flow.

### Priority

Identity provider priority enables processing authentication in a certain order. It gives more control over the authentication flow by deciding which provider should evaluate credentials first.

In order to change the priority of the providers:

* Make sure your provider is **selected**
* Simply **drag-and-drop** the providers
* Save your settings

### Selection rules

Identity provider selection rules also give you more control over the authentication via Gravitee's Expression Language.

When coupled with [flows](flows.md) you can decide which provider will be used to authenticate your end users.

<figure><img src="https://docs.gravitee.io/images/am/current/graviteeio-am-userguide-application-identity-providers-selection-rule.png" alt=""><figcaption><p>Selection rule</p></figcaption></figure>

To apply a selection rule:

* Click on the **Selection rule** icon
* Enter your expression language rule
* Validate and save your settings

When applying rules on **regular** Identity Providers:

* If the rule is empty, the provider **will be** taken into account (this is to be retro-compatible when migrating from a previous version)
* Otherwise, AM will authenticate with the first identity provider where the rule matches.

If you are not using[ identifier-first login](login/identifier-first-login-flow.md), the rule won’t be effective on Social/Enterprise providers

However, if you are using identifier-first login:

* If the rule is empty, the provider **WILL NOT BE** taken into account (this is to be retro-compatible when migrating from a previous version)
* Otherwise, AM will authenticate with the first identity provider where the rule matches.

## Dynamic client registration

Another way to create applications in AM is to use the OpenID Connect Dynamic Client Registration endpoint. This specification enables Relying Parties (clients) to register applications in the OpenID Provider (OP).

### Enable Dynamic Client Registration with AM Console

By default this feature is disabled. You can enable it through the domain settings:

1. Log in to AM Console.
2. Click **Settings**, then in the **OPENID** section click **Client Registration**.
3. Click the toggle button to **Enable Dynamic Client Registration**.

{% hint style="danger" %}
There is another parameter called **Enable\Disable Open Dynamic Client Registration**. This parameter is used to allow any unauthenticated requests to register new clients through the registration endpoint. It is part of the OpenID specification, but for security reasons, it is disabled by default.
{% endhint %}

<figure><img src="https://docs.gravitee.io/images/am/current/graviteeio-am-userguide-domain-enable-dcr.png" alt=""><figcaption><p>Enable dynamic client registration</p></figcaption></figure>

### Enable Dynamic Client Registration with AM API

```sh
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

### Register a new client

#### Obtain an access token

Unless you enabled open dynamic registration, you need to obtain an access token via the `client_credentials` flow, with a `dcr_admin` scope.

{% hint style="danger" %}
The `dcr_admin` scope grants CRUD access to any clients in your domain. You must only allow this scope for trusted RPs (clients).
{% endhint %}

{% code overflow="wrap" %}
```sh
#Request a token
curl -X POST \
  'http://GRAVITEEIO-AM-GATEWAY-HOST/:domain/oauth/token?grant_type=client_credentials&scope=dcr_admin&client_id=:clientId&client_secret=:clientSecret'
```
{% endcode %}

#### Register new RP (client)

Once you obtain the access token, you can call AM Gateway through the registration endpoint. You can specify many client properties, such as `client_name`, but only the `redirect_uris` property is mandatory. See the [OpenID Connect Dynamic Client Registration](https://openid.net/specs/openid-connect-registration-1_0.html) specification for more details.

The endpoint used to register an application is available in the OpenID discovery endpoint (e.g., `http(s)://your-am-gateway-host/your-domain/oidc/.well-known/openid-configuration`) under the `registration_endpoint` property.

The response will contain some additional fields, including the `client_id` and `client_secret` information.

You will also find the `registration_access_endpoint` and the `registration_client_uri` in the response. These are used to read/update/delete the client id and client secret.

{% hint style="warning" %}
According to the [specification](https://tools.ietf.org/html/rfc6749#section-10.6), an Authorization Server MUST require public clients and SHOULD require confidential clients to register their redirection URIs.\
Confidential clients are clients that can keep their credentials secret, for example:\
\- web applications (using a web server to save their credentials): `authorization_code`\
\- server applications (treating credentials saved on a server as safe): `client_credentials`\
Unlike confidential clients, public clients are clients who cannot keep their credentials secret, for example:\
\- Single Page Applications: `implicit`\
\- Native mobile application: `authorization_code`\
**Because mobile and web applications use the same grant, we force `redirect_uri` only for implicit grants.**
{% endhint %}

**Register Web application example**

The following example creates a web application (`access_token` is kept on a backend server).

```sh
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

### Register new client using templates

You can create a client and define it as a template. Registering a new application with a template allows you to specify which identity providers to use, and apply template forms (such as login, password management, and error forms) or emails (such as registration confirmation and password reset emails).

#### Enable Dynamic Client Registration templates

You can enable the template feature in the AM Dynamic Client Registration **Settings** tab:

<figure><img src="https://docs.gravitee.io/images/am/current/graviteeio-am-userguide-domain-enable-dcr-templates.png" alt=""><figcaption><p>Enable templates</p></figcaption></figure>

You can also enable this feature using AM API:

```sh
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

<figure><img src="https://docs.gravitee.io/images/am/current/graviteeio-am-userguide-domain-define-dcr-templates.png" alt=""><figcaption><p>Specify clients</p></figcaption></figure>

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

<figure><img src="https://docs.gravitee.io/images/am/current/graviteeio-am-userguide-domain-dcr-templates.png" alt=""><figcaption><p>Client overview</p></figcaption></figure>

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
