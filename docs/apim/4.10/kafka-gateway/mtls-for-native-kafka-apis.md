### Impacts

Enabling mTLS for native Kafka APIs introduces the following operational changes:

- **Stricter SSL configuration**: Both the Gateway and Kafka clients must be configured with keystores and truststores. The Gateway requires `clientAuth: required` in `gravitee.yml`.
- **Mandatory client certificate management**: Each application must provide a valid client certificate to establish a connection. Certificates must be associated with subscriptions in APIM.
- **Limited plan combination options**: Kafka APIs cannot simultaneously publish Keyless, mTLS, and authentication plans (OAuth2, JWT, API Key). Only one security model can be active at a time.

### Benefits

mTLS for native Kafka APIs provides the following security and operational improvements:

- **Strong authentication of Kafka clients**: The Gateway validates client identities using certificates, preventing unauthorized access.
- **Improved security for Kafka traffic**: Mutual TLS authentication adds a layer of protection beyond standard TLS, ensuring both parties verify each other's identity.
- **Alignment with existing APIM mTLS mechanisms**: mTLS for Kafka APIs works the same way as for classic V4 APIs, enabling consistent subscription resolution and accurate metrics attribution (plan, application, subscription).

### Summary

- mTLS for native Kafka APIs works the same way as for classic APIs.
- It requires SSL/mTLS configuration on both the Gateway and Kafka clients.
- An mTLS plan must be added and published in APIM.
- Applications must be created with a client certificate.
- Some plan combinations are not allowed (Keyless, mTLS, and authentication plans cannot be published together).