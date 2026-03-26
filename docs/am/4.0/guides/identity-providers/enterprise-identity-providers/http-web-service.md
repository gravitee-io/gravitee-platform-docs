---
description: API and reference documentation for You.
---

# HTTP (web service)

## Overview

You can authenticate and manage users in AM using remote API calls.

{% hint style="info" %}
For the Identity Provider to work, the user’s payload must at least contain the following claims: _`sub`_. To obtain more information about your user you can use the link: [Standard Claims](https://openid.net/specs/openid-connect-core-1_0.html#StandardClaims) of the OpenID Connect protocol. You can achieve this with the AM User Mapper feature.
{% endhint %}

<figure><img src="https://docs.gravitee.io/images/am/current/graviteeio-am-userguide-http-idp-mapping.png" alt=""><figcaption><p>HTTP IdP</p></figcaption></figure>

## Create an HTTP identity provider

1. Log in to AM Console.
2. Click **Settings > Providers**.
3. Click the plus icon ![plus icon](https://docs.gravitee.io/images/icons/plus-icon.png).
4. Select **HTTP** as your identity provider type and click **Next**.
5. Give your identity provider a name.
6. Configure the settings.
7. Click **Create**.

### Configuration

The HTTP Identity Provider is used to invoke an HTTP(S) URL and store the response content in one or more variables of the execution context.

The result of the authentication is stored in a variable named `authenticationResponse` and the User Management operations are stored in the _`usersResponse`_ variable.

These variables can be used to check whether the API calls have failed. The sections below list the data context and options you can configure for your identity provider.

#### **Authentication Resource**

| Property                    | Required | Description                                                                | Type         | Default                                                 |
| --------------------------- | -------- | -------------------------------------------------------------------------- | ------------ | ------------------------------------------------------- |
| baseURL                     | X        | URL invoked by the HTTP client (supports EL)                               | URL          | -                                                       |
| httpMethod                  | X        | HTTP Method used to invoke URL                                             | HTTP method  | POST                                                    |
| httpHeaders                 | -        | List of HTTP headers used to invoke the URL (supports EL)                  | HTTP Headers | -                                                       |
| httpBody                    | -        | The body content sent when calling the URL (supports EL)                   | string       | {"username":"{#principal}","password":"{#credentials}"} |
| httpResponseErrorConditions | X        | List of conditions which will be verified to end the request (supports EL) | string       | {#authenticationResponse.status == 401}                 |

| Property            | Required | Description                                                                                       | Type   | Default |
| ------------------- | -------- | ------------------------------------------------------------------------------------------------- | ------ | ------- |
| baseURL             | X        | URL invoked by the HTTP client (supports EL)                                                      | URL    |         |
| identifierAttribute | X        | Field used to retrieve user identifier into the JSON object provided into the HTTP response body. | String |         |
| usernameAttribute   | X        | Field used to retrieve username into the JSON object provided into the HTTP response body.        | String |         |

#### **Create**

| Property                    | Required | Description                                                                | Type         | Default                                                                                                                 |
| --------------------------- | -------- | -------------------------------------------------------------------------- | ------------ | ----------------------------------------------------------------------------------------------------------------------- |
| Path                        | X        | URL invoked by the HTTP client (supports EL)                               | URL          | /users                                                                                                                  |
| httpMethod                  | X        | HTTP Method used to invoke URL                                             | HTTP method  | POST                                                                                                                    |
| httpHeaders                 | -        | List of HTTP headers used to invoke the URL (supports EL)                  | HTTP Headers | -                                                                                                                       |
| httpBody                    | -        | The body content sent when calling the URL (supports EL)                   | string       | {"username":"{#user.username}","email":"{#user.email}", "firstName":"{#user.firstName}", "lastName":"{#user.lastName}"} |
| httpResponseErrorConditions | X        | List of conditions which will be verified to end the request (supports EL) | string       | {#usersResponse.status == 400}                                                                                          |

#### **Read**

{% hint style="info" %}
Only the _username_ attribute is available at this stage.
{% endhint %}

| Property                    | Required | Description                                                                | Type         | Default                          |
| --------------------------- | -------- | -------------------------------------------------------------------------- | ------------ | -------------------------------- |
| path                        | X        | URL invoked by the HTTP client (supports EL)                               | URL          | /users?username={#user.username} |
| httpMethod                  | X        | HTTP Method used to invoke URL                                             | HTTP method  | GET                              |
| httpHeaders                 | -        | List of HTTP headers used to invoke the URL (supports EL)                  | HTTP Headers | -                                |
| httpBody                    | -        | The body content sent when calling the URL (supports EL)                   | string       | -                                |
| httpResponseErrorConditions | X        | List of conditions which will be verified to end the request (supports EL) | string       | {#usersResponse.status == 404}   |

#### **Update**

| Property                    | Required | Description                                                                | Type         | Default                                                                                                                 |
| --------------------------- | -------- | -------------------------------------------------------------------------- | ------------ | ----------------------------------------------------------------------------------------------------------------------- |
| path                        | X        | URL invoked by the HTTP client (supports EL)                               | URL          | /users/{#user.id}                                                                                                       |
| httpMethod                  | X        | HTTP Method used to invoke URL                                             | HTTP method  | PUT                                                                                                                     |
| httpHeaders                 | -        | List of HTTP headers used to invoke the URL (supports EL)                  | HTTP Headers | -                                                                                                                       |
| httpBody                    | -        | The body content sent when calling the URL (supports EL)                   | string       | {"username":"{#user.username}","email":"{#user.email}", "firstName":"{#user.firstName}", "lastName":"{#user.lastName}"} |
| httpResponseErrorConditions | X        | List of conditions which will be verified to end the request (supports EL) | string       | {#usersResponse.status == 404}                                                                                          |

#### **Delete**

| Property                    | Required | Description                                                                | Type         | Default                        |
| --------------------------- | -------- | -------------------------------------------------------------------------- | ------------ | ------------------------------ |
| path                        | X        | URL invoked by the HTTP client (supports EL)                               | URL          | /users/{#user.id}              |
| httpMethod                  | X        | HTTP Method used to invoke URL                                             | HTTP method  | DELETE                         |
| httpHeaders                 | -        | List of HTTP headers used to invoke the URL (supports EL)                  | HTTP Headers | -                              |
| httpBody                    | -        | The body content sent when calling the URL (supports EL)                   | string       | -                              |
| httpResponseErrorConditions | X        | List of conditions which will be verified to end the request (supports EL) | string       | {#usersResponse.status == 404} |

## Test the connection

You can test your HTTP connection using a web application created in AM.

1.  In AM Console, click **Applications** and select your HTTP identity provider.

    <figure><img src="https://docs.gravitee.io/images/am/current/graviteeio-am-userguide-social-idp-list.png" alt=""><figcaption><p>Select application IdP</p></figcaption></figure>
2.  Call the Login page (i.e `/oauth/authorize` endpoint) and try to sign in with the username/password form.

    If you are unable to authenticate your user, there may be a problem with the identity provider settings. Check the AM Gateway log and audit logs for more information.
