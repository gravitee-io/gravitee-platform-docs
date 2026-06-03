# Configuring the Import Whitelist

## Gateway Configuration

### Import Whitelist

Configure the import whitelist and private-address policy in the gateway's `ImportConfiguration` bean. All remote URLs used for API imports must match at least one pattern in the whitelist. Private and link-local addresses are rejected unless explicitly permitted.

| Property | Description | Example |
|:---------|:------------|:--------|
| `importWhitelist` | List of allowed URL patterns for remote imports. Patterns may use regex or glob syntax. | `["https://github.com/.*", "https://internal-repo.example.com/.*"]` |
| `allowImportFromPrivate` | Whether to permit imports from private or link-local IP ranges (e.g., `http://169.254.169.254/`). Defaults to `false`. | `false` |
