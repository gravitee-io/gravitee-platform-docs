# Push

## Overview

A Push plan is used when an API contains an entrypoint that sends message payloads to API consumers (e.g., Webhook). This type of plan is unique in that the security configuration is defined by the API consumer, in the subscription request created in the Developer Portal. For example, when subscribing to a Webhook entrypoint, the API consumer specifies the target URL and authentication for the Gateway to use when sending messages.

Push plans do not apply to SSE entrypoints. Although messages are pushed from the server, the client application initiates message consumption.

## Configuration

Push plans have the same configuration options as [Keyless](keyless.md) plans in APIM. The bulk of the configuration for a Push plan is set by the API consumer in the Developer Portal, and the content of the configuration varies by entrypoint type.

Gravitee currently supports Push plans for Webhook entrypoints.

### Key Push plan fields&#x20;

Before you approve a webhook subscription, verify the following field values:

| Field          | Description                                                             |
| -------------- | ----------------------------------------------------------------------- |
| Callback URL   | The full HTTPS endpoint that will receive the webhook.                  |
| TLS badge      | A lock icon confirms that the TLS certificate validation is enabled.    |
| Custom headers | Additional headers like `X-Signature` are forwarded with each delivery. |

### Retry strategy

The Gateway automatically retries technical failures occurring between the Gateway and the backend. For example, DNS errors or network transitional issues.&#x20;

Prior to Gravitee 4.8, the Gateway performed 5 retries at 3s intervals. After 5 retries, the subscription's status was set to FAILURE.

Starting with Gravitee 4.8, the Gateway performs retries indefinitely using exponential retries. With exponential retries, the subscription never fails when an issue occurs between the Gateway and the backend. Instead, the API publisher is notified after every 5 failed retries.

Here is a table that shows the retry configuration for your `gravitee.yml` file.

| Key                    | Default     | Description                                                                                                                                                                         |
| ---------------------- | ----------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `backoffStrategy`      | EXPONENTIAL | LINEAR or EXPONENTIAL. Configure the type of retry.                                                                                                                                 |
| `maxRetries`           | -1          | <p>The maximum number of retry attempts. Use -1 for infinite retries.<br>When the limit is reached, the subscription's status changes to FAILURE and message consumption stops.</p> |
| `maxDelayMs`           | -1          | The maximum delay after which retries stop. Used for exponential retry. Use -1 for infinite retries.                                                                                |
| `delayMs`              | 5000        | The initial delay, in milliseconds, for exponential retry, or the delay between retries for linear retry.                                                                           |
| `notificationInterval` | 5           | The number of retries after which the notification must be sent.                                                                                                                    |

Here is the default configuration in the `gravitee.yml` file:

```yaml
api:
  subscriptionEndpointRetry:
    backoffStrategy: EXPONENTIAL # LINEAR or EXPONENTIAL
    maxRetries: -1 # The maximum number of retries to attempt. -1 for infinite retries
    maxDelayMs: -1 # Maximum delay to reach to stop retrying for exponential retry. -1 for infinite retry
    delayMs: 5000 # The initial delay in milliseconds for exponential retry or the delay between retries for linear retry
    notificationInterval: 5 # Number of retries after which the notification needs to be sent
```
