# Manage Application Certificates (Developer Portal)

## Creating Certificates

To upload a certificate, navigate to the application's Certificates section in the Developer Portal and click **Upload Certificate**. The upload workflow consists of three steps:

1. **Upload**: Provide a certificate name and paste the PEM-encoded certificate or upload a `.pem`, `.crt`, or `.cer` file. If the certificate name field is left blank, the system auto-fills it from the uploaded file name. The system validates the certificate format server-side.
2. **Configure**: Optionally set an **Active Until** date. If available, this field is pre-filled from the certificate's expiration date. If active certificates already exist, you must specify a **Grace Period End** date for the current certificate to enable rotation without downtime. Both certificates remain active during the grace period.
3. **Confirm**: Review the summary and confirm to create the certificate.

{% hint style="info" %}
Certificate names are limited to 256 characters.
{% endhint %}

## Managing Certificates

Application owners view certificates in two tabs:

* **Active Certificates**: Displays certificates with status `ACTIVE`, `ACTIVE_WITH_END`, or `SCHEDULED`.
* **Certificate History**: Displays certificates with status `REVOKED`.

The table displays the following columns:

| Column | Description |
|:-------|:------------|
| Name | Certificate name |
| Uploaded | Upload date |
| Expiry date | Certificate expiration date or `—` if not set |
| Status | Certificate status |
| Days Remaining | Days until expiration, `Expired`, or `—` |

To delete a certificate, click the delete action for the row. If deleting the last active certificate, a second confirmation dialog warns that no active certificate will remain. Deletion is blocked if active **M Tls** subscriptions exist, returning an HTTP 400 error.

## End-User Configuration

The Certificates section is displayed only when `portal.next.mtls.enabled` is set to `true` by an administrator. Viewing certificates requires `APPLICATION_DEFINITION[READ]` permission. Uploading, updating, or deleting certificates requires `APPLICATION_DEFINITION[UPDATE]` permission.

When no certificates exist, an empty state displays with the message "No mTLS certificates added" and the prompt "Add your first certificate to enable mTLS authentication for this application."
