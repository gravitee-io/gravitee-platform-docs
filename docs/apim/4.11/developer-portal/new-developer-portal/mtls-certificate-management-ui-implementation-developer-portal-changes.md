# mTLS Certificate Management UI Implementation (Developer Portal Changes)

## Related Changes

The Management UI adds an **Enable mTLS Certificate Management** toggle in Portal Settings → New Developer Portal, controlling the `portalNext.mtls.enabled` property. The Developer Portal adds a Certificates section to Application Settings, visible only when `portal.next.mtls.enabled` is true. The section displays an empty state with icon and description when no certificates exist, and a tabbed table view (Active Certificates and Certificate History) when certificates are present. The upload certificate dialog implements a three-step wizard (Upload, Configure, Confirm) with inline validation and error display. File upload auto-populates the certificate textarea and optionally the name field. Deletion triggers two-step confirmation for the last active certificate.
