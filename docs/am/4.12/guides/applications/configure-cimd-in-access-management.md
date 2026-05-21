# Configure CIMD in Access Management

## Creating CIMD Clients

CIMD clients are created dynamically during the OAuth authorization flow. To enable CIMD support:

1. Navigate to the domain's CIMD settings page.
2. Enable the **Enable CIMD** toggle.

    <figure><img src="../../.gitbook/assets/am-cimd-settings-disabled.png" alt="CIMD settings page with CIMD disabled"><figcaption></figcaption></figure>

3. Select a **Template Application** from the autocomplete list (filtered to applications with the template flag enabled).

    <figure><img src="../../.gitbook/assets/am-cimd-settings-enabled.png" alt="CIMD settings page with CIMD enabled and template application selected"><figcaption></figcaption></figure>

4. Configure SSRF protection settings:
   * Enable **Allow private/loopback IP addresses** or **Allow unsecured HTTP URIs** only if your environment requires access to internal or non-HTTPS metadata sources.
   * Set **Fetch Timeout (ms)** and **Max Response Size (KB)** to control resource consumption.
   * Optionally, add domains to the **Allowed Domains** chip list to restrict metadata sources (use `*.example.com` for first-level subdomain wildcards).

    <figure><img src="../../.gitbook/assets/am-cimd-ssrf-protection.png" alt="CIMD SSRF protection settings configured"><figcaption></figcaption></figure>

5. Configure **Cache TTL (seconds)** and **Cache Max Entries** to balance freshness and performance.

    <figure><img src="../../.gitbook/assets/am-cimd-cache-settings.png" alt="CIMD cache configuration with TTL and max entries"><figcaption></figcaption></figure>

6. Enable **Revoke on Document Change** to automatically revoke tokens when metadata changes.

    <figure><img src="../../.gitbook/assets/am-cimd-revoke-on-change.png" alt="CIMD settings with token revocation on metadata change enabled"><figcaption></figcaption></figure>

7. Save the configuration.
