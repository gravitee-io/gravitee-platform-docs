### Renewing Protected Resource Secrets

To renew an existing secret, send a POST request to `/secrets/{secretId}/_renew`. This generates a new secret value and updates the expiration date while preserving the settings ID.

### Managing Protected Resource Memberships

Add a member by sending a POST request to `/organizations/{orgId}/environments/{envId}/domains/{domainId}/protected-resources/{resourceId}/members` with JSON:

```json
{
  "memberId": "user-id",
  "memberType": "USER",
  "role": "string"
}
```

Members can be users or groups assigned specific roles. Permissions cascade from organization → environment → domain → resource levels. Four permission types control access:

* **LIST** — View members
* **CREATE** — Add or update members
* **DELETE** — Remove members
* **READ** — View permissions

To remove a membership, send a DELETE request to `/members/{member}`.
