### Configuring Tenant Assignments in the Management Console

The endpoint configuration form includes a **Tenants** multi-select dropdown field. This field is displayed for all Native Kafka endpoints.

To assign tenants to a Native Kafka endpoint:

1. Open the endpoint editor for the Native Kafka endpoint.
2. Locate the **Tenants** field in the configuration form.
3. Select one or more tenants from the dropdown. Tenant names are displayed with descriptions shown on hover.
4. Save the endpoint configuration.

The selected tenant IDs are stored in the endpoint definition and used by gateways at runtime to filter endpoints.

### Restrictions

* Only the first matching endpoint in a group is selected. No load balancing occurs across tenant-filtered endpoints.
* If a gateway has a tenant configured and no endpoint matches, the API request fails with a `KafkaNoApiEndpointFoundException`.
* Tenant matching is exact and case-sensitive. Partial matches or wildcards are not supported.
* Endpoints with `null` or empty tenant lists match any gateway tenant, including gateways with no tenant configured.
* Gateways with no tenant configured match all endpoints, regardless of their tenant assignments.
