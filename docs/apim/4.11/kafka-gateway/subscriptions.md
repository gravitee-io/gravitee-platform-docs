---
description: An overview about subscriptions.
metaLinks:
  alternates:
    - subscriptions.md
---

# Subscriptions

## Overview

A subscription is a successful contract between an API publisher and an API consumer. A subscription is created when an API consumer uses a registered application to make a subscription request to a published plan and an API publisher either manually or automatically validates the subscription.

{% hint style="info" %}
**Keyless plan subscriptions**

APIs with Keyless plans do not require the API consumer to create an application or submit a subscription request because no authorization is required to access the backend API.
{% endhint %}

## Create subscriptions

API consumers can subscribe to APIs with published plans during the application creation process, or after the application is created. The APIM Console offers two ways to create a subscription using an existing application:

* To create a subscription from within your API, follow [these](create-and-configure-kafka-apis/configure-kafka-apis/consumers.md#create-a-subscription) instructions.
* To create a subscription from an existing application, follow the instructions below.
  1. Log in to your APIM Console
  2. Select **Applications** from the left nav
  3. Select **Subscriptions** from the inner left nav
  4.  Click the **+ Create a subscription** button

      <figure><img src="../.gitbook/assets/subscription_create 2.png" alt=""><figcaption><p><br>Create a subscription</p></figcaption></figure>
  5. Search for the API you want to subscribe to. To be searchable the API consumer must have access to the API, i.e., the API must be public or the API consumer must be a member of it.
  6.  Select the plan you would like to request a subscription to

      <figure><img src="../.gitbook/assets/subscription_create.png" alt=""><figcaption><p>Select the subscription plan</p></figcaption></figure>
  7. Click **Create** to see the subscription details

## Manage subscriptions

When creating a plan, you can enable subscription auto-validation to immediately approve subscription requests. If **Auto validate subscription** is disabled, the API publisher must approve all subscription requests.

{% hint style="info" %}
To be notified of subscription validation tasks, enable [Notifications](../configure-and-manage-the-platform/gravitee-gateway/notifications.md)
{% endhint %}

To manage subscriptions in APIM Console:

1. Log in to your APIM Console
2. Select **APIs** from the left nav
3. Select the API with subscriptions to manage
4. Select **Consumers** from the inner left nav
5. Click the **Subscriptions** header tab
6. Select the request or subscription you want to manage
7. Validate or reject the subscription
   *   If validating, fill out the **Validate your subscription** form, then click **Validate**

       <figure><img src="../.gitbook/assets/subscription_validate 2.png" alt=""><figcaption><p>Validate the subscription</p></figcaption></figure>

### API Key plans

Subscriptions to API Key plans include additional security management settings:

*   **Renew:** Generate a new API key or provide a custom API key. The existing API key will be automatically invalidated after two hours.

    <figure><img src="../.gitbook/assets/subscription_api key renew.png" alt=""><figcaption><p>Renew an API key</p></figcaption></figure>
*   **Revoke:** Immediately invalidate an existing API key. This option is reversible.

    <figure><img src="../.gitbook/assets/subscription_api key revoke.png" alt=""><figcaption><p>Revoke an API key</p></figcaption></figure>
*   **Expire:** Set a date/time to automatically invalidate an existing API key

    <figure><img src="../.gitbook/assets/subscription_api key expire.png" alt=""><figcaption><p>Expire an API key</p></figcaption></figure>

### mTLS plans

Subscriptions to mTLS plans require a client certificate for authentication. The certificate must be Base64-encoded PEM format and registered with the subscription.

#### Certificate-based subscription identification

Subscriptions for mTLS plans are uniquely identified by:
- API ID
- Client certificate fingerprint (MD5 hash of the certificate)

#### Subscription workflow

When an administrator creates a subscription for an mTLS plan:

1. The administrator uploads the client certificate in Base64-encoded PEM format
2. The gateway computes the MD5 hash of the certificate
3. The gateway registers the certificate in the subscription truststore manager

#### Authentication flow

When a client connects to an mTLS-secured API:

1. The client presents its certificate during the TLS handshake
2. The gateway extracts the certificate from the TLS session
3. The gateway computes the MD5 hash of the certificate
4. The gateway queries the subscription service using the API ID and certificate fingerprint
5. If a matching subscription is found and active, authentication succeeds
6. The connection is authorized under that subscription

{% hint style="info" %}
The exact UI workflow for uploading client certificates during subscription creation is not fully documented. Contact Gravitee support for guidance on registering client certificates with mTLS subscriptions.
{% endhint %}

#### Revoking mTLS subscriptions

When a subscription is revoked:
1. The subscription status is set to inactive
2. The client certificate is unregistered from the gateway's subscription truststore manager
3. Clients using this certificate can no longer connect to the API

### mTLS plans

Subscriptions to mTLS plans require a client certificate for authentication. The certificate must be Base64-encoded PEM format and registered with the subscription.

#### Certificate-based subscription identification

Subscriptions for mTLS plans are uniquely identified by:
- API ID
- Client certificate fingerprint (MD5 hash of the certificate)

#### Subscription workflow

When an administrator creates a subscription for an mTLS plan:

1. The administrator uploads the client certificate in Base64-encoded PEM format
2. The gateway computes the MD5 hash of the certificate
3. The gateway registers the certificate in the subscription truststore manager

#### Authentication flow

When a client connects to an mTLS-secured API:

1. The client presents its certificate during the TLS handshake
2. The gateway extracts the certificate from the TLS session
3. The gateway computes the MD5 hash of the certificate
4. The gateway queries the subscription service using the API ID and certificate fingerprint
5. If a matching subscription is found and active, authentication succeeds
6. The connection is authorized under that subscription

<!-- GAP: Exact UI workflow for uploading client certificate during subscription creation -->
<!-- GAP: Certificate validation feedback during upload -->

#### Revoking mTLS subscriptions

When a subscription is revoked:
1. The subscription status is set to inactive
2. The client certificate is unregistered from the gateway's subscription truststore manager
3. Clients using this certificate can no longer connect to the API

### mTLS plans

Subscriptions to mTLS plans require API consumers to provide a valid client certificate when subscribing. The certificate must be Base64-encoded and included in the subscription request's `clientCertificate` field. The Gateway calculates the MD5 hash of the certificate and uses it as the security token for subscription lookup.

For detailed instructions on subscribing to Kafka APIs with mTLS plans, see [Subscribe to Kafka APIs with mTLS Plans](create-and-configure-kafka-apis/configure-kafka-apis/subscribe-to-kafka-apis-with-mtls-plans.md).

#### Certificate-based subscription identification

Subscriptions for mTLS plans are uniquely identified by:
- API ID
- Client certificate fingerprint (MD5 hash of the certificate)

#### Subscription workflow

When an administrator creates a subscription for an mTLS plan:

1. The administrator provides the client certificate in Base64-encoded format
2. The Gateway computes the MD5 hash of the certificate
3. The Gateway registers the certificate in the subscription truststore manager

#### Authentication flow

When a client connects to an mTLS-secured API:

1. The client presents its certificate during the TLS handshake
2. The Gateway extracts the certificate from the TLS session
3. The Gateway computes the MD5 hash of the certificate
4. The Gateway queries the subscription service using the API ID and certificate fingerprint
5. If a matching subscription is found and active, authentication succeeds
6. The connection is authorized under that subscription

<!-- GAP: Exact UI workflow for uploading client certificate during subscription creation -->
<!-- GAP: Certificate validation feedback during upload -->

#### Revoking mTLS subscriptions

When a subscription is revoked:
1. The subscription status is set to inactive
2. The client certificate is unregistered from the Gateway's subscription truststore manager
3. Clients using this certificate can no longer connect to the API