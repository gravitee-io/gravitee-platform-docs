# Manage Application Certificates

## Creating Certificates

Navigate to the application's **Settings** tab in the Developer Portal and locate the **Certificates** section. Click **Upload certificate** to open the Add Certificate dialog.

### Upload step

1. Enter a certificate name (up to 256 characters).
2. Paste the PEM-encoded certificate into the **Certificate (PEM)** textarea, or upload a `.pem`, `.crt`, or `.cer` file.
3. Click **Continue** to validate the certificate.

When uploading a file, the certificate name field auto-fills from the file name (without extension) if the name field is empty.

### Configure Step

1. Optionally set an **Active until** date. The date must be today or later.
2. If an active certificate already exists, set a **Grace period end for current certificate** date. This field is required and must fall between today and the active certificate's expiration date.
3. Click **Continue** to review the summary.

{% hint style="info" %}
Both certificates remain active during the grace period to avoid downtime.
{% endhint %}

### Confirm Step

Review the certificate summary, which displays the certificate name, **Active until** date (if set), and **Grace period ends** date (if set). Click **Add Certificate** to create the certificate.

## Managing Certificates

Certificates appear in two tabs:

* **Active certificates**: Displays Active, Active With End, and Scheduled certificates.
* **Certificate history**: Displays Revoked certificates.

Each tab shows a badge with the certificate count. The certificate table displays the following columns:

| Column | Description |
|:-------|:------------|
| Name | Certificate name |
| Uploaded date | Certificate creation timestamp |
| Expiry date | Certificate expiration date, or "—" if not set |
| Status | Certificate status (Active, Active With End, Scheduled, or Revoked) |
| Days Remaining | Days until expiry, "Expired", or "—" if not set |

### Deleting Certificates

To delete a certificate from either tab, click the delete icon. A confirmation dialog appears with the message: "Are you sure you want to delete the certificate '{certificateName}'?"

If deleting the last active certificate, a second confirmation dialog appears with the warning: "There is no active certificate in case you proceed with the deletion. Do you want to proceed?"


Deleting a certificate while active **M Tls** subscriptions exist returns an HTTP 400 error and prevents deletion.
