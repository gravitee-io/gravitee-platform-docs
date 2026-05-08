# Custom Reporters Overview

## Overview

Custom Reporters enable API platform administrators to stream API analytics and logs to external TCP endpoints in JSON format. Administrators configure reporters at the account level, link them to gateways, and select which data types (V2/V4 logs, metrics, health checks, Kafka events) to export. Reporters support TLS encryption with configurable keystores and truststores.

For detailed information about TCP reporter functionality and data export behavior, see the [TCP Reporter documentation](https://documentation.gravitee.io/apim/analyze-and-monitor-apis/reporters/tcp-reporter).

## Key Concepts

### Reporter Configuration

A custom reporter defines the TCP endpoint, connection behavior, and TLS settings for exporting analytics data. Each reporter is scoped to an account and can be linked to multiple gateways. Configuration includes host, port, timeout values (in milliseconds), reconnect behavior, and optional TLS encryption with keystore and truststore files.

<figure><img src="../../.gitbook/assets/gravitee-cloud-custom-reporters-step-01.png" alt="Connection settings form with host, port, connection timeout, reconnect attempts, reconnect interval, and retry timeout fields"><figcaption></figcaption></figure>

| Property | Description | Example |
|:---------|:------------|:--------|
| Name | Human-readable identifier (2-128 characters, alphanumeric + spaces - _ .) | `Production Logs` |
| Host | TCP endpoint hostname or IP (max 255 characters, no protocol prefix or path) | `logs.example.com` |
| Port | TCP port (1-65535) | `8514` |
| Connect Timeout | Connection timeout in milliseconds | `1000` |
| Reconnect Attempts | Number of reconnection attempts | `10` |
| Reconnect Interval | Delay between reconnection attempts in milliseconds | `500` |
| Retry Timeout | Maximum retry duration in milliseconds | `5000` |

### Data Selection

Administrators select which data types to export from a predefined list. Available types include V2 Logs, V2 Metrics, V4 Logs, V4 Metrics, V4 Message Logs, V4 Message Metrics, API Health Check Logs, and Kafka event metrics (Operation, Topic, Application, API). Gateway Monitoring Metrics is always excluded from selection, even if explicitly chosen. At least one data type must be selected.

For information about configuring data selection and field filtering, see [Configuring Reporters and Selecting Fields](https://documentation.gravitee.io/apim/analyze-and-monitor-apis/reporters#configuring-reporters-and-selecting-fields).

<figure><img src="../../.gitbook/assets/gravitee-cloud-custom-reporters-step-02.png" alt="Data selection checklist showing logs and metrics options for V2 and V4 APIs, message logs, health check logs, and Kafka event metrics"><figcaption></figcaption></figure>

### TLS Configuration

TLS encryption is optional and supports JKS and PKCS12 keystore and truststore formats. When TLS is enabled, administrators upload keystore and truststore files (≤ 2 MB each) and provide passwords. The **TLS Verify Client** option controls client certificate verification. If a keystore or truststore type is selected, the corresponding password and file content are required. Disabling TLS clears all TLS-related fields.

<figure><img src="../../.gitbook/assets/gravitee-cloud-custom-reporters-step-03.png" alt="TLS configuration form with enabled toggle, verify client checkbox, keystore type dropdown, keystore password field, and truststore settings"><figcaption></figcaption></figure>

| Property | Description | Allowed Values |
|:---------|:------------|:---------------|
| TLS Enabled | Enable TLS encryption | `true`, `false` |
| TLS Verify Client | Require client certificate verification | `true`, `false` |
| Keystore Type | Keystore format | `JKS`, `PKCS12`, None |
| Keystore Password | Keystore password (encrypted at rest) | — |
| Keystore Content | Base64-encoded keystore file | — |
| Truststore Type | Truststore format | `JKS`, `PKCS12`, None |
| Truststore Password | Truststore password (encrypted at rest) | — |
| Truststore Content | Base64-encoded truststore file | — |

### Gateway Linking

Reporters are linked to gateways to enable data export. Administrators can link a reporter to one or more gateways during creation or update. When a reporter's configuration or data selection changes, all linked gateways are automatically updated with the new settings. Deleting a reporter removes all gateway links. Each gateway can have only one reporter of each type (TCP is the only supported type). Each gateway tracks reporter deployment status (`DEPLOYED`, `PENDING`, `DELETING`) and the associated job ID.

<figure><img src="../../.gitbook/assets/gravitee-cloud-custom-reporters-step-04.png" alt="Gateways table showing name, environment, and link status columns with an add gateways button"><figcaption></figcaption></figure>

## Prerequisites

- Account must have a `galaxy` or `universe` license tier
- Account must be a customer account (`customer === true`)
- User must have `ACCOUNT_PRIMARY_OWNER` or `CLOUD_ACCOUNT_OWNER` role
- RSA public key must be configured for encrypting sensitive fields (keystore and truststore passwords)
- Custom Reporters feature flag must be enabled

## Managing Custom Reporters

To update a reporter, select it from the list and modify the configuration fields. Changes to host, port, timeouts, data selection, or TLS settings trigger automatic synchronization with all linked gateways. To link or unlink gateways, use the gateway management interface to add or remove gateway associations. Deleting a reporter removes all gateway links and stops data export.

<figure><img src="../../.gitbook/assets/gravitee-cloud-custom-reporters-step-06.png" alt="Custom reporters management page showing list of configured reporters with edit and delete actions"><figcaption></figcaption></figure>

When adding gateways to a reporter, use the gateway selection dialog to search and select eligible gateways in the account.

<figure><img src="../../.gitbook/assets/gravitee-cloud-custom-reporters-step-07.png" alt="Gateway selection dialog showing search field and list of available gateways with checkboxes"><figcaption></figcaption></figure>

