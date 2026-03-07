### Policy Compatibility

Eleven policies support A2A Proxy APIs. Each policy declares supported phases (REQUEST, RESPONSE, or both) in its `plugin.properties` file.

| Policy | Supported Phases | Minimum Version |
|:-------|:-----------------|:----------------|
| Interrupt | REQUEST, RESPONSE | 2.1.0 |
| IP Filtering | REQUEST | 2.2.0 |
| Retry | REQUEST | 4.1.0 |
| RBAC | REQUEST | 2.1.0 |
| HTTP Callout | REQUEST, RESPONSE | 5.4.0 |
| Rate Limit | REQUEST | 4.3.0 |
| JavaScript | REQUEST, RESPONSE | 2.1.0 |
| Groovy | REQUEST, RESPONSE | 4.2.0 |
| AI Prompt Guard Rails | REQUEST | (version not specified) |
| Assign Attributes | REQUEST, RESPONSE | 3.2.0 |
| Transform Headers | REQUEST, RESPONSE | 5.2.0 |

Phase support is declared in each policy's `plugin.properties` file using the format `a2a_proxy=REQUEST,RESPONSE`.
