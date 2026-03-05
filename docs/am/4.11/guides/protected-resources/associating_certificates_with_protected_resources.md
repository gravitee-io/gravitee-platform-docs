### Certificate-Based Authentication for Protected Resources

Protected Resources support certificate-based authentication for JWT signature validation during token introspection. Before associating a certificate with a Protected Resource, upload the certificate to the domain.

#### Configuration

Reference the certificate in the Protected Resource configuration via the `certificate` field. This field stores the certificate ID as `nvarchar(64)` in JDBC databases or as a string field in MongoDB.

#### Token Introspection Behavior

When introspecting tokens with an `aud` claim matching the Protected Resource's `clientId`:

* **Certificate configured**: The system uses the associated certificate for JWT signature validation.
* **No certificate configured**: The system assumes HMAC-signed tokens.

#### Deletion Constraint

Attempting to delete a certificate referenced by any Protected Resource returns `400 Bad Request` with the message:

{% hint style="info" %}
Configuring certificate-based authentication requires `PROTECTED_RESOURCE[UPDATE]` permission.
{% endhint %}
