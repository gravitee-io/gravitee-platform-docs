# Custom Reporters Reference

## Restrictions

- Only TCP reporter type is supported
- Only JSON output format is supported
- Gateway Monitoring Metrics data type is always excluded from export
- Reporter names must match the pattern `^[a-zA-Z0-9\s\-_.]+$`
- Host field cannot contain protocol prefixes (`http://`, `https://`, `tcp://`) or paths
- Host field cannot contain whitespace or control characters
- TLS certificate files must be JKS or PKCS12 format
- TLS certificate files must be 2 MB or smaller
- When TLS is enabled, all three fields (type, password, content) must be provided for each store (keystore and truststore)
- Password fields display a masked placeholder (`********`) for existing values; actual passwords cannot be retrieved after initial entry
- Updating a reporter re-deploys only to gateways with `DEPLOYED` status (not `PENDING` or `DELETING`)
- Configuration keys changed from seconds to milliseconds in recent versions; existing reporters must migrate values (e.g., `connectionTimeoutSeconds: "30"` becomes `connectTimeout: "1000"`)
- Output format restriction changed from multiple formats (`json`, `csv`, `message_pack`, `elasticsearch`) to JSON only; existing reporters with non-JSON formats will fail validation on update

<figure><img src="../../.gitbook/assets/gravitee-cloud-custom-reporters-step-07.png" alt="Gateway selection dialog showing no eligible gateways found message with eligibility requirements"><figcaption></figcaption></figure>

## Related Changes

The custom reporters feature introduces a new settings page under account configuration, accessible via the `/accounts/:accountId/settings/custom-reporters` route. The UI includes an empty state with documentation links and a multi-step setup form for configuring TCP endpoints, connection parameters, TLS certificates, and data type selection. Password fields support a masked placeholder mode that displays `********` for existing values and clears on focus, restoring the placeholder if the user does not type a new value. File upload components validate certificate size (maximum 2 MB) and convert files to base64 before submission. The platform stores reporter configurations in a new `account_reporters` MongoDB collection and extends gateway documents with a `reporters` array tracking deployment status and job IDs. The feature is gated by a `customReporters` release toggle and requires Galaxy or Universe tier licenses.
