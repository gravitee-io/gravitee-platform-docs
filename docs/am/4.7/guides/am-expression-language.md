# AM Expression Language

## Overview

The AM Expression Language (EL for short) is one of the key features that can be used to configure various aspects of an AM domain.

## Usage

The basic expression language syntax is as follows:

```
{#request.method}

{#context.attributes['user']}
```

See the sections below for example expression notations.

## Information available through the Expression Language

To use the EL, it is important to know which information is available. In this section, you can find a summary of what is available through the AL on AM.

{% hint style="info" %}
This page contains the most used elements, for some specific EL there is other information available. To be aware of this information, you can refer to the UI documentation by clicking on the information icon (the letter "i" into a circle) available in the EL field description.
{% endhint %}

### **Request information**

It is sometimes useful to access the request information through the EL. As an example, you may want to check the presence of a scope in the authorization request to enforce MFA (`{#request.params['scope'][0] == 'write'}`)

| Attribute | Description                                          | Syntax                                  |
| --------- | ---------------------------------------------------- | --------------------------------------- |
| headers   | Headers of the HTTP request (MultiValueMap)          | {#request.headers\['MyHeaderName']\[0]} |
| params    | Query parameters of the HTTP request (MultiValueMap) | {#request.params\['MyParam']\[0]}       |
| scheme    | Scheme of the request (http, https)                  | {#request.scheme}                       |
| method    | Method of the request (POST, GET, …​)                | {#request.method}                       |
| path      | Path of the request                                  | {#request.path}                         |
| paths     | Array of string that contains each path element      | {#request.paths\[0]}                    |

### **Application information**

You can access the client/app properties using this EL `{#context.attributes['client']}`. This expression will return a ClientProperties object with the following attributes:

| Attribute  | Description                                                     | Syntax                                                             |
| ---------- | --------------------------------------------------------------- | ------------------------------------------------------------------ |
| id         | Client/App Internal identifier                                  | {#context.attributes\['client']\['id']}                            |
| domain     | Domain Internal identifier on which the application is attached | {#context.attributes\['client']\['domain']}                        |
| clientId   | The client\_id of the application                               | {#context.attributes\['client']\['clientId']}                      |
| clientName | The name of the application                                     | {#context.attributes\['client']\['clientName']}                    |
| name       | The name of the application (Same as clientName)                | {#context.attributes\['client']\['name']}                          |
| metadata   | Map of Metadata associated to the application                   | {#context.attributes\['client']\['metadata']\['my-metadata-name']} |

### **User Profile information**

You can access to the User information using this EL `{#context.attributes['user']}`. This expression will return a UserProperties object with following attributes:

| Attribute             | Description                                                                                                                  | Syntax                                                                           |
| --------------------- | ---------------------------------------------------------------------------------------------------------------------------- | -------------------------------------------------------------------------------- |
| id                    | User Internal identifier                                                                                                     | {#context.attributes\['user']\['id']}                                            |
| externalId            | User Identifier coming from the IdentityProvider                                                                             | {#context.attributes\['user']\['externalId']}                                    |
| domain                | Domain Internal identifier on which the user is attached                                                                     | {#context.attributes\['user']\['domain']}                                        |
| username              | Username                                                                                                                     | {#context.attributes\['user']\['username']}                                      |
| firstname             | First name                                                                                                                   | {#context.attributes\['user']\['firstname']}                                     |
| lastname              | Last name                                                                                                                    | {#context.attributes\['user']\['lastname']}                                      |
| email                 | email address                                                                                                                | {#context.attributes\['user']\['email']}                                         |
| source                | Internal ID of the Identity provider that identifies the user                                                                | {#context.attributes\['user']\['source']}                                        |
| preferredLanguage     | Preferred Language defined in the user profile                                                                               | {#context.attributes\['user']\['preferredLanguage']}                             |
| roles                 | List of roles owned by the users (role name)                                                                                 | {#context.attributes\['user']\['roles']\[0]}                                     |
| groups                | List of groups on which the user is member of (group name)                                                                   | {#context.attributes\['user']\['groups']\[0]}                                    |
| additionalInformation | Map of additional information as displayed on the user detail page of the Management Console                                 | {#context.attributes\['user']\['additionalInformation']\['preferred\_username']} |
| claims                | Map of additional information as displayed on the user detail page of the Management Console (same as additionalInformation) | {#context.attributes\['user']\['claims']\['preferred\_username']}                |

{% hint style="info" %}
As you may have noticed, `claims` and `additionalInformation` contain the same data. Depending on the place where the Expression Language is defined, the `claims` attribute may not be accessible whereas the `additionalInformation` attribute will always be present.
{% endhint %}

### **Context attributes**

The Context attributes contain all the information you can add to AM Flows using policies.

* You can use the `authFlow` attribute to accumulate information across the authentication flow thanks to the Enrich Authentication Flow Policy.
* The `authFlow.requestParameters` attribute contains the request parameters defined using the [PAR specification](https://datatracker.ietf.org/doc/html/rfc9126).

| Attribute                  | Description                                            | Syntax                                                             |
| -------------------------- | ------------------------------------------------------ | ------------------------------------------------------------------ |
| authFlow                   | Map of data managed by the Enrich Authentication Flow. | {#context.attributes\['authFlow']\['my-data']}                     |
| authFlow.requestParameters | Parameters provided through PAR specification          | {#context.attributes\['authFlow']\['requestParameters']\['scope']} |

## Add information into the EL context

Thanks to the flows and policies, you can add attributes to the context. For example, using the CalloutHttpPolicy, you can create an attribute using the response of the callout :

Attr Key : `callout-attribute`

Attr Value: `{#jsonPath(#calloutResponse.content, '$.field')}`

<figure><img src="https://docs.gravitee.io/images/am/current/graviteeio-am-userguide-el-callout.png" alt=""><figcaption><p>EL with HTTP callout policy</p></figcaption></figure>

After the CalloutHttpPolicy execution, this attribute is available with the expression : `{#context.attributes['callout-attribute']}`

## How to add token claims using external data

For some use cases, the access\_token or id\_token must contain claims coming from external data sources. To do so, the Login flow must contain the Callout HTTP Policy to request the Data to an external service and the Enrich Authentication Flow Policy to preserve the data until the token generation.

In the Callout HTTP Policy, configure a variable :

Attr Key : `callout-attribute`

Attr Value: `{#jsonPath(#calloutResponse.content, '$.field')}`

<figure><img src="https://docs.gravitee.io/images/am/current/graviteeio-am-userguide-el-callout.png" alt=""><figcaption><p>EL with HTTP callout policy</p></figcaption></figure>

In the Enrich Authentication Flow Policy, configure a variable :

Attr Key: `authflow-attribute`

Attr Value: `{#context.attributes['callout-attribute']}`

<figure><img src="https://docs.gravitee.io/images/am/current/graviteeio-am-userguide-el-authflow.png" alt=""><figcaption><p>EL with Enrich Authentication flow</p></figcaption></figure>

In the tokens tab of the application OAuth 2.0 settings `domains > mydomain > applications > myapp > settings > oauth2`, use EL to get information from the authentication flow context

Claim : `uuid`

Claim Value: `{#context.attributes['authFlow']['authflow-attribute']}`

\\

<figure><img src="https://docs.gravitee.io/images/am/current/graviteeio-am-userguide-el-token.png" alt=""><figcaption><p>Application tokens</p></figcaption></figure>
