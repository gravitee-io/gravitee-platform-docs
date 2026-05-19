# Enable CIMD for a Domain

## Creating a CIMD-Enabled Domain

To enable CIMD for a domain, navigate to the domain's CIMD settings page (`/domains/:domainId/settings/cimd`) and complete the following steps:

1. Toggle **Enable CIMD** to `true`.
2. Select a **Template Application** from the autocomplete list. The list is filtered to applications with the `template` flag.
3. Configure **SSRF Protection** settings:
   * Enable **Allow Private/Loopback IP Addresses** only if your environment requires metadata document requests to private IP addresses.
   * Enable **Allow Unsecured HTTP URIs** only if your environment requires metadata document requests to plain HTTP URIs.
   * Set **Fetch Timeout (ms)** to an appropriate value for your network conditions.
   * Set **Max Response Size (KB)** to an appropriate value for your network conditions.
4. (Optional) Specify **Allowed Domains** to restrict metadata document URLs to trusted domains. This field supports wildcard patterns like `*.example.com`.
5. Configure **Cache Settings**:
   * Set **Cache TTL (seconds)** to control how long metadata is cached.
   * Set **Cache Max Entries** to limit memory usage.
6. (Optional) Enable **Revoke Tokens and Consents When Client Metadata Changes** to automatically revoke tokens when remote metadata changes.
7. Save the configuration.

After enabling CIMD, the OIDC discovery document (`/.well-known/openid-configuration`) will advertise `"client_id_metadata_document_supported": true`.

<figure><img src="../../.gitbook/assets/am-cimd-settings-enabled.png" alt="CIMD settings page with CIMD enabled and default configuration"><figcaption></figcaption></figure>

<figure><img src="../../.gitbook/assets/am-cimd-settings-disabled.png" alt="CIMD settings page with CIMD disabled"><figcaption></figcaption></figure>

<figure><img src="../../.gitbook/assets/am-cimd-settings-advanced.png" alt="CIMD settings page showing advanced settings"><figcaption></figcaption></figure>
