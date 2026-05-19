# Enable CIMD for a Domain

## Creating a CIMD-Enabled Domain

To enable CIMD support for a domain:

1. Navigate to **Settings > OAuth 2.0 > CIMD** in the domain configuration.
2. Toggle **Enable CIMD** to activate CIMD support.
3. Select a **Template Application** from the autocomplete list.

    {% hint style="info" %}
    Only applications marked as templates are shown in the autocomplete list. At least one application must be configured as a template before enabling CIMD.
    {% endhint %}

4. Configure SSRF protection settings:
   * **Allow Private/Loopback IP Addresses**: Enable to permit metadata document requests to private, loopback, link-local, or any-local IP addresses. Disable for production environments.
   * **Allow Unsecured HTTP URIs**: Enable to permit metadata document requests to plain HTTP (non-HTTPS) URIs. Disable for production environments.
5. Set metadata fetch behavior:
   * **Fetch Timeout (ms)**: Maximum time in milliseconds to wait for a metadata document response. Must be greater than 0.
   * **Max Response Size (KB)**: Maximum allowed size of a metadata document response in kilobytes. Must be greater than 0.
6. (Optional) Specify **Allowed Domains** to restrict metadata fetching to trusted hosts.

    {% hint style="info" %}
    The **Allowed Domains** field supports wildcard patterns for first-level subdomains. For example, `*.example.com` matches `app.example.com` but not `api.app.example.com`. Leave empty to allow all domains.
    {% endhint %}

7. Configure caching settings:
   * **Cache TTL (seconds)**: Time-to-live for cached metadata responses in seconds. Must be greater than 0.
   * **Cache Max Entries**: Maximum number of metadata documents to store in the cache. Must be greater than 0.
8. (Optional) Enable **Revoke Tokens And Consents When Client Metadata Changes** to automatically revoke all access tokens, refresh tokens, and scope approvals when a CIMD client's remote metadata document changes.

    {% hint style="warning" %}
    When enabled, this setting stores SHA-256 hashes of CIMD metadata documents per domain. The stored data persists indefinitely while the policy is enabled. If disabled, this data is deleted. This policy detects changes in remote CIMD metadata only; changes to template application settings do not trigger revocation.
    {% endhint %}


9. Click **Save** to activate CIMD support for the domain.

## Using CIMD Clients

After enabling CIMD, clients can authenticate using URL-shaped client IDs. See [CIMD Client Usage and Runtime Behavior](../auth-protocols/oauth-2.0/cimd-client-usage-and-runtime-behavior.md) for details.
