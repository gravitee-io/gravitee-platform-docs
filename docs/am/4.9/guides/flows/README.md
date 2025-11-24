---
description: Overview of Flows.
---

# Flows

## Overview

You can use flows to extend the standard AM behavior by executing [policies](policies/) during the `OnRequest` step of selected stages. Flows can be configured at the security domain level or application level.

## Execution context

Each policy has access to the `Execution Context` to retrieve and set information required to execute the policy code. The `Execution Context` data is propagated for availability in future use cases. For example, custom HTML forms.

The following example retrieves `Execution Context` data using the [Gravitee Expression Language](../am-expression-language.md):

{% code overflow="wrap" %}
```
{#request}: Current HTTP Request with parameters, headers, path, ...
{#context.attributes['client']}: OAuth 2.0 Client (if available) with clientId, clientName, ...
{#context.attributes['user']}: Authenticated User (if available) with username, firstName, lastName, email, roles, ...
```
{% endcode %}

<figure><img src="../../.gitbook/assets/Screenshot 2025-08-04 at 08.48.36.png" alt=""><figcaption><p>Policy Studio</p></figcaption></figure>

## Flow configuration

Flow configuration determines where and when policies are applied within AM authentication and authorization processes. Instead of executing policies globally, AM lets you attach them to specific phases of user interaction, which are referred to as flows. Each flow represents a logical step, such as login, registration, consent, or multi-factor authentication (MFA).

Policies can be executed at selected steps within flows, typically before or after a user action, such as submitting a form or confirming consent. This approach gives you precise control over security, validation, and customization logic at every key moment of the user journey.

### Key characteristics of flows

Flows lay the foundation for building complex, secure, and user-friendly authentication processes in AM. Flows have the following characteristics:

* **Granularity:** You can assign each policy to the specific flow phase that requires it for precise policy execution. You can also assign multiple policies to multiple phases to cascade policy execution in a single flow.
* **Flexibility:** Multiple flow types are supported, each corresponding to a different authentication or registration event.
* **Step specificity:** For each flow, policies can be run before or after a user action. This increases customization potential.
* **Separation of concerns:** By segmenting flows, you can separate policy logic by context. This simplifies management and troubleshooting.

### Flow types

Access Management supports a variety of flow types. Each type corresponds to a distinct stage in the authentication or user management process. Within each flow, you can define policies to be executed before or after the key user action.

<details>

<summary>ALL</summary>

The **ALL** flow is executed on each incoming request for one of the login, consent or register flows.

</details>

<details>

<summary>LOGIN IDENTIFIER</summary>

The **LOGIN IDENTIFIER** flow allows you to fetch more information or validate incoming data during the providing identity by End-User phase. It is triggered during the phase when the user provides their identifier (e.g., email or username). Policies can be applied before the identifier form is shown or after the user submits their identity.

**Pre Login Identifier**

The Pre step allows you to fetch more information before displaying the Login Identifier HTML Page.

The following attributes are available while processing the policy chain:

* [**Request**](./#request): current HTTP Request
* [**Client**](./#client): the application

**Post Login Identifier**

Post End-User Login Identifier happens after the user has given his identity to the authentication. It allows you to validate incoming data (user identity) before displaying password page.

The following attributes are available while processing the policy chain :

* [**Request**](./#request): current HTTP Request
* [**Client**](./#client): the application
* [**User**](./#user): the End-User identity

</details>

<details>

<summary>LOGIN</summary>

The **LOGIN** flow allows you to fetch more information or validate incoming data during the End-User authentication phase. Policies can be executed before displaying the login form or after successful authentication.

**Pre Login**

The Pre step allows you to fetch more information before displaying the Login HTML Page.

The following attributes are available while processing the policy chain:

* [**Request**](./#request): current HTTP Request
* [**Client**](./#client)**:** the application

**Post Login**

Post End-User Login happens after the user has given his consent to the processing of personal data. It allows you to validate incoming data (user consent) before giving access to the application.

The following attributes are available while processing the policy chain :

* [**Request**](./#request)**:** current HTTP Request
* [**Client**](./#client)**:** the application
* [**User**](./#user)**:** the End-User

</details>

<details>

<summary>CONNECT</summary>

The **CONNECT** flow allows you to execute additional operations when an authenticated user is recognized by the system, typically during federated login or account linking scenarios. It enables the execution of policies such as account linking between an external Identity Provider (IdP) and an existing user account.

**Pre Connect**

The **Pre Connect** step is executed before linking the authenticated user from an external Identity Provider (IdP) to a local user account.

Available attributes while processing the policy chain:

* [**Request:**](./#request) current HTTP Request
* [**Client:**](./#client) the application
* [**User:**](./#user) the authenticated user provided by the external IdP

**Post Connect**

The **Post Connect** step is executed **after** the user from the IdP has been linked to a local user account.

Available attributes while processing the policy chain:

* [**Request:**](./#request) current HTTP Request
* [**Client:**](./#client) the application
* [**User:**](../user-management/users/) the connected user

</details>

<details>

<summary>CONSENT</summary>

The **CONSENT** flow allows you to fetch more information or validate incoming data during the End-User consent phase. This flow happens after the user has logged in. Policies can run before showing the consent page or after the user gives consent for personal data processing.

**Pre End-User Consent**

Pre End-User Consent allows you to fetch more information or validate incoming data before displaying the User Consent HTML Page.

The following attributes are available while processing the policy chain:

* [**Request**](./#request): current HTTP Request
* [**Client**](./#client): the application
* [**User**](./#user): the End-User
* [**Authorization Request**](./#oauth-2.0-authorization-request): OAuth 2.0 Authorization Request

**Post End-User Consent**

Post End-User Consent happens after the user has given his consent to the processing of personal data. It allows you to validate incoming data (user consent) before giving access to the application.

The following attributes are available while processing the policy chain:

* [**Request**](./#request): current HTTP Request
* [**Client**](./#client): the application
* [**User**](./#user): the End-User
* [**Authorization Request**](./#oauth-2.0-authorization-request): OAuth 2.0 Authorization Request

</details>

<details>

<summary>REGISTER</summary>

The **REGISTER** flow allows you to fetch more information or validate incoming data during the End-User registration phase. Policies can be enforced before displaying the registration form or after the user’s data has been submitted.

**Pre End-User Registration**

Pre End-User Registration step is executed before displaying the User Consent HTML Page.

The following attributes are available while processing the policy chain:

* [**Request**](./#request): current HTTP Request
* [**Client**](./#client): the application

**Post End-User Registration**

Post End-User Registration step is executed once the user submit the registration form and information are preserve in database.

The following attributes are available while processing the policy chain :

* [**Request**](./#request): current HTTP Request
* [**Client**](./#client): the application
* [**User**](./#user): the End-User

</details>

<details>

<summary>RESET PASSWORD</summary>

The **RESET PASSWORD** flow allows you to execute policies during the password reset process. Policies may be executed before the reset form is shown or after the user submits a new password.

**Pre Reset Password**

The Pre Reset Password step is executed before displaying the Reset Password HTML page to the user.

Available attributes while processing the policy chain:

* [**Request**](./#request)**:** current HTTP Request
* [**Client:**](./#client) the application
* [**User:**](./#user) the End-User

**Post Reset Password**

The Post Reset Password step is executed after the user submits a new password and the change is processed.

Available attributes while processing the policy chain:

* [**Request:**](./#request) current HTTP Request
* [**Client:**](./#client) the application
* [**User:**](./#user) the End-User

</details>

<details>

<summary>REGISTRATION CONFIRMATION</summary>

The **REGISTRATION CONFIRMATION** flow is triggered during the account confirmation step after user registration. Policies can run before displaying the confirmation page or after the user confirms their account.

**Pre Registration Confirmation**

The Pre Registration Confirmation step is executed before displaying the Registration Confirmation HTML page to the user.

Available attributes while processing the policy chain:

* [**Request**](./#request)**:** current HTTP Request
* [**Client**](./#client)**:** the application
* [**User:**](./#user) the End-User

**Post Registration Confirmation**

The Post Registration Confirmation step is executed after the user confirms their account (e.g., via confirmation link or code).

Available attributes while processing the policy chain:

* [**Request**](./#request)**:** current HTTP Request
* [**Client**](./#client)**:** the application
* [**User**](./#user)**:** the End-User

</details>

<details>

<summary>TOKEN</summary>

The **TOKEN** flow occurs during the token request process (e.g., OAuth 2.0 token endpoint). It allows you to execute policies before or after token generation.

**Pre Token**

The Pre Token step is executed before generating the access token.

Available attributes while processing the policy chain:

* [**Request:**](./#request) current HTTP Request
* [**Client**](./#client)**:** the application
* [**Authorization Request**](./#oauth-2.0-authorization-request)**:** OAuth 2.0 Authorization Request
* [**User**](./#user)**:** (if authenticated) the End-User

**Post Token**

The Post Token step is executed after the token is generated and before it is returned to the client.

Available attributes while processing the policy chain:

* [**Request**](./#request)**:** current HTTP Request
* [**Client**](./#client)**:** the application
* [**Authorization Request**](./#oauth-2.0-authorization-request)**:** OAuth 2.0 Authorization Request
* [**User**](./#user)**:** (if authenticated) the End-User

</details>

<details>

<summary>WEBAUTHN REGISTER</summary>

The **WEBAUTHN REGISTER** flow is triggered during registration of a WebAuthN device (e.g., security key or biometric device). Policies may run before showing the WebAuthN registration page or after device registration.

**Pre WebAuthN Register**

The Pre WebAuthN Register step is executed before displaying the WebAuthN registration page to the user.

Available attributes while processing the policy chain:

* [**Request**](./#request)**:** current HTTP Request
* [**Client**](./#client)**:** the application
* [**User**](./#user)**:** the authenticated user

**Post WebAuthN Register**

The Post WebAuthN Register step is executed after the user completes registration of their WebAuthN device.

Available attributes while processing the policy chain:

* [**Request**](./#request)**:** current HTTP Request
* [**Client**](./#client)**:** the application
* [**User**](./#user)**:** the authenticated user

</details>

<details>

<summary>MFA CHALLENGE</summary>

The **MFA CHALLENGE** flow allows you to fetch additional information or validate incoming data during Multi-Factor Authentication (MFA) code verification. Policies can execute before the MFA challenge form is displayed or after the user submits the MFA code.

**Pre MFA Challenge**

The Pre MFA Challenge step is executed before the MFA Challenge HTML page is displayed, where the user will enter their MFA code.

The following attributes are available while processing the policy chain:

* [**Request**](./#request): current HTTP Request
* [**Client**](./#client): the application
* [**User**](./#user): authenticated user

**Post MFA Challenge**

The Post MFA Challenge step is executed after the user successfully submits a valid MFA code.

The following attributes are available while processing the policy chain:

* [**Request**](./#request): current HTTP Request
* [**Client**](./#client): the application
* [**User**](./#user): authenticated user

</details>

<details>

<summary>MFA ENROLLMENT</summary>

The **MFA ENROLLMENT** flow applies when a user enrolls a new MFA method. It allows you to execute additional operations such as Enroll MFA and MFA Challenge, enabling support for multiple factors during authentication. Policies can be triggered before showing the enrollment page or after the user completes enrollment.

**Pre MFA Enrollment**

The Pre MFA Enrollment step is executed before the MFA enrollment page is displayed to the user.

The following attributes are available while processing the policy chain:

* [**Request**](./#request): current HTTP Request
* [**Client**](./#client): the application
* [**User**](./#user): authenticated user

**Post MFA Enrollment**

The Post MFA Enrollment step is executed after the user completes the selection of the MFA factor for enrollment.

The following attributes are available while processing the policy chain:

* [**Request**](./#request): current HTTP Request
* [**Client**](./#client): the application
* [**User**](./#user): authenticated user

</details>

<figure><img src="../../.gitbook/assets/Screenshot 2025-08-04 at 08.48.36.png" alt=""><figcaption><p>Policy Studio</p></figcaption></figure>

## Execution context information

This section describes the objects provided by the execution context.

### Request

The following table shows the properties of the Request object.

| Property | Description                                | Type            | Always present |
| -------- | ------------------------------------------ | --------------- | -------------- |
| id       | Request identifier                         | string          | X              |
| headers  | Request headers                            | key / value     | X              |
| params   | Request query parameters + Form attributes | key / value     | X              |
| path     | Request path                               | string          | X              |
| paths    | Request path parts                         | array of string | X              |

**Example 1:** Get the value of the `Content-Type` header for an incoming HTTP request: `{#request.headers['content-type']}`

**Example 2:** Get the second part of the request path: `{#request.paths[1]}`

### Client

The following table shows the properties of the Client object.

| Property   | Description                         | Type   | Always present |
| ---------- | ----------------------------------- | ------ | -------------- |
| id         | Client technical identifier         | string | X              |
| clientId   | Client OAuth 2.0 client\_id headers | string | X              |
| clientName | Client’s name                       | string |                |

**Example:** Get the value of the `client_id` of the client: `{#context.attributes['client'].clientId}`

### User

The following table shows the properties of the User object.

| Property              | Description                | Type        | Always present |
| --------------------- | -------------------------- | ----------- | -------------- |
| id                    | User technical identifier  | string      | X              |
| username              | User’s username            | string      | X              |
| email                 | User’s email               | string      |                |
| firstName             | User’s first name          | string      |                |
| lastName              | User’s last name           | string      |                |
| displayName           | User’s display name        | string      |                |
| additionalInformation | User additional attributes | key / value | X              |

**Example:** Get the value of the `user` of the user : `{#context.attributes['user'].username}`

### OAuth 2.0 Authorization Request

The following table shows the properties of the OAuth 2.0 Authorization Request object.

| Property     | Description                | Type            | Always present |
| ------------ | -------------------------- | --------------- | -------------- |
| responseType | OAuth 2.0 response type    | string          | X              |
| scopes       | OAuth 2.0 requested scopes | array of string |                |
| clientId     | OAuth 2.0 client\_id       | string          | X              |
| redirectUri  | OAuth 2.0 redirect\_uri    | string          | X              |
| state        | OAuth 2.0 state            | string          |                |

**Example:** Get the value of the first `scopes` param for the OAuth 2.0 authorization request: `{#context.attributes['authorizationRequest'].scopes[0]}`
