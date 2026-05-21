# CIMD Console and UI Changes

## Related Changes

### CIMD Settings Page

The CIMD settings page is accessible under the **OAuth 2.0** section in the domain settings menu, labeled **CIMD**. The form includes the following controls:

- **Enable CIMD**: Slide toggle to enable or disable Client ID Metadata Document support
- **Template Application**: Autocomplete field to select the template application (filtered to applications with `template = true`)
- **Allow private/loopback IP addresses**: Slide toggle for SSRF protection to allow private IP addresses
- **Allow unsecured HTTP URIs**: Slide toggle for SSRF protection to allow plain HTTP URIs
- **Fetch Timeout (ms)**: Numeric input for metadata fetch timeout
- **Max Response Size (KB)**: Numeric input for maximum metadata response size
- **Allowed Domains**: Chip list to restrict metadata to specific domains (supports wildcard patterns for first-level subdomains, e.g., `*.example.com`)
- **Cache TTL**: Numeric input for metadata cache time-to-live
- **Cache Max Entries**: Numeric input for maximum cache entries
- **Revoke tokens and consents when client metadata changes**: Toggle to enable automatic token revocation when metadata changes

**Validation rules:**
- Template Application is required when CIMD is enabled
- Numeric fields must be greater than zero
- Allowed domains must match valid domain patterns or wildcard patterns for first-level subdomains

**Error handling:**
On save failure, error messages from the API response are displayed in a snackbar.

### Application General Settings

Application general settings now display a **CIMD Template** badge if the application is the CIMD template. The delete and un-template actions are disabled for the CIMD template application.

### Audit Logs

Audit logs for CIMD clients include a `metadataDocumentHash` attribute in the actor attributes for `CLIENT_AUTHENTICATED` and `TOKEN_CREATED` events. Actor links are suppressed for CIMD clients because no detail page exists.

### Configuration Property Rename

The configuration property `softwareId` has been renamed to `templateId` in domain CIMD settings. Existing configurations must update this property name and ensure `templateId` references a valid application ID with `template = true`.

{% hint style="info" %}
CIMD clients do not appear in the application list or have detail pages in the console.
{% endhint %}
