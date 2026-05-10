# Custom Reporters Management API Reference

### Management API

| Method | Path | Description |
|:-------|:-----|:------------|
| POST | `/cloud/accounts/{accountId}/custom-reporters` | Create a custom reporter |
| GET | `/cloud/accounts/{accountId}/custom-reporters` | List all custom reporters for the account |
| GET | `/cloud/accounts/{accountId}/custom-reporters/{reporterId}` | Retrieve a specific custom reporter |
| PUT | `/cloud/accounts/{accountId}/custom-reporters/{reporterId}` | Update a custom reporter |
| DELETE | `/cloud/accounts/{accountId}/custom-reporters/{reporterId}` | Delete a custom reporter |

| PATCH | `/gateways/{accountId}/{gatewayId}/reporters` | Link a reporter to a gateway |
| DELETE | `/gateways/{accountId}/{gatewayId}/reporters/{reporterId}` | Unlink a reporter from a gateway |
