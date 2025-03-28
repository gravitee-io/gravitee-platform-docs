# Azure API Management

Azure API Management, or Azure APIM for short, is Azure's built-in API management solution and is commonly used to expose services running in the Azure cloud to the public internet.

## Prerequisites

In order to federate Azure API Management APIs into Gravitee, you'll need permission to access the Azure API Management console. At minimum, you'll need access to somebody who has permission and can provide you with credentials that the agent will use to authenticate against Azure APIM.

You'll also need to be running Gravitee API Management version 4.5 or above, with an enterprise license.&#x20;

For the federation agent to authenticate with Gravitee API Management, you'll need an access token. For more information, see our dedicated guide on [how to create a service account and an access token](../federation-agent-service-account.md) for the federation agent.

## 1. Create an Azure API Management integration in the Gravitee APIM Console

Log in to the Gravitee APIM Console, open the **Integrations** section in the left menu, and create a new Azure API Management integration.&#x20;

Once you've created the integration, copy the integration ID that will be visible on the integration overview tab. You'll use this later.

<figure><img src="../../.gitbook/assets/image (121).png" alt=""><figcaption></figcaption></figure>

## 2. Configure the Azure federation agent

The Azure APIM federation agent needs the following configuration parameters to connect to your Azure APIM account:

* Azure APIM Subscription ID
* Azure APIM Resource Group name
* Azure APIM Service name
* Azure APIM Tenant ID
* Azure credentials (App ID and App Secret)

### Point to the right Azure APIM instance

The easiest way to obtain much of this information is to use the [Azure CLI](https://learn.microsoft.com/en-us/cli/azure/install-azure-cli).&#x20;

Start by logging in:

```bash
az login
```

Next, you can list the tenants and subscriptions, as shown below:

```bash
az account list --output table --query '[].{Name:name, SubscriptionId:id, TenantId:tenantId}'
```

This should produce an output similar to the following:

```bash
Name           SubscriptionId                        TenantId
-------------  ------------------------------------  ------------------------------------
Gravitee       02ae5fba-...........................  b7389665-...........................
```

Copy the IDs of the Azure APIM tenant and subscription you want to use.

Next, run the following command to configure Azure CLI to work with your chosen subscription:

```bash
az account set --subscription <your-subscriptionId>
```

Once this is set, you can obtain the Service name and Resource Group name with the following command:

```bash
az apim list --query '[].{ServiceName:name, ResourceGroup:resourceGroup}' -o table
```

This should produce an output similar to the following:

```bash
ServiceName      ResourceGroup
---------------  ----------------------
my-service-name  my-resource-group-name
```

Copy both of these values.

Now you should have the 4 key pieces of information that you'll need in the next steps:

* Azure APIM Subscription ID
* Azure APIM Resource Group name
* Azure APIM Service name
* Azure APIM Tenant ID

### **Authenticate with Azure APIM**

The Gravitee Azure APIM federation agent needs to authenticate with the Azure APIM management API to perform actions like discovery and subscription management.

To achieve this, you'll need to create a Service Principal for the agent in Azure, and then assign it the `Contributor` role.

The easiest way to set this up is to use the [Azure CLI](https://learn.microsoft.com/en-us/cli/azure/install-azure-cli).&#x20;

To make it easier to run this command, you can use information you previously obtained from Azure to set the environment variables below:

```bash
RESOURCE_GROUP_NAME=[your-resource-group-name]
SERVICE_NAME=[your-service-name]
SUBSCRIPTION_ID=[your-subscription-id]
```

Once these are set, you can run the command to create the Azure Service Principal:

```bash
az ad sp create-for-rbac --role Contributor --scopes /subscriptions/${SUBSCRIPTION_ID}/resourceGroups/${RESOURCE_GROUP_NAME}/providers/Microsoft.ApiManagement/service/${SERVICE_NAME}
```

This should produce an output similar to the one shown below. Copy the **appId** and **password** to use later.

```json
{
  "appId": "12345",
  "displayName": "12345",
  "password": "12345",
  "tenant": "12345"
}
```

{% hint style="info" %}
You can also find some of the information needed by the agent by browsing the Azure APIM console.

![](<../../.gitbook/assets/image (120).png>)
{% endhint %}

## 3. Run the Azure federation agent with Docker

To run the federation agent using Docker, copy and save the following into a Docker Compose file called `docker-compose.yaml`:

```yaml
services:
  integration-agent:
    image: graviteeio/federation-agent-azure-api-management:${AGENT_VERSION:-latest}
    restart: always
    environment:
      # Gravitee-specific configuration
      - gravitee_integration_connector_ws_endpoints_0=${WS_ENDPOINTS}
      - gravitee_integration_connector_ws_headers_0_name=Authorization
      - gravitee_integration_connector_ws_headers_0_value=Bearer ${WS_AUTH_TOKEN}
      - gravitee_integration_providers_0_integrationId=${INTEGRATION_ID}
      - gravitee_integration_providers_0_type=azure-api-management
      # Azure APIM authentication
      - gravitee_integration_providers_0_configuration_auth_appId=${APP_ID}
      - gravitee_integration_providers_0_configuration_auth_appSecret=${APP_SECRET}
      - gravitee_integration_providers_0_configuration_auth_tenant=${TENANT_ID}
      - gravitee_integration_providers_0_configuration_subscription=${SUBSCRIPTION}
      - gravitee_integration_providers_0_configuration_resourceGroup=${RESOURCE_GROUP}
      - gravitee_integration_providers_0_configuration_service=${SERVICE}
      - gravitee_integration_providers_0_configuration_dev_email=${AZURE_DEV_EMAIL}
      - gravitee_integration_providers_0_configuration_dev_firstName=${AZURE_DEV_FIRST_NAME}
      - gravitee_integration_providers_0_configuration_dev_lastName=${AZURE_DEV_LAST_NAME}
```

Next, create a file named `.env` in the same directory. This file is used to set the required Docker Compose variables. Replace the values in this file with those you obtained in [step 2](azure-api-management.md#id-2.-configure-the-azure-federation-agent).

```bash
## GRAVITEE PARAMETERS ##

# Gravitee APIM management API URL, typically suffixed with the path /integration-controller
WS_ENDPOINTS=https://[your-APIM-management-API-host]/integration-controller

# Gravitee APIM token to be used by the agent
WS_AUTH_TOKEN=[your-token]

# ID of the APIM integration you created for this agent
INTEGRATION_ID=[your-integration-id]

# APIM organization ID, example: DEFAULT
WS_ORG_ID=[organization-id]

# Optionally specify a specific version of the agent, default will be latest
# AGENT_VERSION=2.0.0

## AZURE API MANAGEMENT PARAMETERS ##

# Azure APIM tenant ID
TENANT_ID=[your-tenant-id]

# Azure APIM subscription ID
SUBSCRIPTION=[your-subscription-id]

# Azure APIM resource group name
RESOURCE_GROUP=[your-resource-group]

# Azure APIM service name
SERVICE=[your-service]

# Azure APIM developer details
# This developer will be used as the owner of applications 
# that are created by Gravitee in Azure APIM
# Gravitee will create the developer if it doesn't already exist
# or will reuse an existing developer if it exist in Azure
# The provided email address will receive notifications from Azure
AZURE_DEV_EMAIL=[developer-email]
AZURE_DEV_FIRST_NAME=[developer-firstname]
AZURE_DEV_LAST_NAME=[developer-lastname]

# Azure APIM credentials
APP_ID=[your-app-id]
APP_SECRET=[your-app-secret]
```

Run the following command to make sure you've got the latest available Docker image:

```bash
docker compose pull
```

You can start the agent in the background with the following command:

```bash
docker compose up -d
```

In the Gravitee API Management Console, after refreshing, you should now see that the agent's status is set to `Connected`:

<figure><img src="../../.gitbook/assets/image (122).png" alt=""><figcaption></figcaption></figure>

If your **Agent Connection** still shows as `Disconnected`, then inspect the agent's container logs. There you should find error logs that will help you troubleshoot.

## Limitations

By default, the agent only ingests the APIs of products that have a single API. To change this behavior, you can set a configuration:

```yaml
            - gravitee_integration_providers_0_configuration_multipleApiByProduct=true
```
