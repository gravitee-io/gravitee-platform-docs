### Token Introspection with Protected Resources

When introspecting a token, AM resolves the audience claim (`aud`) to determine the resource server. The resolution logic depends on whether the token contains a single audience or multiple audiences.

#### Single Audience Resolution

For a single audience value, AM performs the following checks in order:

1. Query `ClientSyncService` to check if the audience matches a client ID
2. If not found, query `ProtectedResourceSyncService` to check if the audience matches a Protected Resource client ID
3. If not found, validate the audience as a resource identifier via `ProtectedResourceManager`

#### Multiple Audience Resolution

For multiple audience values, AM validates all audiences as resource identifiers per RFC 8707. Each audience must correspond to a valid Protected Resource identifier.

#### Certificate-Based JWT Verification

After resolving the audience to a client or Protected Resource, AM determines the JWT verification method:

* If the resolved client or Protected Resource has a `certificate` field, AM uses that certificate for JWT signature verification
* If the `certificate` field is null, AM assumes HMAC-based verification

#### Introspection Response

The introspection response includes the following fields:

* `client_id`: Set to the resolved client or Protected Resource ID
* `aud`: Set to the resolved client or Protected Resource ID

