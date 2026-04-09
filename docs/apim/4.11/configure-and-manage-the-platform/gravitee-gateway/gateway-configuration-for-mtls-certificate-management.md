# Gateway Configuration for mTLS Certificate Management

## Certificate Validation

Uploaded certificates are validated before storage. Certificate validation is performed server-side. Invalid PEM content fails at the validation step with error message "Validation failed for Certificate uploaded. Please try again".

## Prerequisites

* New Developer Portal must be enabled
* `portal.next.mtls.enabled` configuration property must be set to `true`
* User must have `APPLICATION_DEFINITION[UPDATE]` permission to upload or delete certificates
* Valid PEM-formatted client certificate (`.pem`, `.crt`, or `.cer` file)

## Certificate Management


### Portal Configuration

| Property | Description | Example |
|:---------|:------------|:--------|
| `portal.next.mtls.enabled` | Enables mTLS certificate management in the new Developer Portal | `false` (default) |

Application owners with `APPLICATION_DEFINITION[UPDATE]` permission can manage client certificates directly through the Developer Portal. For details on certificate upload, rotation, and lifecycle management, see the application-level mTLS certificate management documentation.

For Kubernetes-managed certificate configuration, see [Kubernetes CRD Configuration for Client Certificates](../../../../gko/4.11/guides/kubernetes-crd-configuration-for-client-certificates.md).

## Restrictions

* Certificate deletion is blocked if it is the last active certificate and the user cancels the final warning dialog.
* Grace period end date cannot exceed the active certificate's expiration date.
* Grace period end date is required when rotating certificates (when active certificates exist).
* File upload supports only `.pem`, `.crt`, and `.cer` extensions.
* Certificate name is limited to 256 characters.
