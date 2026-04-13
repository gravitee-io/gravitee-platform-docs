# Create and manage mTLS certificates (application owner guide)

This guide shows application owners how to upload, rotate, and delete mTLS client certificates for their applications from the new Developer Portal.

## Prerequisites

- The new Developer Portal is enabled for your environment (`portal.next.access.enabled`).
- Your administrator has turned on the **Enable mTLS Certificate Management** toggle in the **New Developer Portal** section of the **Portal** settings page in the Management Console. Without this toggle the Certificates section isn't shown. For details, see [Configuring mTLS certificate management (administrator guide)](configuring-mtls-certificate-management-administrator-guide.md).
- You have `APPLICATION_DEFINITION[READ]` on the application to view certificates, and `APPLICATION_DEFINITION[UPDATE]` to upload, update, or delete them.
- Your certificate is a valid X.509 certificate in PEM format. CA certificates aren't accepted.

## Open the Certificates section

1. In the new Developer Portal, open the application you want to manage.

    <!-- TODO: Screenshot of application details page in new Developer Portal -->
    <figure><img src="../../.gitbook/assets/PLACEHOLDER-new-portal-application-details.png" alt=""><figcaption><p>Application details page</p></figcaption></figure>

2. Open the **Settings** tab and scroll to the **Certificates** section.

    <!-- TODO: Screenshot of Settings tab showing empty Certificates section -->
    <figure><img src="../../.gitbook/assets/PLACEHOLDER-new-portal-certificates-empty.png" alt=""><figcaption><p>Empty Certificates section</p></figcaption></figure>

    If no certificate has been uploaded yet, the section shows an empty state with the message _"No mTLS certificates added"_. Once one or more certificates exist, the section displays **Active certificates** and **Certificate history** tabs.

## Upload a certificate

1. In the **Certificates** section, click **Upload certificate** to open the upload wizard.

    <!-- TODO: Screenshot of Upload certificate button -->
    <figure><img src="../../.gitbook/assets/PLACEHOLDER-new-portal-upload-certificate-button.png" alt=""><figcaption><p>Upload certificate button</p></figcaption></figure>

2. On the **Upload** step, enter a **Certificate Name**. The name can be up to 255 characters.

    <!-- TODO: Screenshot of upload dialog step 1 -->
    <figure><img src="../../.gitbook/assets/PLACEHOLDER-new-portal-add-certificate-upload-step.png" alt=""><figcaption><p>Upload step of the add certificate wizard</p></figcaption></figure>

3. Provide the PEM-encoded certificate body in one of two ways:

    - Paste the PEM content into the **Certificate (PEM)** text area.
    - Click **Choose file (.pem, .crt, .cer)** and select a certificate file from your local machine. If the **Certificate Name** field is empty, it auto-fills with the file name (without extension).

4. Click **Continue**. The portal sends the PEM to Gravitee for validation. If the certificate is valid, the wizard advances to the **Configure** step and pre-fills the **Active until** date with the certificate's expiration date. If validation fails, an inline error is shown and you stay on the **Upload** step.

5. On the **Configure** step, optionally adjust **Active until (optional)**. The date can't be earlier than today.

    <!-- TODO: Screenshot of upload dialog step 2 (no existing active certificate) -->
    <figure><img src="../../.gitbook/assets/PLACEHOLDER-new-portal-add-certificate-configure-step.png" alt=""><figcaption><p>Configure step of the add certificate wizard</p></figcaption></figure>

6. If another certificate is already active for this application, the wizard also asks for a **Grace period end for current certificate** date. Both certificates remain active until this date, so clients can cut over without downtime. The grace period end can't be later than the currently active certificate's expiration.

    <!-- TODO: Screenshot of upload dialog step 2 with grace period field -->
    <figure><img src="../../.gitbook/assets/PLACEHOLDER-new-portal-add-certificate-grace-period.png" alt=""><figcaption><p>Grace period field during rotation</p></figcaption></figure>

7. Click **Continue** to open the **Confirm** step, review the summary, and click **Add Certificate** to submit. The new certificate is created and, if a grace period was set, the currently active certificate's end date is updated to match.

    <!-- TODO: Screenshot of upload dialog step 3 (summary) -->
    <figure><img src="../../.gitbook/assets/PLACEHOLDER-new-portal-add-certificate-confirm-step.png" alt=""><figcaption><p>Confirm step showing certificate summary</p></figcaption></figure>

## View certificates

In the **Certificates** section, two tabs organize certificates by state:

- **Active certificates** — certificates with status `ACTIVE`, `ACTIVE_WITH_END`, or `SCHEDULED`.
- **Certificate history** — certificates with status `REVOKED`.

Each row displays:

| Column | Description |
|:-------|:------------|
| Name | The certificate's display name. |
| Uploaded | The date the certificate was uploaded. |
| Expiry date | The certificate's X.509 `notAfter` date. |
| Status | The current certificate status. |
| Days remaining | The number of days until expiration. |

## Delete a certificate

1. In the **Active certificates** tab, click the delete action on the certificate row.
2. Confirm the first deletion dialog.
3. If the certificate you're deleting is the only active certificate left on the application, a second warning dialog asks you to confirm that no active certificate will remain. Click **Cancel** on either dialog to abort the deletion.

If the application still has active mTLS subscriptions and you try to delete its last certificate, Gravitee rejects the request to prevent leaving those subscriptions without a valid certificate. Upload a replacement first or delete the subscriptions, then retry.

## Verification

To verify mTLS certificate management is working as expected, follow these steps:

1. In the new Developer Portal, open your application and confirm the **Certificates** section is visible in the **Settings** tab.
2. Upload a test certificate by following the steps above. After submission the certificate appears in the **Active certificates** tab with status `ACTIVE` or `ACTIVE_WITH_END`.

    <!-- TODO: Screenshot of populated Active certificates tab -->
    <figure><img src="../../.gitbook/assets/PLACEHOLDER-new-portal-active-certificates-tab.png" alt=""><figcaption><p>Active certificates tab after upload</p></figcaption></figure>

3. Delete the test certificate. After confirmation, it moves to the **Certificate history** tab with status `REVOKED`.
