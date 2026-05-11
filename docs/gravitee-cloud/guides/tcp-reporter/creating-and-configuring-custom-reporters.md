# Creating and Configuring Custom Reporters

## Prerequisites

Before creating a custom reporter, ensure the following requirements are met:

* Enterprise license with Galaxy or Universe tier
* `customReporters` release toggle enabled in the platform
* Account-level permissions to manage custom reporters
* TCP endpoint accessible from gateway network
* (Optional) JKS or PKCS12 certificate files for TLS connections

## Creating a Custom Reporter

1. Access the custom reporters configuration page.
2. Click **Create Custom Reporter**.
3. Provide a unique name for the reporter.
 * Name must be 2-128 characters.
 * Allowed characters: alphanumeric, spaces, hyphens, underscores, and periods.
4. Configure the following connection settings:
 1. Enter the destination **Host** (maximum 255 characters, no protocol prefix or path).
 2. Enter the **Port** (1-65535).
 3. Set the **Connection Timeout** in milliseconds.
 4. Set the **Reconnect Attempts**.
 5. Set the **Reconnect Interval** in milliseconds.
 6. Set the **Retry Timeout** in milliseconds.

 <figure><img src="../../.gitbook/assets/gravitee-cloud-custom-reporters-step-06.png" alt="Connection settings form with host, port, connection timeout, reconnect attempts, reconnect interval, and retry timeout fields"><figcaption></figcaption></figure>

6. Select at least one data type to export from the available options.
7. (Optional) Enable TLS:
 1. Toggle **TLS Enabled**.
 2. (Optional) Enable **TLS Verify Client** to validate the remote server's certificate.
 3. Select the **Keystore Type** (JKS or PFK).
 4. Upload the keystore file (maximum 2 MB).
 5. Provide the encrypted keystore password.
 6. Select the **Truststore Type** (JKS or PFK).
 7. Upload the truststore file (maximum 2 MB).
 8. Provide the encrypted truststore password.
8. Link the reporter to one or more gateways.
9. Click **Save**.

<figure><img src="../../.gitbook/assets/gravitee-cloud-custom-reporters-step-04.png" alt="Edit custom reporter page showing basic configuration, gateway linking, connection settings, TLS configuration, and data selection sections"><figcaption></figcaption></figure>
