# mTLS Client Certificate Validation and Cache Behavior

## End-User Configuration

<!-- UNCERTAIN: End-user configuration steps not provided in source materials -->

## Restrictions

* The deprecated `clientCertificate` property and the `clientCertificates` array are mutually exclusive. Setting both triggers a validation error: "cannot use both clientCertificate and clientCertificates."
* Within a certificate object, `content` and `ref` are mutually exclusive. Setting both triggers: "cannot use both content and ref."
* Either `content` or `ref` must be set. Omitting both triggers: "either content or ref must be set."
* Certificate fingerprints (SHA-256) must be unique across all active applications (status != REVOKED) within an environment.
* Inline certificate `content` must be valid PEM format. Invalid PEM triggers: "invalid PEM format."
* If `encoded: true`, content must be valid base64. Invalid encoding triggers: "invalid base64 encoding."
* `startsAt` and `endsAt` must be RFC3339 format. Invalid dates trigger validation errors.
