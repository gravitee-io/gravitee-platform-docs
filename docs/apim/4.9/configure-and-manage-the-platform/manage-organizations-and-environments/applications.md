---
description: An overview about applications.
---

# Applications

## Overview

To access Gravitee APIs, consumers must register an application and subscribe to a published API plan. Applications act on behalf of the user to request tokens, provide user identity information, and retrieve protected resources from remote services and APIs.

## Prerequisites

For an API consumer to create an application, the following must be true:

* An admin must define the 2 types of applications that API consumers are allowed to create:
  * **Default application type:** API consumers can optionally define the `client_id` when creating a simple application.
  * **Dynamic Client Registration (DCR) for applications:** The API publisher must enable and configure DCR for the allowed application types. The client registration provider is responsible for creating the `client_id` and `client_secret` for each application that registers.
* An API consumer must have a user account to register an application and subscribe to an API (see [User Management](user-management.md)).

## Default application configuration

The default simple application enables an API consumer to define the `client_id` for use in JWT and OAuth API plans. To allow API consumers to create a simple application, complete the following steps:

1. Log in to your APIM Console
2. Select **Settings** from the left nav
3. Select **Client Registration** from the inner left nav
4. Under **Default application type**, toggle **Simple** ON

<figure><img src="broken-reference" alt=""><figcaption></figcaption></figure>

{% hint style="info" %}
To expedite API consumption, a default application is automatically created for every new user (not including admins). This can be disabled in the `gravitee.yml` file as shown below:

{% code title="gravitee.yml" overflow="wrap" %}
```yaml
user:
    login:
       # Create a default application when user connects to the portal for the very first time (default true)
       defaultApplication: false
```
{% endcode %}
{% endhint %}

## DCR application configuration

{% hint style="warning" %}
Dynamic Client Registration is an [Enterprise Edition](../../readme/enterprise-edition.md) capability
{% endhint %}

The DCR protocol allows an OAuth client application to dynamically register with an OAuth server through the OpenID Connect (OIDC) client registration endpoint to obtain credentials and access protected resources.

Both the Developer Portal and APIM Console allow API consumers to register applications using DCR. DCR outsources the tasks of issuing and managing application credentials to a third party. These third parties may offer additional configuration options and compatibility with IdP OIDC features.

When an API publisher authorizes an application to access a protected resource, the authorization server verifies credentials and returns an access token. Token introspection is performed before requests to the Gateway can access backend APIs protected by OAuth2 plans.

### Terminology

DCR is an OAuth flow. Review relevant OAuth terminology below.

<details>

<summary>OAuth terminology</summary>

**OAuth 2.0 roles**

* **Authorization server:** Issues access tokens to the client after authenticating the resource owner and obtaining authorization. Can be the resource server.
* **Client:** An application making protected resource requests on behalf of the resource owner and with the resource owner’s authorization. The term client does not imply any particular implementation characteristics (i.e., whether the application executes on a server, a desktop, or another device).
* **Resource owner**: An entity enabled to grant access to a protected resource. When the resource owner is a person, it is referred to as an end user.
* **Resource server:** Hosts the protected resources. Capable of accepting and responding to protected resource requests using access tokens. Can be the authorization server.

**Additional terminology**

* **Access Token:** Used by the client to communicate with the resource server
* **Authorization Code:** Short-lived code sent to the client from the authorization server. The client sends the authorization code and client secret back to the authorization server to receive an access token.
* **Client ID:** Used by the authorization server to identify the client
* **Client Secret:** Password known to only the client and authorization server
* **Consent:** Verifies scopes with the resource owner to determine if the client will receive the requested permissions
* **Redirect URI**: The URL the authorization server will redirect the resource owner back to after granting permission to the client. Often referred to as the callback URL.
* **Response type:** The type of information the client expects to receive. Generally, it is an authorization code.
* **Scope:** Granular permissions requested by the client, e.g., access to data

</details>

{% hint style="info" %}
**OAuth2 terminology applied to Gravitee DCR configuration**

* **Authorization server:** The client registration provider
* **Client:** The consumer application attempting to register through the Developer Portal or Management Console
* **Resource owner:** The API publisher (owner of the backend APIs protected by Gravitee's Gateway)
* **Resource server:** The APIM Gateway sitting in front of the backend APIs
{% endhint %}

### Enable DCR

To enable DCR, complete the following steps:

1. Log in to your APIM Console
2. Select **Settings** from the left nav
3. Select **Client Registration** from the inner left nav
4. Toggle **Enable Dynamic Client Registration** ON

<figure><img src="broken-reference" alt=""><figcaption></figcaption></figure>

### Add a DCR provider

{% hint style="info" %}
Any authentication server supporting OIDC can be used as a DCR provider. This guide uses Gravitee Access Management (AM).
{% endhint %}

At the bottom of the **Client Registration** page, click **+ Add a provider** and configure the following:

<figure><img src="broken-reference" alt=""><figcaption></figcaption></figure>

* Set a **Name** and **Description** for the provider
*   **OpenID Connect Discovery Endpoint:** Enter the URL where an OIDC-compatible authorization server publishes its metadata

    <div data-gb-custom-block data-tag="hint" data-style="info" class="hint hint-info">
      <p>Metadata is a JSON listing of the OpenID/OAuth endpoints, supported scopes and claims, public keys used to sign the tokens, etc., which can be used to construct a request to the authorization server). Metadata field names and values are defined in the <a href="https://openid.net/specs/openid-connect-discovery-1_0.html">OIDC Discovery Specification.</a></p>
    </div>
* Use the **Initial Access Token Provider** drop-down menu to select the [initial access token flow](applications.md#initial-access-token-flows):
  * **Initial Access Token:** For direct provisioning, enter the **Initial Access Token** in the corresponding field
  * Provide the following **Client Credentials**:
    * **Client ID**
    * **Client Secret**
    * **Scopes:** Default scopes to use for application registration
    * **Client Template (software\_id):** Client template ID to use for all applications registering through this provider
* **Trust Store Type:** Use the drop-down menu to specify trusted SSL/TLS certificates. See [#dcr-trusted-certificate-configuration-details](applications.md#dcr-trusted-certificate-configuration-details "mention") for more information.
* **Key Store Type:** Use the drop-down menu to configure a key store. See [#dcr-trusted-certificate-configuration-details](applications.md#dcr-trusted-certificate-configuration-details "mention") for more information.
* **Enable renew client\_secret support:** Toggle ON to let registered clients call the endpoint with their `client_id` to renew the `client_secret` issued by the authorization server
  * Provide the **HTTP Method**
  * Provide the **Endpoint**. This field supports Gravitee Expression Language, e.g.,\
    `https://<your-am-gateway-domain>/<your-security-domain>/oidc/register/{#client_id}/renew_secret`

<details>

<summary>Initial access token flows</summary>

The Client Credentials flow sets up the authorization server and adds the client ID and client secret to the provider's configuration settings. A request for an initial access token is sent with the client credentials to the authorization server's token endpoint. API consumers registering an application can use the initial access token to access the protected client registration endpoint.

Some authorization servers allow you to create a client as a template. Registering a new application with a template allows you to specify which IdPs to use and apply template forms (e.g., login, password management, error forms) or emails (e.g., registration confirmation, password reset). This can simplify administration if the configuration of the template changes (e.g., authentication requirements, redirect URI(s), allowed scopes) because all dynamic clients are immediately updated.

Alternatively, direct provisioning is a much simpler and less secure way to provide the initial access token.

</details>

<details>

<summary>DCR trusted certificate configuration details</summary>

Trusted certificates secure communication between client applications and the OpenID provider. This ensures that only trusted clients can register using DCR.

**Configure the trust store**

To configure the trust store, complete the following steps:

1. Upload a `.p12` or `.jks` trust store file that contains the trusted CA certificates.
2. Enter the trust store password.

**Configure the key store**

If you are using mTLS and need to configure the key store, complete the following steps:

1. Upload a `.p12` or `.jks` key store file that includes the client certificate and private key.
2. Enter the key store password used to open the key store file.
3. If the private key is protected separately, enter the key password used to open the private key.
4. If necessary, specify the alias of the key entry.

{% hint style="info" %}
Gravitee does not directly support PEM (.crt/.key) certificates for trust store or key store configuration. To convert a PEM file to P12, use the following command:

```bash
openssl pkcs12 -export \
 -in client.crt \
 -inkey client.key \
 -out client.p12 \
 -name myalias \
 -CAfile ca.crt \
 -caname root
```
{% endhint %}

**Verification**

To verify that the trusted certificates are correctly configured for the DCR provider, follow the steps to register a new client application using a valid SSL/TLS certificate:

1. Obtain an access token with the `dcr_admin` scope.
2.  Use a tool like cURL or Postman to send a registration request to the DCR provider's registration endpoint. Include the SSL/TLS certificate in the request.

    ```bash
    curl -X POST \
     -H 'Authorization: Bearer <access_token>' \
     -H 'Content-Type: application/json' \
     --cert /path/to/client.crt \
     --key /path/to/client.key \
     -d '{ ... }' \
     https://<gravitee-am-gateway>/oidc/register
    ```

A successful registration indicates that the trusted certificates are configured correctly.

</details>

### Authorization grant types

Gravitee offers several DCR application types: Browser, Web, Native, and Backend-to-Backend. Each of these is associated with a subset of allowed authorization grant types. An authorization grant is a flow used by the client to obtain an access token. Grant type implementation is dependent on application type.

APIM supports the following authorization grant flows out of the box:

* [Authorization code](applications.md#authorization-code)
* [Implicit](applications.md#implicit)
* [Resource owner credentials](applications.md#resource-owner-credentials)
* [Client credentials](applications.md#client-credentials)
* [Refresh token](applications.md#refresh-token)

{% tabs %}
{% tab title="Authorization code" %}
The authorization code is a temporary code returned after requesting the authorization of the end user.

**Flow**

1. The end user signs in to the application
2. The end user is redirected to the authorization server
3. The end user authenticates using one of the configured identity providers and login options (e.g., MFA)
4. (Optional) A consent page is displayed asking for user approval
5. The authorization server redirects the end user back to the application with an authorization code
6. The application calls the authorization server to exchange the code for an access token and (optionally) a refresh token
7. The application uses the access token to make secure API calls on behalf of the end user

**Additional information**

* Authorization codes are single-use.
* For server-side web apps, e.g., native (mobile) and Javascript, the [PKCE extension](https://tools.ietf.org/html/rfc7636) is used as part of the flow to provide protection against attacks where the authorization code may be intercepted
{% endtab %}

{% tab title="Implicit" %}
{% hint style="danger" %}
**Security concerns**

The OAuth standard discourages using an implicit grant to request access tokens from Javascript applications. Consider using an authorization code grant with a PKCE extension for all of your applications.
{% endhint %}

The implicit grant is a simplified authorization code flow. Instead of first getting a temporary code, you can retrieve an access token directly from web browser redirection.

**Flow**

1. The end user signs in to the application
2. The end user is redirected to the authorization server
3. The end user authenticates using one of the configured identity providers and login options (e.g., MFA)
4. (Optional) A consent page is displayed asking for user approval
5. The authorization server redirects the end user back to the application with an access token
6. The application uses the access token to make secure API calls on behalf of the end user
{% endtab %}

{% tab title="Resource owner credentials" %}
The resource owner credentials (username and password) can be used directly as an authorization grant to obtain an access token This uses a REST approach, where the authentication process is triggered by the application and not the authorization server.

{% hint style="info" %}
**Trusted clients only**

This grant type should only be used when there is a high degree of trust between the resource owner and the client, e.g., the client is part of the device operating system or a highly privileged application, and other authorization grant types are not available.
{% endhint %}

**Flow**

1. The end user signs in to the application using the resource owner credentials
2. The application forwards the credentials to the authorization server
3. The authorization server verifies the credentials
4. The authorization server responds with an access token and (optionally) a refresh token
5. The application uses the access token to make secure API calls on behalf of the end user
{% endtab %}

{% tab title="Client credentials" %}
The client credentials grant type is used by clients to obtain an access token outside of the user context, e.g., to access client resources (as opposed to user resources).

The flow is typically used when the client is acting on its own behalf (the client is also the resource owner), i.e., machine-to-machine communication.
{% endtab %}

{% tab title="Refresh token" %}
A refresh token is used to obtain a new access token and prompts the client application to renew access to protected resources without displaying a login page to the resource owner.

For security reasons, because a user can remain authenticated indefinitely, a refresh token must be stored in a secure place (i.e., server-side) and is never sent to the resource server.
{% endtab %}
{% endtabs %}

For more information about these flows, see the [RFC](https://tools.ietf.org/html/rfc6749#section-1.3.1).

## Manage applications

An application is usually shared through a developer application and retrieves information such as API keys and API analytics. Initially, only the application’s creator can view and manage the application. By default, APIM includes three membership roles:

<table><thead><tr><th width="228">Role</th><th>Description</th></tr></thead><tbody><tr><td><strong>Primary owner</strong></td><td>The creator of the application. Can perform all possible API actions.</td></tr><tr><td><strong>Owner</strong></td><td>A lighter version of the primary owner role. Can perform all possible actions except delete the application.</td></tr><tr><td><strong>User</strong></td><td>A person who can access the application in read-only mode and use it to subscribe to an API.</td></tr></tbody></table>

{% hint style="info" %}
Only users with the required permissions can manage application members. See [User Management](user-management.md).
{% endhint %}

### Delete and restore applications

To delete an application, the primary owner must:

1. Log in to your APIM Console
2. Select **Applications** from the left nav
3. Select your application
4. Select **Global Settings** from the inner left nav
5.  In the **Danger Zone**, click **Delete**

    <figure><img src="broken-reference" alt=""><figcaption><p>Delete an application</p></figcaption></figure>

* A deleted application has a status of `ARCHIVED`, meaning:
  * The link to the primary owner of the application is deleted.
  * Its subscriptions are closed. In the case of a subscription to an API Key plan, the keys are revoked.
  * Notification settings are deleted.
* An `ADMIN` can restore applications in the APIM Console and will become the primary owner of the application
  * An application’s subscriptions will be restored with `PENDING` status. The API publisher must manually reactivate previous subscriptions.
