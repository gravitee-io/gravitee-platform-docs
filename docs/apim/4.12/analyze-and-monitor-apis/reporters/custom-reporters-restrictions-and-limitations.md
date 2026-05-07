# Custom Reporters Restrictions and Limitations

## Restrictions

- Only `TCP_REPORTER` type is supported.
- Only `json` output format is supported. CSV, MessagePack, and Elasticsearch formats are not available.
- Gateway Monitoring Metrics are always excluded from data selection, even if explicitly selected.
- Keystore and truststore files are limited to 2 MB in the UI.
- Requires enterprise license with tier `galaxy` or `universe`. Accounts with tier `planet` or no license cannot access the feature.
- `customReporters` feature flag must be enabled in the `release_toggles` collection.
- Hostnames must be printable ASCII (no Unicode). IPv6 addresses must use bracket notation (e.g., `[2001:db8::1]`).
- Hostnames cannot include protocol prefixes (`http://`, `https://`, `tcp://`) or path segments.
- When keystore or truststore type is set, all three fields (type, password, content) are required.
- Existing passwords are masked as `********` in API responses. The encrypted value is not exposed.
- Gateway linking errors during create, update, or delete are logged but do not block the reporter operation.
- Gateways with status `PENDING` or `DELETING` are skipped during configuration updates.

<figure><img src="../../.gitbook/assets/gravitee-cloud-custom-reporters-step-07.png" alt="Gateway selection dialog showing no eligible gateways found message with eligibility requirements"><figcaption></figcaption></figure>

## Related Changes

