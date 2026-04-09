# Creating and Uploading mTLS Certificates

## Creating Certificates

To add a certificate, navigate to the application's **Certificates** section and click **Upload certificate**. The upload process consists of four steps:

### Step 1: Upload

1. Enter a certificate name (up to 256 characters).
2. Provide the certificate content using one of the following methods:
   * Paste the PEM content directly into the **Certificate (PEM)** field.
   * Click **Choose file (.pem, .crt, .cer)** to upload a certificate file. File upload automatically populates the **Certificate Name** field with the file name (excluding the extension) if the field is empty.
3. Click **Continue** to proceed to validation.

If validation fails, an error message is displayed.

### Step 2: Configure

1. (Optional) Set an **Active until** date to specify when the certificate should stop being active.
2. If active certificates already exist, specify a **Grace period end for current certificate** date. This field is required when rotating certificates and must be set to a date between today and the active certificate's expiration date. Both certificates remain active during the grace period to prevent downtime.
3. Click **Continue** to proceed to confirmation.

### Step 3: Confirm

1. Review the certificate summary, which displays:
   * Certificate name
   * **Active until** date (if set)
   * **Grace period ends** date (if set)
2. Click **Add Certificate** to complete the upload.

If a grace period was set, the previously active certificate is updated with the grace period end date as its expiration.

## Managing Certificates
