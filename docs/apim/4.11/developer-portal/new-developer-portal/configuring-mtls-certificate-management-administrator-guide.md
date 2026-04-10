# Configuring mTLS Certificate Management (Administrator Guide)

## Gateway Configuration

### Portal Settings

The following properties control mTLS certificate management availability:

| Property | Description | Default |
|:---------|:------------|:--------|
| `portal.next.mtls.enabled` | Enables mTLS certificate management UI in the new Developer Portal | `false` |
| `portalNext.mtls.enabled` | Backend configuration property controlling mTLS certificate feature availability | `false` |

Both properties default to `false` and must be enabled to activate the feature. The `portalNext.mtls.enabled` property can be toggled in the Management UI under **Portal Settings → New Developer Portal** using the **Enable mTLS Certificate Management** toggle.


