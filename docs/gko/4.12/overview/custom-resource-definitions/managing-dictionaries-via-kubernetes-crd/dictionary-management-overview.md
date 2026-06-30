# Dictionary management overview



Dictionary management lets administrators create, update, and delete dictionaries through the Automation API and the Kubernetes CRD. Dictionaries provide environment-scoped key-value data stores that can be referenced in API policies and configurations using Gravitee Expression Language. Policies can reference dictionary data at runtime. For configuration details, see [Dictionary Management](../../../guides/managing-dictionaries-via-automation-api.md). Manual dictionaries hold static properties, while dynamic dictionaries poll an external HTTP provider to refresh values automatically.

## Key concepts

The sections below describe the dictionary types, how dictionaries are identified, and how their deployment state works.

### Dictionary types

Dictionaries come in two types: `MANUAL` and `DYNAMIC`. Manual dictionaries store static key-value pairs defined at creation time. Dynamic dictionaries fetch properties from an external HTTP endpoint at scheduled intervals, using a JOLT transformation specification to map the response into key-value pairs.

| Type      | Properties source                       | Deployment behavior                   |
| --------- | --------------------------------------- | ------------------------------------- |
| `MANUAL`  | Static `properties` map                 | Deployed or undeployed on the gateway |
| `DYNAMIC` | HTTP provider with a JOLT specification | Polling provider started or stopped   |

### Dictionary key

The Gravitee Kubernetes Operator builds each dictionary's key from the namespace and name of the `Dictionary` resource, joined with a hyphen: `<namespace>-<name>`. For example, a dictionary named `e2e-dict-manual` in the `default` namespace has the key `default-e2e-dict-manual`. Reference this key in Gravitee Expression Language to read a dictionary property: `{#dictionaries['<namespace>-<name>']['<property>']}`.

### Deployment state

A dictionary's deployment state controls whether it's active on the gateway. For a manual dictionary, `deployed: true` deploys the dictionary to the gateway, and `deployed: false` undeploy it. For a dynamic dictionary, `deployed: true` start the polling provider and deploy the retrieved values to the gateway. Setting `deployed: false` stops the polling and undeploys the values from the gateway.
