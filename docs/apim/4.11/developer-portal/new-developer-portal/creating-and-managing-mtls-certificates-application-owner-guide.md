# Creating and Managing mTLS Certificates (Application Owner Guide)

## Creating Certificates

To create a certificate:

1. Navigate to the application's Certificates section and click **Upload certificate**.
2. In the upload dialog, enter a certificate name (up to 256 characters).
3. Paste the PEM-encoded certificate content or upload a file with `.pem`, `.crt`, or `.cer` extension.
   
   If uploading a file, the certificate name field auto-fills with the file name (without extension) if empty.
4. Click **Continue** to validate the certificate server-side.
   
   The system returns expiration, subject, and issuer metadata.
5. In the configuration step, optionally set an **Active until** date (minimum: today).
6. If active certificates exist, specify a grace period end date for the current certificate (maximum: current certificate expiration date).
   
   {% hint style="info" %}
   Both certificates remain active during the grace period to avoid downtime.
   {% endhint %}
7. Review the summary and click **Add Certificate** to submit.

The system creates the new certificate and, if applicable, updates the current certificate's end date to match the grace period.

Application owners can view certificates in two tabs:

* **Active Certificates**: Displays Active, Active with end, and Scheduled certificates
* **Certificate History**: Displays Revoked certificates

Each table displays the following information:

| Column | Description |
|:-------|:------------|
| Name | Certificate name |
| Uploaded | Upload date |
| Expiry date | Certificate expiration date |
| Status | Certificate status |
| Days Remaining | Days remaining until expiration |

Users with `APPLICATION_DEFINITION[UPDATE]` permission can delete certificates using the delete button on each row.

### Deleting Certificates

Deleting the last active certificate triggers a two-step confirmation:

1. Standard deletion confirmation
2. Warning that no active certificate will remain

If the user cancels at either step, the certificate is not deleted.

{% hint style="warning" %}
Attempting to delete the last active certificate when active mTLS subscriptions exist returns an HTTP 400 error.
{% endhint %}


