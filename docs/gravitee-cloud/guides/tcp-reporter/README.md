# TCP Reporter

## Overview 

Custom Reporters enable API platform administrators to configure TCP-based log and metrics exporters that stream analytics data from Gravitee gateways to external monitoring systems. Reporters support TLS encryption, configurable retry logic, and selective data type filtering. This feature is available to enterprise customers with Galaxy or Universe tier licenses.

For more information about TCP reporter configuration, see [TCP Reporter](https://documentation.gravitee.io/apim/analyze-and-monitor-apis/reporters/tcp-reporter).

### Compatibility matrix 

| Reporter | APIM version |
| :--- | :--- |
| TCP TLS | 4.11.x and above |
| TCP Plain | Up to 4.11.x |

## Key Concepts

### Reporter Configuration

A custom reporter defines the connection parameters, security settings, and data selection rules for exporting gateway telemetry. Each reporter specifies a TCP endpoint (host and port), connection timeouts, reconnection behavior, and optional TLS certificates. Administrators select which data types to export (V2 Logs, V4 Metrics, Kafka event metrics, etc.) and link the reporter to one or more gateways.

<figure><img src="../../.gitbook/assets/gravitee-cloud-custom-reporters-step-04.png" alt="TCP reporter configuration form showing host, port, connection timeout, reconnect attempts, reconnect interval, and retry timeout fields"><figcaption></figcaption></figure>

### Gateway Linking

Reporters are deployed to gateways through a linking mechanism. A single reporter can be linked to multiple gateways, and each gateway can host multiple reporters. When a reporter is updated, all linked gateways with `DEPLOYED` status automatically receive the new configuration. Unlinking a reporter from a gateway triggers an asynchronous deletion job, transitioning the reporter status to `DELETING` until the job completes.

<figure><img src="../../.gitbook/assets/gravitee-cloud-custom-reporters-step-01.png" alt="Gateways table showing name, environment, and link status columns with an add gateways button"><figcaption></figcaption></figure>

### Data Type Selection

Administrators choose which telemetry streams to export from a predefined set of data types. Available types include V2 Logs, V2 Metrics, V4 Logs, V4 Metrics, V4 Message Logs, V4 Message Metrics, API Health Check Logs, and Kafka event metrics (operation, topic, application, API). 

For more information about data selection, see [Configuring Reporters and Selecting Fields](https://documentation.gravitee.io/apim/analyze-and-monitor-apis/reporters#configuring-reporters-and-selecting-fields).

<figure><img src="../../.gitbook/assets/gravitee-cloud-custom-reporters-step-02.png" alt="Data selection checklist showing logs and metrics options for V2 and V4 APIs, message logs, health check logs, and Kafka event metrics"><figcaption></figcaption></figure>

### TLS Security

Reporters support mutual TLS authentication using JKS or PFX keystores and truststores. When TLS is enabled, administrators upload certificate files (maximum 2 MB each) and provide encrypted passwords. The TLS Verify Client option controls whether the reporter validates the remote server's certificate. All sensitive fields (keystore passwords, truststore passwords) are encrypted using RSA-OAEP with SHA-256 before storage.

<figure><img src="../../.gitbook/assets/gravitee-cloud-custom-reporters-step-03.png" alt="TLS configuration form with enabled toggle, verify client checkbox, keystore type dropdown, keystore password field, and truststore upload options"><figcaption></figcaption></figure>

## Prerequisites

- Enterprise license with Galaxy or Universe tier
- `customReporters` release toggle enabled in the platform
- Account-level permissions to manage custom reporters
- TCP endpoint accessible from gateway network
- (Optional) JKS or PFX certificate files for TLS connections

To learn more about how to configure the TCP reporter, see the following articles:
<table data-view="cards"><thead><tr><th></th><th data-hidden data-card-target data-type="content-ref"></th></tr></thead><tbody><tr><td>Creating and Configuring Custom Reporters</td><td><a href="creating-and-configuring-custom-reporters.md">creating-and-configuring-custom-reporters.md</a></td></tr><tr><td>Custom Reporters Reference</td><td><a href="custom-reporters-reference.md">custom-reporters-reference.md</a></td></tr><tr><td>Managing Custom Reporter Deployments</td><td><a href="managing-custom-reporter-deployments.md">managing-custom-reporter-deployments.md</a></td></tr></tbody></table>