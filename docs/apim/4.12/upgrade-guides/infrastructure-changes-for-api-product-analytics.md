# Infrastructure Changes for API Product Analytics

If you use the Elasticsearch reporter, APIM automatically applies the updated `v4-log` and `v4-metrics` index templates — which already include the `api-product-id` keyword mapping — during the upgrade; you do not need to edit the templates by hand. Because an index template only affects indices created after it is applied, existing indices keep working but do not gain the filterable field until they are rolled over. Roll over the `v4-log` and `v4-metrics` indices (or wait for the next scheduled rollover) so new indices pick up the mapping.

If you manage your Elasticsearch templates independently, add the `api-product-id` keyword mapping to your v4-metrics and v4-log index templates before upgrading to 4.12.
