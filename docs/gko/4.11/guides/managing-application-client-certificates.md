# Managing Application Client Certificates

## Trust Store Configuration

The gateway builds subscription trust stores from registered certificates. For each subscription, certificates are decoded from Base64, parsed as PKCS7 bundles (with PEM fallback), and added to a `KeyStore` instance. The trust store is registered with `SubscriptionTrustStoreLoaderManager` and indexed by SHA-256 fingerprint. When certificates change, old fingerprints are evicted from cache and new fingerprints are indexed.

## Creating Client Certificates

Applications register certificates through the Console UI or Kubernetes CRD.

In the Console, navigate to **Applications** → **[Application Name]** → **General**. The deprecated `Client Certificate` field displays the most recently created certificate when multiple certificates exist. A warning banner indicates the total count when more than one certificate is registered.

For programmatic registration, use the Application CRD `spec.settings.tls.clientCertificates` array. Each certificate entry supports:

* Inline PEM content
* Secret or ConfigMap references
* Template notation (`[[ secret 'name/key' ]]` with `ENABLE_TEMPLATING=true`)

Each certificate entry includes optional `name`, `startsAt`, and `endsAt` fields. The system computes the SHA-256 fingerprint, extracts subject and issuer DN, and assigns status based on validity dates.
