## Configure mTLS Plans and Subscriptions

mTLS plans for native Kafka APIs work the same way as for HTTP/Message APIs. The Gateway validates client certificates against known subscription certificates to authorize connections and populate context with plan, application, and subscription data.

### Plan Restrictions

Kafka APIs cannot have Keyless, mTLS, and authentication plans (OAuth2, JWT, API Key) published together.

You can publish either:
- An mTLS plan, or
- A Keyless plan, or
- An authentication plan (OAuth2, JWT, API Key)

You cannot combine these plan types on the same Kafka API.

### Add an mTLS Plan

1. Navigate to the Kafka API in APIM.
2. Add an mTLS plan.
3. Publish the plan.

### Create a Subscription

1. Create an application that contains a client certificate (PEM format).
2. Create a subscription to the Kafka API using the mTLS plan.
3. Provide the PEM client certificate during subscription creation.

The client certificate is associated with the subscription and used by APIM to identify the application during the Kafka connection.

### Runtime Behavior

When a client initiates a TLS connection with a client certificate:
1. The Gateway validates the certificate against known subscription certificates.
2. On match: the connection is authorized and the context is populated with plan, application, and subscription data.
3. Metrics and analytics reflect the resolved subscription (not ANONYMOUS).

<!-- GAP: No source material describes the UI steps for "Add an mTLS plan" or "Create a subscription" in detail. The source only states these actions must be performed. -->