### Console UI changes

The Console endpoint table includes a **Tenants** column that displays comma-separated tenant names for each endpoint. The column is hidden if no endpoint in the group has tenants configured.

The endpoint configuration form exposes a multi-select **Tenants** field populated from the organization's tenant list. Tenant descriptions are shown as tooltips. When a tenant ID has no matching tenant object in the organization, the raw tenant ID is displayed.

For runtime behavior and gateway configuration, see the main feature guide.
