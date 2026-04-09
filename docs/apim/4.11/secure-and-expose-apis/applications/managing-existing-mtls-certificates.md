# Managing Existing mTLS Certificates

## Managing Certificates

Certificates are organized into two tabs:

* **Active certificates**: Displays certificates with Active, Active with End, or Scheduled status. The tab shows a badge count of certificates in these statuses.
* **Certificate history**: Displays certificates with Revoked status. The tab shows a badge count of revoked certificates.

Each table displays the following columns:

| Column | Description |
|:-------|:------------|
| Name | Certificate name |
| Uploaded | Upload date |
| Expiry date | Expiration date, or "—" if no expiration is set |
| Status | Certificate status |
| Days Remaining | Number of days until expiration, "Expired" if past expiration, or "—" if no expiration is set |

To delete a certificate, click the **Delete** button in the table row. The deletion behavior depends on the certificate status:

* **Non-last active certificate or revoked certificate**: A single confirmation dialog appears. Click **Confirm** to delete the certificate.
* **Last active certificate**: A two-step confirmation process prevents unintended loss of authentication capability:
  1. Click **Delete** in the table row.
  2. A warning dialog appears with the message: "There is no active certificate in case you proceed with the deletion. Do you want to proceed?"
  3. Click **Confirm** to complete the deletion.


## End-User Configuration

For API endpoint details, see [mTLS Certificate Management API Reference](mtls-certificate-management-api-reference.md).
