---
description: Create a custom TCP reporter in Gravitee Cloud and link it to your gateways. Follow the steps from prerequisites through verification.
---

# Create a TCP reporter

## Prerequisites

Before creating a custom reporter, ensure you meet the following requirements:

* Enterprise license with Galaxy or Universe tier
* Account-level permissions to manage custom reporters
* TCP endpoint accessible from gateway network
* (Optional) JKS or PFX certificate files for TLS connections

## Creating a Custom Reporter

1. From the **Dashboard**, click **Settings**.
2. From the **Settings** menu, click **Custom Reporters**.
3. Click **Create Custom Reporter**.
4. From the **Reporter Type** list, select **TCP**.
5. In the **Reporter Name** field, enter a unique name for the reporter. The name must meet the following requirements:
 * Must be 2-128 characters.
 * Allowed characters: alphanumeric, spaces, hyphens, underscores, and periods.
6. Configure the following connection settings:
 1. Enter the destination **Host** (maximum 255 characters, no protocol prefix or path).
 2. Enter the **Port** (1-65535).
 3. Set the **Connection Timeout** in milliseconds.
 4. Set the **Reconnect Attempts**.
 5. Set the **Reconnect Interval** in milliseconds.
 6. Set the **Retry Timeout** in milliseconds.

 <figure><img src="../../.gitbook/assets/gravitee-cloud-custom-reporters-step-06.png" alt="Connection settings form with host, port, connection timeout, reconnect attempts, reconnect interval, and retry timeout fields"><figcaption></figcaption></figure>

7.  Link the reporter to one or more gateways. To link the reporter to a Gateway, complete the following sub-steps:
 1. Click **Add gateways**.
 2. In the **Select gateways to link** window, select the Gateways to link.
 3. Click **Add**. The button label includes the number of Gateways you selected, for example, **Add 2 gateways**.
8. (Optional) Enable TLS:
 1. Toggle **TLS Enabled**.
 2. (Optional) Enable **Verify Client** to validate the remote server's certificate.
 3. Select the **Keystore Type** (JKS or PFX).
 4. Upload the keystore file (maximum 2 MB).
 5. Provide the encrypted keystore password.
 6. Select the **Truststore Type** (JKS or PFX).
 7. Upload the truststore file (maximum 2 MB).
 8. Provide the encrypted truststore password.
9. From the **Data Selection** menu, select at least one data type to export from the available options.
10. Click **Save**.

<figure><img src="../../.gitbook/assets/gravitee-cloud-custom-reporters-step-04.png" alt="Edit custom reporter page showing basic configuration, gateway linking, connection settings, TLS configuration, and data selection sections"><figcaption></figcaption></figure>

## Verification 

Your Custom Reporter appears in the Custom Reporters screen.