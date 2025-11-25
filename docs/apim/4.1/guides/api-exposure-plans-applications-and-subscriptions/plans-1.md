---
description: How to consume secured APIs
---

# Applications

To access your APIs, consumers must register an application and subscribe to a published API plan (unless the plan is keyless). Applications act on behalf of the user to request tokens, provide user identity information, and retrieve protected resources from remote services and APIs.

## Prerequisites

There are two requirements to allow API consumers to create applications:

1. Admins need to first enable the correct options in the **Settings > Client Registration** page. Here, you can define the allowed types of applications that API consumers can create:

**Simple:** does _not_ require enabling **Dynamic Client Registration.** API consumers can optionally define the `client_id` when creating the application.

**Advanced:** the API producer must enable and configure **Dynamic Client Registration** to allow API consumers to create these application types. The client registration provider is responsible for creating the `client_id` and `client_secret` for each application that registers.

* **Browser**
* **Web**
* **Native**
* **Backend-to-Backend**

<figure><img src="../../.gitbook/assets/client_registration_settings (1).png" alt=""><figcaption><p>Client Registration settings</p></figcaption></figure>

2. API consumers must have a user account to register an application and subscribe to an API which you can learn how to enable in Administration.

## Simple application configuration

To allow API consumers to create a simple application, enable the **Simple** option in the **Allowed application types** section. This allows the API consumer to define the `client_id` on their own for use in JWT and OAuth API plans.

## Advanced application configuration

API producers typically do not allow API consumers to create simple applications when using more secure plans with JWT or OAuth authentication types. To allow API consumers to register advanced applications, dynamic client registration must be enabled and configured with a client registration provider.

Since dynamic client registration is an OAuth flow, we first wanted to provide some quick definitions of relevant OAuth terminology.

### Relevant OAuth terminology

OAuth 2.0 defines four roles:

* **Resource owner**: an entity enabled to grant access to a protected resource. When the resource owner is a person, it is referred to as an _end user_.
  * The API publisher, or owner of the backend APIs that Gravitee's Gateway is protecting, is the resource owner.
* **Client:** an application making protected resource requests on behalf of the resource owner and with the resource owner’s authorization. The term _client_ does not imply any particular implementation characteristics (e.g. whether the application executes on a server, a desktop or other device).
  * The API consumer's application attempting to register through the Developer Portal or Management Console is the client.
* **Resource server:** the server hosting the protected resources, capable of accepting and responding to protected resource requests using access tokens.
  * The APIM Gateway sitting in front of the backend APIs is the resource server.
* **Authorization server:** the server issuing access tokens to the client after successfully authenticating the resource owner and obtaining authorization.
  * The client registration provider we are about to configure is the authorization server.

{% hint style="info" %}
The resource server and the authorization server can be the same server.
{% endhint %}

Additional Oauth terminology:

* **Redirect URI**: the URL the authorization server will redirect the resource owner back to after granting permission to the client. Often referred to as the callback URL.
* **Response type:** the type of information the client expects to receive. Generally, it is an authorization code.
* **Scope:** granular permissions the client requests, such as access to data
* **Consent:** verifies scopes with the resource owner to determine if the client will receive the requested permissions
* **Client ID:** used to identify the client with the authorization server
* **Client Secret:** password only the client and authorization server know
* **Authorization Code:** short-lived code sent back to the client from the authorization server. The client sends the authorization code in combination with the client secret back to the authorization server to receive an access token.
* **Access Token:** the token that the client will use to communicate with the resource server

### Dynamic client registration provider

{% hint style="warning" %}
**Enterprise only**

As of Gravitee 4.0, Dynamic Client Registration is an Enterprise Edition capability. To learn more about Gravitee Enterprise, and what's included in various enterprise packages, please:

* [Refer to the EE vs OSS documentation](../../overview/ee-vs-oss/)
* [Book a demo](https://app.gitbook.com/o/8qli0UVuPJ39JJdq9ebZ/s/rYZ7tzkLjFVST6ex6Jid/)
* [Check out the pricing page](https://www.gravitee.io/pricing)
{% endhint %}

[Dynamic client registration](https://www.rfc-editor.org/rfc/rfc7591) (DCR) is a protocol that allows OAuth client applications to register with an OAuth server through the OpenID Connect (OIDC) client registration endpoint. DCR allows API consumers to register applications with an OAuth server from Gravitee's Developer Portal or Management Console. This outsources the issuer and management of application credentials to a third party, allowing for additional configuration options and compatibility with various OIDC features provided by the identity provider.

Once dynamic client registration has been [enabled in the **Client Registration** settings,](plans-1.md#prerequisites) you need to add a **Provider** at the bottom of the **Client Registration** page. We will be using Gravitee Access Management (AM) for our provider, but you are free to use any authentication server supporting OIDC.

<figure><img src="../../.gitbook/assets/add_dcr_provider (1).png" alt=""><figcaption><p>Add a client registration provider</p></figcaption></figure>

You are presented with the following options when configuring a client registration provider:

<figure><img src="../../.gitbook/assets/client_registration_provider (1).png" alt=""><figcaption><p>Configure a client registration provider</p></figcaption></figure>

The **General** section allows you to set a **Name** and **Description** for your client registration provider.

The **Configuration** section first requires you to set an **OpenID Connect Discovery Endpoint** which is the URL where an OIDC-compatible authorization server publishes its metadata. The metadata is a JSON listing of the OpenID/OAuth endpoints, supported scopes and claims, public keys used to sign the tokens, and other details. This information can be used to construct a request to the authorization server. The field names and values are defined in the [OIDC Discovery Specification.](https://openid.net/specs/openid-connect-discovery-1_0.html)

Once the endpoint is set, the configuration options branch in two directions based on the **Initial Access Token Provider: Client Credentials** or direct provisioning of an **Initial Access Token.** Both of these options are detailed further in the [following section](plans-1.md#dcr-initial-access-token-flows).

One additional configuration setting that is common to both initial access token flows is **Renew client\_secret (outside DCR specification).** If enabled, this allows registered clients to call the relevant endpoint with their `client_id` to renew the `client_secret` issued by the authorization server.

### DCR: Initial access token flows

The initial access token is provided by the authorization server to grant access to its protected client registration endpoint. Regardless of the method used to obtain the initial access token, the flow for registering future applications remains the same. The initial access token will be used to call the protected client registration endpoint which will respond with the application's client ID and depending on the application type, an optional client secret.

For OAuth 2.0 plans, these credentials will be used whenever a resource owner authorizes the application to access a protected resource. If authorized successfully, the authorization server will return an access token that will be verified through token introspection upon requests to the Gateway before accessing backend APIs protected by OAuth 2.0 plans.

#### Client credentials

<figure><img src="../../.gitbook/assets/client_credentials_token_provider (1).png" alt=""><figcaption><p>Client credentials token provider</p></figcaption></figure>

Client credential is an authorization grant flow detailed further in the [next section](plans-1.md#client-credentials-1) and is the first of the two options for retrieving an initial access token.

Using the client credentials flow allows you to set up your authorization server, obtain its associated **Client ID** and **Client Secret,** and add them to the provider's configuration settings. When you select **Create** at the bottom of the page, a request with the client credentials will immediately be sent to the authorization server's token endpoint for an initial access token. Therefore, when future API consumers register an advanced application, they will utilize this initial access token to access the protected client registration endpoint.

The client credential flow offers two additional configuration settings:

* **Scopes:** provide default scopes to use for application registration
* **Client Template (software\_id):** optional id of the client template to use for all applications registering through this provider
  * Some authorization servers allow you to create a client as a template. Registering a new application with a template allows you to specify which identity providers to use, and apply template forms (such as login, password management, and error forms) or emails (such as registration confirmation and password reset emails).
  * This can simplify administration, as all dynamic clients can be updated as a whole. If the configuration of the template changes (e.g., authentication requirements, redirect URI(s), allowed scopes, etc.), then all dynamic clients based on that client are immediately updated.

#### Direct provisioning

<figure><img src="../../.gitbook/assets/Screenshot 2023-03-23 at 12.02.08 PM (1).png" alt=""><figcaption><p>Directly provide initial access token</p></figcaption></figure>

Direct provisioning is a much simpler and less secure way to provide the initial access token. Administrators can directly add the initial access token as shown in the image above.

### Authorization grant types

Each advanced application type has a subset of allowable authorization grant types. An authorization grant is a flow used by the client to obtain an access token. How you use grant types mainly depends on your application type.

APIM supports five authorization grant flows out of the box:

* [Authorization code](plans-1.md#authorization-code)
* [Implicit](plans-1.md#implicit)
* [Resource owner password](plans-1.md#resource-owner-password-credentials)
* [Client credentials](plans-1.md#client-credentials-1)
* [Refresh token](plans-1.md#refresh-token)

#### Authorization code

The authorization code is a temporary code returned after requesting the authorization of the end user.

**Flow**

1. The end user clicks **Sign in** in the application.
2. The end user is redirected to the authorization server.
3. The end user authenticates using one of the configured identity providers and login options (MFA for example).
4. (Optional) A consent page is displayed to ask for user approval.
5. The authorization server redirects the end user back to the application with an authorization code.
6. The application calls the authorization server to exchange the code for an access token (and optionally, a refresh token).
7. The application uses the access token to make secure API calls for the end user.

**Additional information**

* Authorization codes are single-use.
* For server-side web apps, such as native (mobile) and Javascript apps, you also use the [PKCE extension](https://tools.ietf.org/html/rfc7636) as part of your flow, which provides protection against other attacks where the authorization code may be intercepted.
* For more information about this flow, see the [RFC](https://tools.ietf.org/html/rfc6749#section-1.3.1).

#### Implicit

{% hint style="danger" %}
**Implicit flow security concerns**

The OAuth standard now discourages the use of an implicit grant to request access tokens from Javascript applications. You should consider using the authorization code grant with a PKCE extension for all your applications.
{% endhint %}

The implicit grant is a simplified authorization code flow. Instead of getting a temporary code first, you can retrieve an access token directly from web browser redirection.

**Flow**

1. The end user clicks **Sign in** in the application.
2. The end user is redirected to the authorization server.
3. The end user authenticates using one of the configured identity providers and login options (MFA for example).
4. (Optional) A consent page is displayed to ask for user approval.
5. The authorization server redirects the end user back to the application with an access token.
6. The application uses the access token to make secure API calls for the end user.

**Additional information**

* For more information about this flow, see the [RFC](https://tools.ietf.org/html/rfc6749#section-1.3.2).

#### Resource owner password credentials

The resource owner password credentials (i.e. username and password) can be used directly as an authorization grant to obtain an access token (using a REST approach).

The biggest difference from other flows is that the authentication process is triggered by the application and not the authorization server.

{% hint style="info" %}
**Trusted clients only**

This grant type should only be used when there is a high degree of trust between the resource owner and the client (e.g. the client is part of the device operating system or a highly privileged application) and when other authorization grant types are not available (such as the authorization code grant type).
{% endhint %}

**Flow**

1. The end user clicks **Sign in** and enters the user credentials (username/password) in the application form.
2. The application forward the credentials to the authorization server.
3. The authorization server checks the credentials.
4. The authorization server responds with an access token (and optionally, a refresh token).
5. The application uses the access token to make secure API calls for the end user.

**Additional information**

* For more information about this flow, see the [RFC](https://tools.ietf.org/html/rfc6749#section-1.3.3).

#### Client credentials

The client credentials grant type is used by clients to obtain an access token outside the context of a user. This is typically used by clients to access resources about themselves rather than user resources.

**Additional information**

* The flow is typically used when the client is acting on its own behalf (the client is also the resource owner), i.e. machine-to-machine communication.
* For more information about this flow, see the [RFC](https://tools.ietf.org/html/rfc6749#section-1.3.4).

#### Refresh token

A refresh token is used to get a new access token, prompting the client application to renew access to protected resources without displaying a login page to the resource owner.

**Additional information**

* For security reasons (a user can remain authenticated forever), a refresh token must be stored in a secure place (i.e server side) and is never sent to the resource server.

## Create an application

With all the preparation work complete, API consumers can now create an application through either the Management Console or the Developer Portal. We will work through the Management Console as we have a separate guide dedicated to the Developer Portal.

{% @arcade/embed url="https://app.arcade.software/share/K4c4gw3qU4Mrmsm74Q0E" flowId="K4c4gw3qU4Mrmsm74Q0E" %}

{% hint style="info" %}
**Default application**

To help new users quickly move forward with API consumption, a default application is automatically created for every new user (not including admins). This can be easily disabled in the `gravitee.yml` file using the configuration below.
{% endhint %}

{% code title="gravitee.yml" overflow="wrap" %}
```yaml
user:
    login:
       # Create a default application when user connects to the portal for the very first time (default true)
       defaultApplication: false
```
{% endcode %}

## Manage applications

When a new application is created, only the application’s creator, the _primary owner_, can see and manage the application. Most of the time, an application is shared through a developer application and will retrieve information such as API keys and API analytics.

By default, APIM includes three membership roles:

| Role              | Description                                                                                                                                |
| ----------------- | ------------------------------------------------------------------------------------------------------------------------------------------ |
| **Primary owner** | When an application is created, the primary owner is the creator of the application. Primary owner can do all possible actions for an API. |
| **Owner**         | Owner is a lightest version of the primary owner role. Owner can do all possible actions except delete the application.                    |
| **User**          | A user is a person who can access the application in read only mode and use the application to subscribe to an API.                        |

{% hint style="info" %}
Only users with the required permissions can manage application members. For more details, see the [User Management and Permissions](../administration/user-management-and-permissions.md) section of the Administration Guide.
{% endhint %}

{% @arcade/embed url="https://app.arcade.software/share/zb22huL5KmUF9Nky2hZ7" flowId="zb22huL5KmUF9Nky2hZ7" %}

### Delete and restore applications

You can delete any application you are the primary owner of at the bottom of the **Global Settings** page.

<figure><img src="../../.gitbook/assets/delete_application (1).png" alt=""><figcaption><p>Delete an application</p></figcaption></figure>

When a user deletes an application, it is in `ARCHIVED` status.

It means that:

* The link to the primary owner of the application is deleted.
* The subscriptions are closed. In the case of a subscription to an API-Key plan, the keys are revoked.
* Notification settings are deleted.

As an `ADMIN`, you can restore applications in the APIM Console.

The `ADMIN` user will become the primary owner of the application.

{% hint style="info" %}
Every application’s subscriptions will be restored in`PENDING` status. The API publisher will have to manually reactivate previous subscriptions.
{% endhint %}
