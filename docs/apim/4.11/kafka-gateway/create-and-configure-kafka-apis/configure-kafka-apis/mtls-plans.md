# mTLS plans for Kafka native APIs

## Overview

mTLS plan support for Kafka native APIs enables client authentication using X.509 certificates and resolves subscriptions for accurate metrics attribution. Previously, mTLS was blocked for Kafka listeners, forcing users to rely on Keyless plans with TLS context policies that resulted in ANONYMOUS metrics. This feature brings Kafka native APIs to parity with HTTP and message APIs.

## Plan Security Mutual Exclusion

Kafka native APIs enforce strict separation between plan security types. You cannot mix Keyless, mTLS, and authentication plans (OAuth2, JWT, API Key) in published state. When publishing a plan of one type, all published plans of conflicting types are automatically closed. Multiple plans of the same security type (for example, two mTLS plans) can coexist.

| Plan Type to Publish | Conflicts With | Allowed With |
|:---------------------|:---------------|:-------------|
| Keyless | mTLS, API Key, OAuth2, JWT | Other Keyless plans |
| mTLS | Keyless, API Key, OAuth2, JWT | Other mTLS plans |
| API Key, OAuth2, JWT | Keyless, mTLS | Other authentication plans |

**Error Messages:**

When attempting to publish conflicting plan types, the system returns one of the following messages:

| Scenario | Error Message |
|:---------|:--------------|
| Publishing Keyless when mTLS/auth exists | `"A plan with mTLS or authentication is already published for the Native API. Keyless plans cannot be combined with mTLS or authentication plans."` |
| Publishing mTLS when Keyless/auth exists | `"A Keyless or authentication plan is already published for the Native API. mTLS plans cannot be combined with Keyless or authentication plans."` |
| Publishing auth when Keyless/mTLS exists | `"A Keyless or mTLS plan is already published for the Native API. Authentication plans cannot be combined with Keyless or mTLS plans."` |

## Hot-Reload Certificate Management

Subscription certificates are loaded dynamically without requiring gateway restarts. When a subscription is created or updated with a new certificate, the gateway's trust store manager refreshes its internal state to include the new certificate.
