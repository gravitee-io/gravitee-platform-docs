---
description: Implement the backend-for-frontend pattern for single-page apps with an API Management 4.10 shared policy group. Learn what it handles.
---

# Implement BFF pattern (with a Shared Policy Group)

## Overview

In recent years, it was common to implement OpenID Connect for single-page apps (SPAs) in JavaScript (React, Angular, Vue, etc.). This approach is no longer recommended.

For more information, see the [OAuth browser-based apps draft.](https://datatracker.ietf.org/doc/draft-ietf-oauth-browser-based-apps/)

* Using access tokens in the browser has more security risks than using secure cookies.
* A SPA is a public client and cannot keep a secret. Any secret would be part of the JavaScript and accessible to anyone inspecting the source code.
* Recent browser changes to prevent tracking may result in third-party cookies being dropped during token renewal.
* Browsers cannot store data securely for long periods. Stored data is vulnerable to various attacks.
* Browsers have introduced stronger [SameSite cookies](https://datatracker.ietf.org/doc/html/draft-west-first-party-cookies-07), and using tokens in the browser is now considered less secure in comparison.&#x20;

Due to the above issues, the recommended security approach for SPAs is to avoid storing access tokens in the browser and instead create a lightweight backend component called Backend for Frontend (BFF).

{% hint style="info" %}
The **BFF pattern** can also serve as a valuable approach in scenarios where backend APIs or applications lack existing protection, providing a transparent and secure mechanism for consumers to access them through web browsers.
{% endhint %}

<figure><img src="../../.gitbook/assets/how-to-guides-use-case-tutorials-impleme-1-3.png" alt="A diagram of the backend-for-frontend pattern, where a single-page application served from a CDN exchanges credentials with API Management, whose OAuth agent and proxy call an authorization server and return a secure cookie holding a signed access token."><figcaption><p>BFF - High level architecture</p></figcaption></figure>

#### BFF Shared Policy Group responsibilities

* **OAuth Agent:** Forwards OAuth requests to the Authorization Server when requested by the SPA. The agent creates the actual OAuth request messages and any secrets used, then receives tokens in response messages. Secure cookies are then returned to the browser and cannot be accessed by the SPA's JavaScript code.
* **OAuth Proxy:** Receives a secure cookie from the SPA and propagates the access token to backend APIs.

## Implementation

This guide assumes that the `clientId` property has been created in your API. This `clientId` redirects the user to the Authorization Server. This implementation creates a session cookie. (Optional): You can edit the  [shared policy group](../../create-and-configure-apis/apply-policies/shared-policy-groups.md) to configure the cookie with an expiration date.

### Task 1: Create an On-Request Shared Policy Group

1. Navigate to the shared policy groups by clicking on Settings, and then **Shared Policy Groups**.

<figure><img src="../../.gitbook/assets/how-to-guides-use-case-tutorials-impleme-2-3.png" alt="The Shared Policy Groups settings, listing four deployed proxy request groups for GeoIP rate limiting and three AI examples, with an Add Shared Policy Group button."><figcaption></figcaption></figure>

2. Click **Add Shared Policy Group**, and select **Proxy API**.
3. Specify a name for this SPG, and ensure the **Request** phase is selected.  Then click on the **\[Save]** button.

<figure><img src="../../.gitbook/assets/how-to-guides-use-case-tutorials-impleme-3-3.png" alt="The Add Shared Policy Group for Proxy API dialog, with a BFF on-request name, a description about protecting APIs with a JWT cookie, an empty prerequisite message, and the Request phase selected."><figcaption></figcaption></figure>

4. Add the [**Groovy**](../../create-and-configure-apis/apply-policies/policy-reference/4.9-groovy.md) **Policy**
   1. Use the following GroovyScript to get the Auth BFF cookie

```groovy
def cookieHeader = request.headers['Cookie'][0]
def getCookieValue(cookieHeader, cookieName) {
    if (!cookieHeader) {
        return nulln
    }
    for (String part: cookieHeader.split(';')) {
        String trimmed = part.trim()
        String[] pieces = trimmed.split('=', 2)
        if (pieces.length == 2) {
            String name = pieces[0]
            String value = pieces[1]
            if (name == cookieName) {
                return value
            }
        }
    }
    return null
}
def bffCookie = getCookieValue(cookieHeader, "X-Gravitee-BFF-Cookie")
context.attributes['bffCookie'] = bffCookie
```

&#x20;     b. Click on the **\[Add policy]** button, and progress to the next step.

<figure><img src="../../.gitbook/assets/how-to-guides-use-case-tutorials-impleme-4-4.png" alt="The Groovy policy configuration, described as getting the BFF cookie, with read and override content both switched off and a script that parses the cookie header for a named value." width="188"><figcaption><p>Groovy Policy - Get Auth BFF cookie</p></figcaption></figure>

5. Add the [**Mock**](../../create-and-configure-apis/apply-policies/policy-reference/mock.md) **Policy**
   1. Set the **Trigger condition** to `{#context.attributes['bffCookie'] == null && #request.params['code'] == null}`
   2. Set the **HTTP Status Code** to `302-MOVED_TEMPORARILY` &#x20;
   3. Add a new **Header** named `Location`, with value of `https://auth.server.com/oauth/authorize?client_id={#api.properties['clientId']}&response_type=code&redirect_uri={#request.scheme + '://' + #request.host + #request.path}`
   4. Click on the **\[Add policy]** button, and progress to the next step.

<figure><img src="../../.gitbook/assets/how-to-guides-use-case-tutorials-impleme-6-3.png" alt="The Mock policy configuration, described as redirecting to the authorization server, with a trigger condition on a missing cookie, a 302 status code, and a Location header pointing to an authorize endpoint, beside the policy documentation." width="188"><figcaption><p>Mock Policy - Redirect to Auth Server if no cookie</p></figcaption></figure>

6. Add the [**HTTP Callout**](../../create-and-configure-apis/apply-policies/policy-reference/http-callout.md) **Policy**
   1. Set the **Trigger condition** to `{#context.attributes['bffCookie'] == null && #request.params['code'] != null}`
   2. Set the **HTTP Method** to `POST`
   3. Set the **URL** to the Auth Server token endpoint. E.g.: `https://auth.server.com/oauth/token`
   4. Add a new **Header** named `Content-Type`, with value of `application/x-www-form-urlencoded`
   5. Set the **Request body** to `grant_type=authorization_code&code={#request.params['code'][0]}&client_id={#api.properties['clientId']}&redirect_uri={#request.scheme + '://' + #request.host + #request.path}`
   6. Add a new **Context Variable** named `accessToken`, with value of `{#jsonPath(#calloutResponse.content, '$.access_token')}`
   7. Click on the **\[Add policy]** button, and progress to the next step.

<figure><img src="../../.gitbook/assets/how-to-guides-use-case-tutorials-impleme-7-4.png" alt="The HTTP Callout policy configuration for exchanging an authorization code, with a POST to a token endpoint, a form-encoded content type header, a request body carrying the grant type and code, and a context variable capturing the access token." width="188"><figcaption><p>HTTP Callout Policy - Exchange code for a token</p></figcaption></figure>

7. Add the [**Transform Headers**](../../create-and-configure-apis/apply-policies/policy-reference/transform-headers.md) **Policy**
   1. Set the **Trigger condition** to `{#context.attributes['bffCookie'] != null}`
   2. Within the **Set/replace headers** section, add a new **Key** named `Authorization` with a value of `Bearer {#context.attributes['bffCookie']}`
   3. Click on the **\[Add policy]** button, and progress to the next step.

<figure><img src="../../.gitbook/assets/how-to-guides-use-case-tutorials-impleme-9-5.png" alt="The Transform Headers policy configuration, with a trigger condition on the cookie attribute and an Authorization header set to a Bearer token read from that cookie." width="188"><figcaption><p>Transform Headers Policy - Add Bearer token fetch from the cookie if any</p></figcaption></figure>

8. Add the [**JSON Web Tokens**](../../create-and-configure-apis/apply-policies/policy-reference/jws-validator.md) **Policy**
   1. Set the **Trigger condition** to `{#context.attributes['bffCookie'] != null}`
   2. Set the **JWKS resolver** to `JWKS_URL`
   3. Set the **Resolver parameter** to `https://auth.server.com/.well-known/jwks.json`
   4. Click on the **\[Add policy]** button, and progress to the next step.

<figure><img src="../../.gitbook/assets/how-to-guides-use-case-tutorials-impleme-11-3.png" alt="The JSON Web Tokens policy configuration, with the RSA_RS256 signature, the JWKS_URL resolver, a resolver parameter, authorization header propagation on, and the user claim set to sub." width="188"><figcaption><p>JSON Web Tokens Policy - Verify Auth BFF cookie</p></figcaption></figure>

9. Now that all the policies have been added, click on the **\[Save]** button.
10. Click the **\[Deploy]** button.

<figure><img src="../../.gitbook/assets/how-to-guides-use-case-tutorials-impleme-12-3.png" alt="An undeployed BFF on-request shared policy group, showing Groovy, Mock, HTTP Callout, Transform Headers, and JSON Web Tokens policies in the request phase, each with its trigger condition above, and a Deploy button."><figcaption><p>BFF On-Request Shared Policy Group</p></figcaption></figure>

<details>

<summary>You can find the full JSON definition for the <strong>BFF On-Request Shared Policy Group</strong> here</summary>

```json
{
  "name": "BFF On-Request Shared Policy Group",
  "description": "Protect your APIs with a JWT cookie, if no cookie, redirect the user to the authorization server",
  "prerequisiteMessage": "",
  "version": 1,
  "apiType": "PROXY",
  "originContext": {
    "origin": "MANAGEMENT"
  },
  "steps": [
    {
      "name": "Groovy",
      "description": "Get Auth BFF cookie",
      "enabled": true,
      "policy": "groovy",
      "configuration": {
        "scope": "REQUEST",
        "script": "def cookieHeader = request.headers['Cookie'][0]\n\ndef getCookieValue(cookieHeader, cookieName) {\n    if (!cookieHeader) {\n        return null\n    }\n\n    for (String part : cookieHeader.split(';')) {\n        String trimmed = part.trim()\n        String[] pieces = trimmed.split('=', 2)\n        if (pieces.length == 2) {\n            String name = pieces[0]\n            String value = pieces[1]\n            if (name == cookieName) {\n                return value\n            }\n        }\n    }\n    return null\n}\n\ndef bffCookie = getCookieValue(cookieHeader, \"X-Gravitee-BFF-Cookie\")\ncontext.attributes['bffCookie'] = bffCookie\n"
      }
    },
    {
      "name": "Mock",
      "description": "Redirect to Auth Server if no cookie",
      "enabled": true,
      "policy": "mock",
      "configuration": {
        "headers": [
          {
            "name": "Location",
            "value": "https://auth.server.com/oauth/authorize?client_id={#api.properties['clientId']}&response_type=code&redirect_uri={#request.scheme + '://' + #request.host + #request.path}"
          }
        ],
        "status": "302"
      },
      "condition": "{#context.attributes['bffCookie'] == null && #request.params['code'] == null}"
    },
    {
      "name": "HTTP Callout",
      "description": "Exchange code for a token",
      "enabled": true,
      "policy": "policy-http-callout",
      "configuration": {
        "headers": [
          {
            "name": "Content-Type",
            "value": "application/x-www-form-urlencoded"
          }
        ],
        "variables": [
          {
            "name": "accessToken",
            "value": "{#jsonPath(#calloutResponse.content, '$.access_token')}"
          }
        ],
        "method": "POST",
        "fireAndForget": false,
        "scope": "REQUEST",
        "errorStatusCode": "500",
        "body": "grant_type=authorization_code&code={#request.params['code'][0]}&client_id={#api.properties['clientId']}&redirect_uri={#request.scheme + '://' + #request.host + #request.path}",
        "errorCondition": "{#calloutResponse.status >= 400 and #calloutResponse.status <= 599}",
        "url": "https://auth.server.com/oauth/token",
        "exitOnError": false
      },
      "condition": "{#context.attributes['bffCookie'] == null && #request.params['code'] != null}"
    },
    {
      "name": "Transform Headers",
      "description": "Add Bearer token fetch from the cookie if any",
      "enabled": true,
      "policy": "transform-headers",
      "configuration": {
        "whitelistHeaders": [],
        "addHeaders": [
          {
            "name": "Authorization",
            "value": "Bearer {#context.attributes['bffCookie']}"
          }
        ],
        "scope": "REQUEST",
        "removeHeaders": []
      },
      "condition": "{#context.attributes['bffCookie'] != null}"
    },
    {
      "name": "JSON Web Tokens",
      "description": "Verify Auth BFF cookie",
      "enabled": true,
      "policy": "jwt",
      "configuration": {
        "signature": "RSA_RS256",
        "publicKeyResolver": "JWKS_URL",
        "extractClaims": false,
        "propagateAuthHeader": true,
        "resolverParameter": "https://auth.server.com/.well-known/jwks.json",
        "followRedirects": false,
        "connectTimeout": 2000,
        "tokenTypValidation": {
          "ignoreCase": false,
          "expectedValues": ["JWT"],
          "enabled": false,
          "ignoreMissing": false
        },
        "useSystemProxy": false,
        "requestTimeout": 2000,
        "confirmationMethodValidation": {
          "certificateBoundThumbprint": {
            "extractCertificateFromHeader": false,
            "headerName": "ssl-client-cert",
            "enabled": false
          },
          "ignoreMissing": false
        },
        "userClaim": "sub"
      },
      "condition": "{#context.attributes['bffCookie'] != null}"
    }
  ],
  "phase": "REQUEST",
  "lifecycleState": "DEPLOYED"
}
```

You can import this Shared Policy Group using Gravitee's Management API.

> Save the above JSON definition to a file named `bff-on-request.json`, and then use the following command:
>
> `curl -X POST "http://{gravitee_mAPI_hostname}/management/v2/organizations/DEFAULT/environments/DEFAULT/shared-policy-groups" -H "Authorization: {your_personal_token}" -H "Content-Type: application/json" -d @bff-on-request.json`

</details>

### Task 2: Create an On-Response shared policy group

1. Navigate back to the shared policy groups by clicking on Settings, and then **Shared Policy Groups**.

<figure><img src="../../.gitbook/assets/how-to-guides-use-case-tutorials-impleme-13-3.png" alt="The Shared Policy Groups settings listing five deployed proxy request groups, with the new BFF on-request policy at the top."><figcaption></figcaption></figure>

2. Click **Add Shared Policy Group**, and select **Proxy API**.
3. Specify a name for this SPG, and ensure the **Response** phase is selected.  Then click on the **\[Save]** button.

<figure><img src="../../.gitbook/assets/how-to-guides-use-case-tutorials-impleme-14-3.png" alt="The Add Shared Policy Group for Proxy API dialog, with a BFF on-response name and description and the Response phase selected."><figcaption></figcaption></figure>

4. Add the [**Transform Headers**](../../create-and-configure-apis/apply-policies/policy-reference/transform-headers.md) **Policy**
   1. Set the **Trigger condition** to `{#context.attributes['accessToken'] != null}`
   2. Within the **Set/replace headers** section, add a new **Key** named `Set-Cookie` with a value of `X-Gravitee-BFF-Cookie={#context.attributes['accessToken']}; Path=/; HttpOnly; SameSite=Strict`
   3. Click on the **\[Add policy]** button, and progress to the next step.

<figure><img src="../../.gitbook/assets/how-to-guides-use-case-tutorials-impleme-15-2.png" alt="The Transform Headers policy configuration for the response phase, setting a Set-Cookie header that stores the access token as an HttpOnly, SameSite strict cookie." width="188"><figcaption><p>Transform Headers Policy - Add OAuth 2.0 access token in Auth BFF cookie</p></figcaption></figure>

5. Now that all the policies have been added, click on the **\[Save]** button.
6. Click the **\[Deploy]** button.

<figure><img src="../../.gitbook/assets/how-to-guides-use-case-tutorials-impleme-16-2.png" alt="A deployed BFF on-response shared policy group, showing a single Transform Headers policy in the response phase with a condition on a non-null access token."><figcaption><p>BFF On-Response Shared Policy Group</p></figcaption></figure>

<details>

<summary>You can find the full JSON definition for the <strong>BFF On-Response Shared Policy Group</strong> here</summary>

```json
{
    "name": "BFF On-Response Shared Policy Group",
    "description": "Protect your APIs with a JWT cookie, if no cookie, redirect the user to the authorization server",
    "prerequisiteMessage": "",
    "version": 1,
    "apiType": "PROXY",
    "originContext": {
        "origin": "MANAGEMENT"
    },
    "steps": [
        {
            "name": "Transform Headers",
            "description": "Add OAuth 2.0 access token in Auth BFF cookie",
            "enabled": true,
            "policy": "transform-headers",
            "configuration": {
                "whitelistHeaders": [],
                "addHeaders": [
                    {
                        "name": "Set-Cookie",
                        "value": "X-Gravitee-BFF-Cookie={#context.attributes['accessToken']}; Path=/; HttpOnly; SameSite=Strict"
                    }
                ],
                "scope": "REQUEST",
                "removeHeaders": []
            },
            "condition": "{#context.attributes['accessToken'] != null}"
        }
    ],
    "phase": "RESPONSE",
    "lifecycleState": "DEPLOYED"
}
```

You can import this Shared Policy Group using Gravitee's Management API.

> Save the above JSON definition to a file named `bff-on-response.json`, and then use the following command:
>
> `curl -X POST "http://{gravitee_mAPI_hostname}/management/v2/organizations/DEFAULT/environments/DEFAULT/shared-policy-groups" -H "Authorization: {your_personal_token}" -H "Content-Type: application/json" -d @bff-on-response.json`

</details>

### Task 3: Use the Shared Policy Groups in your API

Now it is time to add these Shared Policy Groups into your existing API.

1. Navigate to your API.
2. Click into **Policies**.
3. Create a new Flow, or select an existing Flow to edit.
4. Add your recently created Shared Policy Groups:
   1. Add the '**BFF On-Request Shared Policy Group**' into the **Request** **Phase**, and
   2. Add the '**BFF On-Response Shared Policy Group**' into the **Response Phase**.
5. Click on the **\[Save]** button.
6. Finally, click on the **\[Deploy API]** popup, to deploy these configuration changes to your Gateway.

<figure><img src="../../.gitbook/assets/how-to-guides-use-case-tutorials-impleme-17-2.png" alt="The Policies page of an API, with a BFF flow selected showing the on-request shared policy group in the request phase and the on-response group in the response phase."><figcaption><p>BFF Shared Policy Groups applied on your API</p></figcaption></figure>

To quickly test the flow, just call your API via a Web Browser and you should be redirected to the login page of your Authorization Server if no cookie has been found.
