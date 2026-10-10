---
description: The OAuth 2.0 Token Exchange policy exchanges the incoming token for one that a trusted authorization server issues in API Management 4.13. Learn how to set it.
---

# OAuth 2.0 Token Exchange

{% hint style="warning" %}
This policy requires an Enterprise Edition license. For more information, see [Enterprise Edition](../../../introduction/enterprise-edition.md).
{% endhint %}

## Overview

The OAuth 2.0 Token Exchange policy implements [RFC 8693](https://www.rfc-editor.org/rfc/rfc8693). On each request, it sends a subject token, usually the consumer's access token, to the token endpoint of an authorization server. By default, it then writes the token that the server issues to the `Authorization` header, in place of the consumer's token, before the request reaches the backend.

The policy reaches the authorization server in one of two ways, set by `connectionMode`:

* `RESOURCE`, the default, uses an OAuth2 resource declared on the API, which holds the connection and the client credentials.
* `INLINE` holds the token endpoint and the client credentials in the policy configuration.

## Examples

{% hint style="warning" %}
This policy applies to the request phase of v4 HTTP proxy APIs, v4 message APIs, and MCP proxies.
{% endhint %}

Sample policy configuration that exchanges the consumer's access token through an OAuth2 resource of the API:

```json
{
  "name": "OAuth 2.0 Token Exchange",
  "policy": "oauth2-token-exchange",
  "configuration": {
    "connectionMode": "RESOURCE",
    "oauth2Resource": "my-oauth2-resource",
    "subjectToken": "{#request.headers['Authorization'][0].substring(7)}",
    "subjectTokenType": "urn:ietf:params:oauth:token-type:access_token",
    "audience": "backend-service"
  }
}
```

Sample policy configuration that exchanges the token at another authorization server, configured inline:

```json
{
  "name": "OAuth 2.0 Token Exchange",
  "policy": "oauth2-token-exchange",
  "configuration": {
    "connectionMode": "INLINE",
    "tokenEndpoint": "https://idp.example.com/oauth/token",
    "clientId": "gravitee-token-exchanger",
    "clientSecret": "my-client-secret",
    "subjectToken": "{#request.headers['Authorization'][0].substring(7)}",
    "subjectTokenType": "urn:ietf:params:oauth:token-type:access_token",
    "audience": "backend-service"
  }
}
```

The `subjectToken` expression reads the consumer's token from the `Authorization` header and drops its `Bearer` prefix. Behind an OAuth2 plan, `{#context.attributes['oauth.access_token']}` returns the same token.

## Configuration

Every string option supports Gravitee Expression Language, and `clientId` and `clientSecret` also accept secret references.

### Connection

In `RESOURCE` mode, `oauth2Resource` names an OAuth2 resource of the API, which performs the exchange with its own connection, client credentials, and TLS settings. The following resource types support token exchange:

* **Gravitee.io AM Authorization Server** (`oauth2-am-resource`) exchanges at the token endpoint of its security domain.
* **OAuth2 / OpenID Connect Provider** (`oauth2`) exchanges at the path set in its **Token exchange endpoint** field, resolved against its authorization server URL. When that field is empty, every exchange fails.
* **Keycloak Adapter** (`oauth2-keycloak-resource`) exchanges at the token endpoint of its realm. This resource isn't included in the default APIM distribution.

The Auth0 and Microsoft Entra ID resources that APIM 4.13 ships don't support token exchange, and every exchange through them fails.

In `INLINE` mode, the policy sends the exchange request to `tokenEndpoint` itself. It authenticates only when both `clientId` and `clientSecret` are set, in an `Authorization: Basic` header by default, or as `client_id` and `client_secret` form parameters when `useClientAuthorizationHeader` is `false`. It validates the certificate of the token endpoint unless `trustAll` is `true`.

The options of the other mode are ignored.

### Authorization header and context attributes

After a successful exchange, the policy writes `<token type> <access token>` to the `Authorization` request header, replacing its value. The token type is the `token_type` that the authorization server returns, or `Bearer` when that value is `N_A`.

Set `authorizationHeader` to write the token to another header, or set `writeAuthorizationHeader` to `false` to write no header. In both cases, the incoming `Authorization` header reaches the backend unchanged.

The policy also stores the response in the following context attributes, which later policies can read with Expression Language, for example `{#context.attributes['token-exchange.access_token']}`:

<table>
    <thead>
        <tr>
            <th>Attribute</th>
            <th>Description</th>
        </tr>
    </thead>
    <tbody>
        <tr>
            <td><code>token-exchange.access_token</code></td>
            <td>The issued token.</td>
        </tr>
        <tr>
            <td><code>token-exchange.token_type</code></td>
            <td>The token type that the authorization server returned.</td>
        </tr>
        <tr>
            <td><code>token-exchange.issued_token_type</code></td>
            <td>The URN of the issued token type.</td>
        </tr>
        <tr>
            <td><code>token-exchange.expires_in</code></td>
            <td>The lifetime of the issued token, in seconds.</td>
        </tr>
        <tr>
            <td><code>token-exchange.scope</code></td>
            <td>The scope of the issued token, when the authorization server returns one.</td>
        </tr>
        <tr>
            <td><code>token-exchange.refresh_token</code></td>
            <td>The refresh token, when the authorization server returns one.</td>
        </tr>
    </tbody>
</table>

The policy doesn't cache issued tokens. It calls the token endpoint on every request that it runs on.

### Phases

The phases checked below are supported by the `oauth2-token-exchange` policy:

<table>
    <thead>
        <tr>
            <th>v4 Phases</th>
            <th data-type="checkbox">Compatible?</th>
        </tr>
    </thead>
    <tbody>
        <tr>
            <td>onRequest</td>
            <td>true</td>
        </tr>
        <tr>
            <td>onResponse</td>
            <td>false</td>
        </tr>
        <tr>
            <td>onMessageRequest</td>
            <td>false</td>
        </tr>
        <tr>
            <td>onMessageResponse</td>
            <td>false</td>
        </tr>
    </tbody>
</table>

### Options

You can configure the `oauth2-token-exchange` policy with the following options:

<table>
    <thead>
        <tr>
            <th>Property</th>
            <th data-type="checkbox">Required</th>
            <th>Description</th>
            <th>Default</th>
        </tr>
    </thead>
    <tbody>
        <tr>
            <td>connectionMode</td>
            <td>false</td>
            <td><code>RESOURCE</code> to exchange through an OAuth2 resource of the API, or <code>INLINE</code> to exchange with the connection set on the policy.</td>
            <td>RESOURCE</td>
        </tr>
        <tr>
            <td>oauth2Resource</td>
            <td>false</td>
            <td>Name of the OAuth2 resource that performs the exchange. Required in <code>RESOURCE</code> mode.</td>
            <td>-</td>
        </tr>
        <tr>
            <td>tokenEndpoint</td>
            <td>false</td>
            <td>Full URL of the token endpoint. Required in <code>INLINE</code> mode.</td>
            <td>-</td>
        </tr>
        <tr>
            <td>clientId</td>
            <td>false</td>
            <td><code>INLINE</code> mode. Client identifier that the Gateway authenticates with.</td>
            <td>-</td>
        </tr>
        <tr>
            <td>clientSecret</td>
            <td>false</td>
            <td><code>INLINE</code> mode. Client secret that the Gateway authenticates with.</td>
            <td>-</td>
        </tr>
        <tr>
            <td>useClientAuthorizationHeader</td>
            <td>false</td>
            <td><code>INLINE</code> mode. Sends the client credentials in an <code>Authorization: Basic</code> header. When <code>false</code>, sends them as form parameters.</td>
            <td>true</td>
        </tr>
        <tr>
            <td>verifyHost</td>
            <td>false</td>
            <td><code>INLINE</code> mode. Checks that the certificate of the token endpoint matches its host name.</td>
            <td>true</td>
        </tr>
        <tr>
            <td>trustAll</td>
            <td>false</td>
            <td><code>INLINE</code> mode. Accepts any certificate from the token endpoint.</td>
            <td>false</td>
        </tr>
        <tr>
            <td>useSystemProxy</td>
            <td>false</td>
            <td><code>INLINE</code> mode. Sends the exchange request through the proxy configured on the Gateway.</td>
            <td>false</td>
        </tr>
        <tr>
            <td>connectTimeout</td>
            <td>false</td>
            <td><code>INLINE</code> mode. Time allowed to open the connection to the token endpoint, in milliseconds.</td>
            <td>3000</td>
        </tr>
        <tr>
            <td>requestTimeout</td>
            <td>false</td>
            <td><code>INLINE</code> mode. Time allowed for the whole exchange request, in milliseconds.</td>
            <td>10000</td>
        </tr>
        <tr>
            <td>subjectToken</td>
            <td>true</td>
            <td>Token that represents the party on whose behalf the request is made.</td>
            <td>-</td>
        </tr>
        <tr>
            <td>subjectTokenType</td>
            <td>true</td>
            <td>URN of the subject token type, for example <code>urn:ietf:params:oauth:token-type:access_token</code>.</td>
            <td>-</td>
        </tr>
        <tr>
            <td>resource</td>
            <td>false</td>
            <td>URI of the target resource.</td>
            <td>-</td>
        </tr>
        <tr>
            <td>audience</td>
            <td>false</td>
            <td>Logical name of the target service.</td>
            <td>-</td>
        </tr>
        <tr>
            <td>scopes</td>
            <td>false</td>
            <td>Scopes to request for the issued token, sent as one space-separated <code>scope</code> parameter.</td>
            <td>-</td>
        </tr>
        <tr>
            <td>requestedTokenType</td>
            <td>false</td>
            <td>URN of the token type to request.</td>
            <td>-</td>
        </tr>
        <tr>
            <td>actorToken</td>
            <td>false</td>
            <td>Token that represents the acting party, sent with <code>actorTokenType</code>.</td>
            <td>-</td>
        </tr>
        <tr>
            <td>actorTokenType</td>
            <td>false</td>
            <td>URN of the actor token type.</td>
            <td>-</td>
        </tr>
        <tr>
            <td>writeAuthorizationHeader</td>
            <td>false</td>
            <td>Writes the issued token to a request header after a successful exchange.</td>
            <td>true</td>
        </tr>
        <tr>
            <td>authorizationHeader</td>
            <td>false</td>
            <td>Request header that the issued token is written to.</td>
            <td>Authorization</td>
        </tr>
    </tbody>
</table>

### Errors

<table>
    <thead>
        <tr>
            <th>HTTP status code</th>
            <th>Description</th>
        </tr>
    </thead>
    <tbody>
        <tr>
            <td><code>500</code></td>
            <td>In <code>RESOURCE</code> mode, the API declares no resource named <code>oauth2Resource</code>. The message is <code>No OAuth2 resource defined with name [&lt;name&gt;]</code>.</td>
        </tr>
        <tr>
            <td><code>502</code></td>
            <td>
                <p>The exchange fails. The message starts with <code>OAuth 2.0 Token Exchange failed:</code> and gives the reason, for example:</p>
                <ul>
                    <li>The authorization server rejects the request. The message carries its status code and its <code>error</code> and <code>error_description</code>.</li>
                    <li>The token endpoint can't be reached in time, or its certificate can't be validated.</li>
                    <li>The response lacks <code>access_token</code>, <code>issued_token_type</code>, or <code>token_type</code>.</li>
                    <li>The OAuth2 resource doesn't support token exchange, or it's an OAuth2 / OpenID Connect Provider resource with no <strong>Token exchange endpoint</strong>.</li>
                </ul>
            </td>
        </tr>
    </tbody>
</table>

You can override the default response with a response template defined at the API level. The policy sends the following key:

<table>
    <thead>
        <tr>
            <th>Key</th>
            <th>Parameters</th>
        </tr>
    </thead>
    <tbody>
        <tr>
            <td>OAUTH2_TOKEN_EXCHANGE_ERROR</td>
            <td>-</td>
        </tr>
    </tbody>
</table>
