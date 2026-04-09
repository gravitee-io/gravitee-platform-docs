# mTLS Certificate Management - Platform Changes

## Related Changes

### Management Console

The Management Console introduces a new **Enable mTLS Certificate Management** toggle in **Portal Settings > New Developer Portal**. This toggle allows administrators to enable or disable the mTLS certificate management feature globally for the Developer Portal.

### Developer Portal

The Developer Portal adds a new **Certificates** section under **Application Settings** with the following components:

**Tabbed Views:**

- **Active certificates** tab: Displays certificates with status `ACTIVE`, `ACTIVE_WITH_END`, or `SCHEDULED`. The tab badge shows the count of active certificates.
- **Certificate history** tab: Displays certificates with status `REVOKED`. The tab badge shows the count of revoked certificates.

**Upload Dialog:**

The certificate upload workflow consists of three steps:

1. **Upload**: User provides the certificate name and PEM content (via paste or file upload).
2. **Configure**: User sets optional active-until date and, when rotating certificates, specifies a grace period end date for the currently active certificate.
3. **Confirm**: User reviews the certificate summary and submits.

**Table Displays:**

Certificate tables show the following metadata:

| Column | Description |
|:-------|:------------|
| Name | Certificate name |
| Uploaded | Creation date |
| Expiry date | Certificate expiration date (or "—" if not set) |
| Status | Certificate status badge (`ACTIVE`, `ACTIVE_WITH_END`, `SCHEDULED`, or `REVOKED`) |
| Days Remaining | Calculated days until expiration, "Expired", or "—" |

**Visibility:**

The Certificates section is visible only when `portal.next.mtls.enabled` is `true`.
