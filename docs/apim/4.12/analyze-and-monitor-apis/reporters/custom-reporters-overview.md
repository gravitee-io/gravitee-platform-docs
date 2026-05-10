# Custom Reporters Overview

## Overview

Custom Reporters enable API platform administrators to send gateway logs and metrics to external systems via TCP. Administrators configure reporters with connection details, TLS settings, and data type selection, then link them to one or more gateways for deployment. This feature extends TCP reporter capability to Gravitee-hosted gateways and requires an enterprise license (Galaxy or Universe tier).

For more information about TCP reporters, see [TCP Reporter](https://documentation.gravitee.io/apim/analyze-and-monitor-apis/reporters/tcp-reporter).

## Key Concepts

### Reporter Configuration

A custom reporter defines the connection parameters for a TCP endpoint that receives gateway telemetry data. Each reporter includes a name, TCP connection settings (host, port, timeouts, reconnection behavior), optional TLS configuration (keystore and truststore), and a selection of data types to export. Reporters are created at the account level and linked to specific gateways for deployment.

<figure><img src="../../.gitbook/assets/gravitee-cloud-custom-reporters-step-01.png" alt="Connection settings form with host, port, connection timeout, reconnect attempts, reconnect interval, and retry timeout fields"><figcaption></figcaption></figure>

### Data Type Selection

Administrators select which telemetry data types the reporter exports. Available types include v2 and v4 logs and metrics, message logs and metrics, API health check logs, and Kafka event metrics (operation, topic, application, and API events). The Gateway Monitoring Metrics type is always excluded from export, even if selected.

For more information about data selection, see [Configuring Reporters and Selecting Fields](https://documentation.gravitee.io/apim/analyze-and-monitor-apis/reporters#configuring-reporters-and-selecting-fields).

<figure><img src="../../.gitbook/assets/gravitee-cloud-custom-reporters-step-02.png" alt="Data selection checklist showing logs and metrics options for V2 and V4 APIs, message logs, health check logs, and Kafka event metrics"><figcaption></figcaption></figure>

| Data Type | Description |
|:----------|:------------|
| v2 Logs | Request/response logs from v2 APIs |
| v2 Metrics | Request metrics from v2 APIs |
| v4 Logs | Request/response logs from v4 APIs |
| v4 Metrics | Request metrics from v4 APIs |
| v4 Message Logs | Message-level logs from v4 APIs |
| v4 Message Metrics | Message-level metrics from v4 APIs |
| API Health Check Logs | Health check probe results |
| Kafka Operation Event Metrics | Kafka operation event telemetry |
| Kafka Topic Event Metrics | Kafka topic event telemetry |
| Kafka Application Event Metrics | Kafka application event telemetry |
| Kafka API Event Metrics | Kafka API event telemetry |

### TLS Configuration

Reporters support mutual TLS authentication with configurable keystore and truststore. Administrators upload JKS or PKCS12 files (max 2 MB each) and provide passwords. Keystore passwords and truststore passwords are encrypted at rest using RSA-OAEP/SHA-256. When TLS is enabled, administrators can optionally require client certificate verification.

<figure><img src="../../.gitbook/assets/gravitee-cloud-custom-reporters-step-03.png" alt="TLS configuration form with enabled toggle, verify client checkbox, keystore type dropdown, keystore password field, and truststore settings"><figcaption></figcaption></figure>

### Gateway Linking

Reporters are linked to gateways during creation or update. When a reporter is created with gateway IDs, the system deploys the reporter configuration to those gateways asynchronously. Updates to reporter configuration trigger re-deployment to all linked gateways. Deleting a reporter unlinks all gateways and removes the configuration from the data plane. A gateway can only have one reporter of each type linked (TCP type only supported today).

<figure><img src="../../.gitbook/assets/gravitee-cloud-custom-reporters-step-04.png" alt="Gateways table showing linked gateway with name, environment, and link status columns"><figcaption></figcaption></figure>

## Prerequisites

- Enterprise license with Galaxy or Universe tier
- Account role: Account Primary Owner or Cloud Account Owner
- Custom Reporters feature flag enabled (`releaseToggles.customReporters`)
- RSA public key configured for encryption (`gravitee_platform_encryption_public-key` environment variable)
- Target TCP endpoint accessible from gateway network
