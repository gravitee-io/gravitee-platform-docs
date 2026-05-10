# Creating and Managing Custom Reporters

## Managing Custom Reporters

<figure><img src=".gitbook/assets/gravitee-cloud-custom-reporters-step-06.png" alt="Custom reporters management page showing list of reporters with name, type, configuration, and output format columns"><figcaption></figcaption></figure>

### Updating a Reporter

To update a reporter, select it from the Custom Reporters table and click **Edit**. Modify connection settings, TLS configuration, or data type selection as needed. Update the list of linked gateways to add or remove deployments. Click **Save** to apply changes. The system re-deploys the updated configuration to all linked gateways asynchronously.

{% hint style="info" %}
Password fields in edit mode display a placeholder (`********`). Actual values are not retrievable from the backend.
{% endhint %}

### Deleting a Reporter

To delete a reporter, select it from the table and click **Delete**. The system unlinks all gateways and removes the reporter configuration from the data plane. Deletion is asynchronous; failures are logged but do not block the operation.

## End-User Configuration

<figure><img src=".gitbook/assets/gravitee-cloud-custom-reporters-step-07.png" alt="Gateway selection dialog showing eligible gateways with search functionality"><figcaption></figcaption></figure>

A reporter can be linked to multiple gateways, but a gateway can only have one reporter of each type linked. When adding gateways, the selection dialog displays only eligible gateways in the account.
