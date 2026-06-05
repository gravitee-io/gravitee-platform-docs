# Agent Application Restrictions and Related Changes

## Restrictions

Agent applications are subject to the following restrictions:

* Agent applications cannot use `implicit`, `password`, or `refresh_token` grants.
* `USER_EMBEDDED` agents cannot use `client_credentials` grant.
* `AUTONOMOUS` agents cannot use `authorization_code` grant.
* `HOSTED_DELEGATED` agents cannot use both `authorization_code` and `client_credentials` grants.
* `USER_EMBEDDED` and `HOSTED_DELEGATED` agents require at least one redirect URI.
* SPIFFE `subjectMatchMode=PREFIX` is only allowed for `HOSTED_DELEGATED` or `AUTONOMOUS` agent applications.
* SPIFFE subject must end with `/` when `subjectMatchMode=PREFIX`.
* SPIFFE subject must start with `spiffe://{trustDomain}/`.
* CIMD documents using secret-based token endpoint auth methods (`client_secret_basic`, `client_secret_post`, `client_secret_jwt`) are rejected.
* CIMD URLs resolving to private/reserved IP addresses are rejected unless `allowPrivateIpAddress=true`.
* CIMD HTTP (non-HTTPS) URLs are rejected unless `allowUnsecuredHttpUri=true`.
* Trust domain JWKS URLs resolving to private/reserved IP addresses are rejected unless `allowPrivateIpAddress=true`.
* SPIFFE JWT-SVIDs presented with `client_assertion_type=urn:ietf:params:oauth:client-assertion-type:jwt-bearer` are rejected with an error.
* Standard `jwt-bearer` assertions now strictly enforce RFC 7523 (`iss == sub == client_id`).

## Related Changes

### Management Console

The management console introduces a top-level **Agents** navigation entry with a dedicated agent list and creation wizard, separate from the **Applications** area. The Applications list now excludes agents by default.

### API Changes

The `/applications` API endpoint accepts a multi-valued `type` query parameter to filter by application type. For example:
- `?type=AGENT`
- `?type=WEB&type=NATIVE`

### Domain Settings

A new **Workload Identity** section under **Domain Settings** provides CRUD operations for trust domains.

### Database Migration

{% hint style="warning" %}
Database migration is required for this release.
{% endhint %}

The following schema changes are applied:
- A new `sub_type` column is added to the `applications` table
- A new `trust_domains` table is created with an index on `reference_type` and `reference_id`

### Application Schema Changes

The application schema has been updated:
- The `settings.agent` nested object is removed
- `settings.spiffe` is renamed to `settings.workloadIdentitySettings`

### Agent Registration

Agent applications can now be marked as DCR/CIMD registration templates.

### Token Behavior

Tokens issued to user-bound agents set `act.sub` to the agent instance ID when known, rather than falling back to the blueprint `client_id`.

