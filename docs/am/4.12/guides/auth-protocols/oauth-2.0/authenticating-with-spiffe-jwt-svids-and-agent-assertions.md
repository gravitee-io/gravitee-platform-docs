# Authenticating with SPIFFE JWT-SVIDs and Agent Assertions

## Authenticating with SPIFFE JWT-SVIDs

Clients authenticate by presenting a SPIFFE JWT-SVID in the `client_assertion` parameter with `client_assertion_type=urn:ietf:params:oauth:client-assertion-type:jwt-spiffe`. The gateway verifies the SVID signature against the trust domain's JWKS bundle and matches the SVID's `sub` claim to the application's subject.

### EXACT Mode Authentication

1. Client obtains a JWT-SVID from its SPIRE agent (e.g., via the Workload API).
2. Client sends a token request:

    ```http
    POST /oauth/token
    Content-Type: application/x-www-form-urlencoded

    grant_type=client_credentials
    &client_assertion_type=urn:ietf:params:oauth:client-assertion-type:jwt-spiffe
    &client_assertion=<JWT-SVID>
    &client_id=<optional>
    ```

3. Gateway extracts `client_id` from the form parameter if present; otherwise uses the SVID's `sub` claim.
4. Gateway validates the SVID:
   1. Verifies `aud` contains the token endpoint.
   2. Looks up the trust domain by name.
   3. Fetches the trust bundle JWKS.
   4. Verifies the SVID signature against the JWKS.
   5. Matches the SVID's `sub` claim to the application's subject (exact match).
5. Gateway mints an access token with `act` claim describing the agent instance.

### PREFIX Mode Authentication (Per-Instance Agents)

PREFIX mode enables per-instance agent identity for `HOSTED_DELEGATED` and `AUTONOMOUS` agents. The application's subject is a prefix (e.g., `spiffe://am.local/hotel-agent/`), and the gateway accepts any SVID whose `sub` starts with that prefix.

1. Client obtains a JWT-SVID with a per-instance SPIFFE ID (e.g., `spiffe://am.local/hotel-agent/instance-a`).
2. Client sends a token request (same format as EXACT mode).
3. Gateway validates the SVID:
   1. Verifies `aud` contains the token endpoint.
   2. Looks up the trust domain by name.
   3. Fetches the trust bundle JWKS.
   4. Verifies the SVID signature against the JWKS.
   5. Matches the SVID's `sub` claim to the application's subject (prefix match).
4. Gateway synthesizes a per-instance client with `agentInstanceId` set to the full SPIFFE ID.
5. Gateway mints an access token with `act.sub` set to the agent instance ID (the full SPIFFE ID).

### Agent JWT-Bearer Assertion (Blueprint Instances)

For agents using self-signed JWTs (not SPIFFE), use `client_assertion_type=urn:ietf:params:oauth:client-assertion-type:agent-jwt-bearer`. The blueprint application's `client_id` is carried in the JWT's `iss` claim, and the agent instance ID is carried in the `sub` claim.

1. Client sends a token request:

    ```http
    POST /oauth/token
    Content-Type: application/x-www-form-urlencoded

    grant_type=authorization_code
    &code=<auth_code>
    &client_assertion_type=urn:ietf:params:oauth:client-assertion-type:agent-jwt-bearer
    &client_assertion=<JWT>
    ```

2. Gateway extracts the blueprint `client_id` from the JWT's `iss` claim and the agent instance ID from the `sub` claim.
3. Gateway validates the assertion:
   1. Verifies `aud` contains the token endpoint.
   2. Looks up the blueprint application by `client_id`.
   3. Verifies the blueprint is an agent application.
   4. Verifies the JWT signature against the blueprint's JWKS.
4. Gateway synthesizes a per-instance client with `agentInstanceId` set to the JWT's `sub`.
5. Gateway mints an access token with `act.sub` set to the agent instance ID.
