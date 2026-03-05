### Token Exchange for MCP Servers

MCP Servers are Protected Resources restricted to `client_credentials` and `urn:ietf:params:oauth:grant-type:token-exchange` grant types. Token exchange allows an MCP Server to obtain a new access token by presenting a valid subject token.

#### Subject Token Validation

The system validates the subject token against domain-level configuration. The `tokenExchangeSettings.allowedSubjectTokenTypes` property controls which token types are accepted. Default allowed types:

* `access_token`
* `refresh_token`
* `id_token`
* `jwt`

#### Claim Preservation

The `gis` claim from the subject token is preserved in the exchanged token. This maintains the original grant identity across token exchanges.

#### Exchanged Token Properties

The exchanged token contains the following properties:

| Property | Value | Description |
|:---------|:------|:------------|
| `client_id` | MCP Server `clientId` | The entity performing the exchange |
| `aud` | MCP Server `clientId` | Token audience |
| `token_type` | `urn:ietf:params:oauth:token-type:access_token` | Always an access token |

#### Expiration Capping

The exchanged token's `expires_in` value cannot exceed the subject token's remaining lifetime. If the subject token expires in 300 seconds, the exchanged token will expire in 300 seconds or less.

#### Token Issuance Restrictions

Token exchange responses never include:

* Refresh tokens
* ID tokens (even when `openid` scope is requested)

#### OAuth Token Endpoint Request

To exchange a token, send a POST request to the OAuth token endpoint:

```http
POST /oauth/token
Content-Type: application/x-www-form-urlencoded

grant_type=urn:ietf:params:oauth:grant-type:token-exchange
&subject_token={subject_token_value}
&subject_token_type={token_type}
```

**Request Parameters:**

| Parameter | Required | Description |
|:----------|:---------|:------------|
| `grant_type` | Yes | Must be `urn:ietf:params:oauth:grant-type:token-exchange` |
| `subject_token` | Yes | The token to exchange |
| `subject_token_type` | Yes | Type of the subject token |

#### Response Format

```json
{
  "access_token": "string",
  "token_type": "urn:ietf:params:oauth:token-type:access_token",
  "expires_in": 3600
}
```

**Response Fields:**

| Field | Type | Description |
|:------|:-----|:------------|
| `access_token` | String | The exchanged access token |
| `token_type` | String | Always `urn:ietf:params:oauth:token-type:access_token` |
| `expires_in` | Integer | Token lifetime in seconds |

## Prerequisites

Before configuring token exchange, ensure the following requirements are met:

* **OAuth 2.0 enabled domain:** The domain must have OAuth 2.0 enabled.
* **Certificate upload (for certificate-based authentication):** If using certificate-based authentication, upload the certificate in PEM format.
* **Token exchange configuration:** Configure the domain's `tokenExchangeSettings.allowedSubjectTokenTypes` property. The default allowed types are:
  * `access_token`
  * `refresh_token`
  * `id_token`
  * `jwt`
* **Secret expiration notifications (optional):** To enable secret expiration notifications, configure the domain's `SecretExpirationSettings`.
