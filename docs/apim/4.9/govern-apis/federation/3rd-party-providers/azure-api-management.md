# Azure API Management

## Prerequisites

In order to Federate Azure API Management APIs into Gravitee, you'll need permission to access the Azure API Management console, or you'll at least need access to somebody who does so that they can provide you with credentials that the agent will use to authenticate against Azure APIM.

You'll also need to be running Gravitee API Management version 4.5 or above, with an enterprise license.

For the federation agent to authenticate with Gravitee API Management, you'll also need an access token. Head to our dedicated guide on [how to create a service account and an access token](../federation-agent-service-account.md) for the federation agent.

## 1. Create an Azure API Management integration in the Gravitee APIM Console

Head to the Gravitee APIM Console, open the Integrations section in the left menu, and create a new Azure API Management integration.

Once you've created the integration, copy the integration ID that will be visible on the integration overview tab, you'll use this later:

<figure><img src="../../../../../../.gitbook/assets/image (119) (1).png" alt=""><figcaption></figcaption></figure>

## 2. Configure the Azure federation agent

The Azure APIM federation agent will need the following configuration parameters in order to connect to your Azure APIM account:

* Azure APIM Subscription ID
* Azure APIM Resource Group name
* Azure APIM Service name
* Azure APIM Tenant ID
* Azure credentials (App Id and App Secret)

### Point to the right Azure APIM instance

The easiest way to obtain much of this information is to use the [Azure CLI](https://learn.microsoft.com/en-us/cli/azure/install-azure-cli).

Start by login in:

```bash
az login
```

Then you can list the tenants and subscriptions like so:

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

Now run the following command to configure Azure CLI to work with your chosen subscription:

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

Now you should have these 4 key pieces of information that you'll need in the next steps:

* Azure APIM Subscription ID
* Azure APIM Resource Group name
* Azure APIM Service name
* Azure APIM Tenant ID

### **Authenticate with Azure APIM**

Finally, the Gravitee Azure APIM federation agent will need to authenticate with the Azure APIM management API in order to perform actions like discovery and subscription management.

To achieve this, you'll need to create a Service Principal for the agent in Azure, and assign it the `Contributor` role.

The easiest way to set this up is to use the [Azure CLI](https://learn.microsoft.com/en-us/cli/azure/install-azure-cli).

To make it easier to run this command, you can start by setting a couple of environment variables based on previously obtained Azure information:

```bash
RESOURCE_GROUP_NAME=[your-resource-group-name]
SERVICE_NAME=[your-service-name]
SUBSCRIPTION_ID=[your-subscription-id]
```

Once these are set, you can run the command to create the Azure service principal:

```bash
az ad sp create-for-rbac --role Contributor --scopes /subscriptions/${SUBSCRIPTION_ID}/resourceGroups/${RESOURCE_GROUP_NAME}/providers/Microsoft.ApiManagement/service/${SERVICE_NAME}
```

This should produce an output similar to below, you'll need to copy the **appId** and **password** for use later:

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

<img src="../../../../../../.gitbook/assets/image (116) (1).png" alt="" data-size="original">
{% endhint %}

## 3. Run the Azure federation agent with Docker

In this guide, we'll run the federation agent using Docker.

Copy and save the following into a Docker Compose file called `docker-compose.yaml`:

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
      # If you are using Gravitee Next-Gen Cloud, then you need to also include a Cloud Token for Federation Agent
      # - gravitee_cloud_token=${GRAVITEE_CLOUD_TOKEN}
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
      - gravitee_integration_providers_0_configuration_subscriptionApprovalType=${SUBSCRIPTION_APPROVAL_TYPE:-ALL}
```

Next, create a file named `.env` in the same directory. We'll use it to set the required Docker Compose variables. Fill the values in this file from those you obtained in [step 2](azure-api-management.md#id-2.-configure-the-azure-federation-agent).

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

# If you are using Gravitee Next-Gen Cloud, then you also need to include a Cloud Token for Federation Agent (https://documentation.gravitee.io/apim/hybrid-installation-and-configuration-guides/next-gen-cloud#cloud-token)
# GRAVITEE_CLOUD_TOKEN=[your-cloud-token-for-federation-agent]

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

# Azure APIM API products can have subscription validation set to manual or automatic.
# This parameter determines if we ingest either or both of these API product types.
# Possible values are [MANUAL|AUTOMATIC|ALL], default is ALL
SUBSCRIPTION_APPROVAL_TYPE=ALL
```

Run the following command to make sure you've got the latest available Docker image:

```bash
docker compose pull
```

Then you can start the agent in the background with the following command:

```bash
docker compose up -d
```

In the Gravitee API Management Console, after refreshing, you should now see the agent's status set to `Connected:`

<figure><img src="../../../../../../.gitbook/assets/image (120) (1).png" alt=""><figcaption></figcaption></figure>

If your **Agent Connection** still shows as `Disconnected`, then please inspect the agent's container logs. There you should find error logs that will help you troubleshoot.

## Limitations

By default, the agent only ingests the APIs of products that have a single API. To change this behavior, you can set a configuration:

```yaml
            - gravitee_integration_providers_0_configuration_multipleApiByProduct=true
```

Azure API Management, or Azure APIM for short, is Azure's built-in API management solution and is commonly used to expose services running in the Azure cloud to the public internet.
