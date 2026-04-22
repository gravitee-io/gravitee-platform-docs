# mTLS plans for Kafka native APIs

## Overview

mTLS plan support for Kafka native APIs enables client authentication using X.509 certificates and resolves subscriptions for accurate metrics attribution. Previously, mTLS was blocked for Kafka listeners, forcing users to rely on Keyless plans with TLS context policies that resulted in ANONYMOUS metrics. This feature brings Kafka native APIs to parity with HTTP and message APIs.

## Plan security mutual exclusion

Kafka native APIs enforce strict separation between plan security types. Keyless, mTLS, and authentication plans (OAuth2, JWT, API Key) can't be mixed in published state. The Management API rejects any attempt to publish a plan that conflicts with an already-published plan type. The Console UI offers to close conflicting plans automatically when publishing through the UI. Multiple plans of the same security type (for example, two mTLS plans) can coexist.

| Plan type to publish | Conflicts with | Allowed with |
|:---------------------|:---------------|:-------------|
| Keyless | mTLS, API Key, OAuth2, JWT | Other Keyless plans |
| mTLS | Keyless, API Key, OAuth2, JWT | Other mTLS plans |
| API Key, OAuth2, JWT | Keyless, mTLS | Other authentication plans |

**Error messages:**

When attempting to publish conflicting plan types via the Management API, the following error is returned:

| Scenario | Error message |
|:---------|:--------------|
| Publishing Keyless when mTLS/auth exists | `"A plan with mTLS or authentication is already published for the Native API. Keyless plans cannot be combined with mTLS or authentication plans."` |
| Publishing mTLS when Keyless/auth exists | `"A Keyless or authentication plan is already published for the Native API. mTLS plans cannot be combined with Keyless or authentication plans."` |
| Publishing auth when Keyless/mTLS exists | `"A Keyless or mTLS plan is already published for the Native API. Authentication plans cannot be combined with Keyless or mTLS plans."` |

## Hot-reload certificate management

Subscription certificates are loaded dynamically without requiring gateway restarts. When a subscription is created or updated with a new certificate, the gateway's trust store manager refreshes its internal state to include the new certificate.
