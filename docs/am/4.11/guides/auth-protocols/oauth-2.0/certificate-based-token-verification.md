### Configuring Certificate-Based Verification

Assign a certificate to a Protected Resource by including the `certificate` field (certificate ID) in the create or update request. During token introspection, when the token's `aud` claim matches the Protected Resource's `clientId`, the system retrieves the certificate to verify the JWT signature.

**Validation logic:**

* **Single-audience tokens:**
  1. Check if the audience matches an Application `clientId`. If found, return the Application certificate.
  2. If not found, check if the audience matches a Protected Resource `clientId`. If found, return the Protected Resource certificate.
  3. If not found, validate as a resource identifier per RFC 8707.
* **Multi-audience tokens:** Always validate via the resource identifier path (RFC 8707).

**Fallback behavior:** If the certificate field is `null`, the system assumes HMAC-signed tokens.

**Deletion restriction:** Certificates in use by Protected Resources cannot be deleted. The system returns `CertificateWithProtectedResourceException` with the message "You can't delete a certificate with existing protected resources."
