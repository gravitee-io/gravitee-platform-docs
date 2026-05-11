# Managing Custom Reporter Deployments

## Managing Reporter Deployments

After creating a reporter, monitor its deployment status on linked gateways. Reporters transition through `PENDING`, `DEPLOYED`, and `DELETING` states as deployment jobs execute. To update a reporter, modify its configuration or data selection; the platform automatically re-deploys the reporter to all gateways with `DEPLOYED` status (gateways in `PENDING` or `DELETING` states are skipped). To remove a reporter from a gateway, unlink it; this triggers an asynchronous deletion job that transitions the reporter to `DELETING` status until the job completes. Deployment failures are logged but don't block reporter creation or updates.

<figure><img src="../../.gitbook/assets/gravitee-cloud-custom-reporters-step-05.png" alt="Custom reporters management page displaying a table with reporter name, type, configuration, and output format columns"><figcaption></figcaption></figure>


