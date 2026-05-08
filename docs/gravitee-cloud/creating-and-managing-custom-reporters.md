# Creating and Managing Custom Reporters

## Creating Custom Reporters

To create a custom reporter:

1. Navigate to account settings and select **Custom Reporters**.
2. Click **Create Custom Reporter**.
3. Configure the reporter name, host, port, and timeout values.
4. Select at least one data type to export from the available checkboxes.
5. (Optional) Enable TLS encryption:
   1. Toggle **TLS Enabled**.
   2. Select the keystore type (**JKS** or **PKCS12**).
   3. Upload the keystore file (maximum 2 MB).
   4. Enter the keystore password.
   5. Select the truststore type (**JKS** or **PKCS12**).
   6. Upload the truststore file (maximum 2 MB).
   7. Enter the truststore password.
6. (Optional) Link the reporter to one or more gateways.
7. Click **Save**.

The reporter is created and deployed to linked gateways asynchronously.

<figure><img src=".gitbook/assets/gravitee-cloud-custom-reporters-step-05.png" alt="Edit custom reporter page showing basic configuration, gateways section, connection settings, TLS configuration, and data selection"><figcaption></figcaption></figure>

## Managing Custom Reporters

### Updating a Reporter

To update a reporter:

1. Select the reporter from the list.
2. Modify the configuration fields (host, port, timeouts, data selection, or TLS settings).
3. Click **Save**.

Changes trigger automatic synchronization with all linked gateways.

{% hint style="info" %}
Password fields display a placeholder (`********`) in edit mode. To update a password, clear the placeholder and enter a new password. If no changes are made, the existing password is retained.
{% endhint %}

### Linking and Unlinking Gateways

To link a reporter to a gateway, use the gateway management interface to patch the reporter association. To unlink a reporter from a gateway, remove the reporter association from the gateway.

Gateway linking and unlinking operations are asynchronous and tracked by deployment jobs.

### Deleting a Reporter

To delete a reporter:

1. Select the reporter from the list.
2. Click **Delete**.

Deleting a reporter removes all gateway links and stops data export.

<figure><img src=".gitbook/assets/gravitee-cloud-custom-reporters-step-06.png" alt="Custom reporters management page showing a table with name, type, configuration, and output format columns"><figcaption></figcaption></figure>

## End-User Configuration

For information about configuring TCP reporters and selecting data fields, see the [TCP Reporter documentation](https://documentation.gravitee.io/apim/analyze-and-monitor-apis/reporters/tcp-reporter) and [Configuring Reporters and Selecting Fields](https://documentation.gravitee.io/apim/analyze-and-monitor-apis/reporters#configuring-reporters-and-selecting-fields).
