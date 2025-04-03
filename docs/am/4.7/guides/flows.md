# Flows

## Overview

You can use _flows_ to extend the standard AM behavior by executing policies during the `OnRequest` step of selected stages. Flows can be configured at the security domain level or application level.

## Execution context

Each policy has access to the `Execution Context` to retrieve and set information required to execute the policy code.

The `Execution Context` data will be propagated to the next steps to be used later on (e.g custom HTML forms).

In this example, we are getting `Execution Context` data using the Gravitee Expression Language:

{% code overflow="wrap" %}
```
{#request}: Current HTTP Request with parameters, headers, path, ...
{#context.attributes['client']}: OAuth 2.0 Client (if available) with clientId, clientName, ...
{#context.attributes['user']}: Authenticated User (if available) with username, firstName, lastName, email, roles, ...
```
{% endcode %}

<figure><img src="https://docs.gravitee.io/images/am/current/graviteeio-am-userguide-policies.png" alt=""><figcaption><p>Policy Studio</p></figcaption></figure>

## Flow configuration

Policies are executed only against selected steps throughout the flow.

AM includes four flow types:

* **All Flow:** This happens for each request.
* **Login Flow:** This happens during the user login phase. It allows you to execute policies before displaying the login form or after user authentication.
* **Consent Flow:** This happens during the user consent phase. It allows you to execute policies before displaying the User Consent HTML Page or after the user has given his consent to the processing of personal data.
* **Registration Flow:** This happens during the user registration phase. It allows you to execute policies before displaying the User Registration HTML Page or after the user data has been processed.

<figure><img src="https://docs.gravitee.io/images/am/current/graviteeio-am-userguide-policies.png" alt=""><figcaption><p>Policy Studio</p></figcaption></figure>

### All flow

The **ALL** flow is executed on each incoming request for one of the login, consent or register flows.

### Login flow

The **LOGIN** flow allows you to fetch more information or validate incoming data during the End-User authentication phase.

#### Pre Login

The Pre step allows you to fetch more information before displaying the Login HTML Page.

The following attributes are available while processing the policy chain:

* [Request](flows.md#request): current HTTP Request
* [Client](flows.md#client): the application

#### Post Login

Post End-User Consent happens after the user has given his consent to the processing of personal data. It allows you to validate incoming data (user consent) before giving access to the application.

The following attributes are available while processing the policy chain :

* [Request](flows.md#request): current HTTP Request
* [Client](flows.md#client): the application
* [User](flows.md#user): the End-User

### Consent flow

The **CONSENT** flow allows you to fetch more information or validate incoming data during the End-User consent phase. This flow happens after the user has logged in.

#### Pre End-User Consent

Pre End-User Consent allows you to fetch more information or validate incoming data before displaying the User Consent HTML Page.

The following attributes are available while processing the policy chain:

* [Request](flows.md#request): current HTTP Request
* [Client](flows.md#client): the application
* [User](flows.md#user): the End-User
* [Authorization Request](flows.md#oauth-2.0-authorization-request): OAuth 2.0 Authorization Request

#### Post End-User Consent

Post End-User Consent happens after the user has given his consent to the processing of personal data. It allows you to validate incoming data (user consent) before giving access to the application.

The following attributes are available while processing the policy chain:

* [Request](flows.md#request): current HTTP Request
* [Client](flows.md#client): the application
* [User](flows.md#user): the End-User
* [Authorization Request](flows.md#oauth-2.0-authorization-request): OAuth 2.0 Authorization Request

### Register flow

The **REGISTER** flow allows you to fetch more information or validate incoming data during the End-User registration phase.

#### Pre End-User Registration

Pre End-User Registration step is executed before displaying the User Consent HTML Page.

The following attributes are available while processing the policy chain:

* [Request](flows.md#request): current HTTP Request
* [Client](flows.md#client): the application

#### Post End-User Registration

Post End-User Registration step is executed once the user submit the registration form and information are preserve in database.

The following attributes are available while processing the policy chain :

* [Request](flows.md#request): current HTTP Request
* [Client](flows.md#client): the application
* [User](flows.md#user): the End-User

### Execution context information

This section describes the objects provided by the execution context.

#### Request

**Properties**

| Property | Description                                | Type            | Always present |
| -------- | ------------------------------------------ | --------------- | -------------- |
| id       | Request identifier                         | string          | X              |
| headers  | Request headers                            | key / value     | X              |
| params   | Request query parameters + Form attributes | key / value     | X              |
| path     | Request path                               | string          | X              |
| paths    | Request path parts                         | array of string | X              |

**Example**

* Get the value of the `Content-Type` header for an incoming HTTP request: `{#request.headers['content-type']}`
* Get the second part of the request path: `{#request.paths[1]}`

#### Client

**Properties**

| Property   | Description                         | Type   | Always present |
| ---------- | ----------------------------------- | ------ | -------------- |
| id         | Client technical identifier         | string | X              |
| clientId   | Client OAuth 2.0 client\_id headers | string | X              |
| clientName | Client’s name                       | string |                |

**Example**

* Get the value of the `client_id` of the client: `{#context.attributes['client'].clientId}`

#### User

**Properties**

| Property              | Description                | Type        | Always present |
| --------------------- | -------------------------- | ----------- | -------------- |
| id                    | User technical identifier  | string      | X              |
| username              | User’s username            | string      | X              |
| email                 | User’s email               | string      |                |
| firstName             | User’s first name          | string      |                |
| lastName              | User’s last name           | string      |                |
| displayName           | User’s display name        | string      |                |
| additionalInformation | User additional attributes | key / value | X              |

**Example**

* Get the value of the `user` of the user : `{#context.attributes['user'].username}`

#### OAuth 2.0 Authorization Request

**Properties**

| Property     | Description                | Type            | Always present |
| ------------ | -------------------------- | --------------- | -------------- |
| responseType | OAuth 2.0 response type    | string          | X              |
| scopes       | OAuth 2.0 requested scopes | array of string |                |
| clientId     | OAuth 2.0 client\_id       | string          | X              |
| redirectUri  | OAuth 2.0 redirect\_uri    | string          | X              |
| state        | OAuth 2.0 state            | string          |                |

**Example**

* Get the value of the first `scopes` param for the OAuth 2.0 authorization request: `{#context.attributes['authorizationRequest'].scopes[0]}`\\
