# Custom Reporters Management API Reference

## Management API Endpoints

**POST** `/cloud/accounts/{accountId}/custom-reporters`

Creates a custom reporter. Requires `ACCOUNT_PRIMARY_OWNER` or `CLOUD_ACCOUNT_OWNER` role. Returns the created reporter with status 201.

**GET** `/cloud/accounts/{accountId}/custom-reporters`

Lists all custom reporters for the account. Returns an array of reporters with status 200.

**GET** `/cloud/accounts/{accountId}/custom-reporters/{customReporterId}`

Retrieves a single reporter by ID. Returns the reporter with status 200.

**PUT** `/cloud/accounts/{accountId}/custom-reporters/{customReporterId}`

Updates a custom reporter. Triggers gateway synchronization if configuration or data selection changes. Returns the updated reporter with status 200.

**DELETE** `/cloud/accounts/{accountId}/custom-reporters/{customReporterId}`

Deletes a custom reporter and removes all gateway links. Returns status 204.

**PATCH** `/accounts/{accountId}/gateways/{gatewayId}/reporters`

Links a reporter to a gateway. Returns the updated gateway with status 200.

**DELETE** `/accounts/{accountId}/gateways/{gatewayId}/reporters/{reporterId}`

Unlinks a reporter from a gateway. Returns the updated gateway with status 200.

**POST** `/deployments/dp/{dataPlaneId}/reporters`

Deploys reporter configuration to a data plane. Returns a job ID with status 200.

## Restrictions

- Only TCP reporter type is supported
- Output format is restricted to JSON only
- Gateway Monitoring Metrics is always excluded from data selection
- TLS keystore and truststore files must be ≤ 2 MB
- Host field cannot contain protocol prefixes (`http://`, `https://`, `tcp://`) or path segments
- Reporter name is limited to 2-128 characters (alphanumeric, spaces, hyphens, underscores, periods)
- Port must be between 1 and 65535
- Requires `galaxy` or `universe` license tier
- Requires customer account status
- Password fields in edit mode display a placeholder; users must re-enter passwords to change them
- Gateway linking on reporter create/update is asynchronous; failures are logged but do not block the operation
