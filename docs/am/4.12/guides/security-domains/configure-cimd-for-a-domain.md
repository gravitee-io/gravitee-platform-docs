# Configure CIMD for a Domain

## Creating a CIMD-Enabled Domain

To enable CIMD at the domain level:

1. Navigate to the domain's CIMD settings page.
2. Toggle **Enable CIMD** on.

    <figure><img src="../../.gitbook/assets/am-cimd-settings-overview.png" alt="AM CIMD settings page showing enable toggle and template application selector"><figcaption></figcaption></figure>

3. Select a **Template Application** from the autocomplete list (filtered to applications with `template=true`).
4. Configure SSRF protection settings:
    * Enable **Allow private/loopback IP addresses** and **Allow unsecured HTTP URIs** only if required by your environment.
    * Add trusted domains to **Allowed Domains** to restrict metadata fetching.

    <figure><img src="../../.gitbook/assets/am-cimd-ssrf-protection.png" alt="AM CIMD SSRF protection settings including private IP and HTTP URI toggles"><figcaption></figcaption></figure>

5. Set **Fetch Timeout (ms)** and **Max Response Size (KB)** to control metadata retrieval behavior.
6. Configure **Cache TTL (seconds)** and **Cache Max Entries** to balance performance and freshness.

    <figure><img src="../../.gitbook/assets/am-cimd-cache-settings.png" alt="AM CIMD cache configuration showing TTL and max entries fields"><figcaption></figcaption></figure>

7. (Optional) Enable **Revoke tokens and consents when client metadata changes** to automatically revoke tokens when metadata documents change.

    <figure><img src="../../.gitbook/assets/am-cimd-revoke-on-change.png" alt="AM CIMD revoke on change toggle enabled"><figcaption></figcaption></figure>

8. Save the configuration.
