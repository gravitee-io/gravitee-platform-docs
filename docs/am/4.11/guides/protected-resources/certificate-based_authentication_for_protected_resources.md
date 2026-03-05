### Certificate-Based Authentication for Protected Resources

Protected Resources support certificate-based authentication for JWT signature verification during token introspection. Upload a certificate to the domain, then reference it in the Protected Resource configuration via the `certificate` field. The system stores the certificate ID as `nvarchar(64)` in JDBC or as a string in MongoDB.

When a token's audience (`aud` claim) matches the Protected Resource's `clientId`, the introspection service uses the associated certificate for signature validation. If no certificate is configured, the system assumes HMAC-signed tokens and uses an empty string as the certificate ID.

Attempting to delete a certificate referenced by any Protected Resource returns `400 Bad Request` with the message "You can't delete a certificate with existing protected resources."

{% hint style="info" %}
For details on how certificates are used during token introspection, see the Token Introspection guide.
{% endhint %}
