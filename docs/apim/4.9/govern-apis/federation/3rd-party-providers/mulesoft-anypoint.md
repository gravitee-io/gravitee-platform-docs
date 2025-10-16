# Mulesoft Anypoint

## Overview

Mulesoft Anypoint Platform is Mulesoft's API Management Solution

## Prerequisites

To start with the Mulesoft Federation Agent, you need access to the Mulesoft Anypoint Platform with permissions to manage and create Connected Apps.

## 1. Create a Mulesoft integration in the Gravitee APIM Console

Head to the Gravitee APIM Console, open the Integrations section in the left menu, and then create a new Mulesoft integration.

Once you have created the integration, copy the integration ID. The integration ID is visible on the integration overview tab. You will use this ID later.

<figure><img src="../../../.gitbook/assets/image (291).png" alt=""><figcaption></figcaption></figure>

## 2. Configure the Mulesoft agent

The Gravitee Mulesoft federation agent needs the following configuration parameters to connect to your Mulesoft Anypoint account:

* The Connected App Client ID and Client Secret
* Mulesoft Root Organization ID

#### How to Generate a Connected App

To generate a Connected App, navigate to Mulesoft's Access Management service. In the left menu, find the **Connected Apps** tab.

Clicking on **Connected Apps** tab shows a **Create App** button to create a new application.

The recommended approach is to create an app that acts on its own behalf.

When creating an app, you need to set the appropriate scopes to grant the app the necessary access for API ingestion. To do this, include the following scopes:

* **Exchange / Exchange Viewer**

The Gravitee Federation Agent ingests APIs only from the business groups selected for this scope. This can also be used as a filter to limit the ingestion to the business group you're interested in.

Once you have created the app, you should see the **clientID** and **clientSecret**, which are required to set up the agent.

In case of any issues, you can refer to this documentation for more information: [MuleSoft Documentation on Creating Connected Apps](https://docs.mulesoft.com/access-management/creating-connected-apps-dev).

#### Mulesoft Root Organization ID

To get the Mulesoft Root organization ID you need to navigate to Anypoint Platform → Access Management → Business Groups → Root Business Group → Settings tab → Business Group ID.

## 3. Run the Mulesoft federation agent with Docker

In this guide, we run the federation agent with Docker.

Copy and save the following into a Docker Compose file called `docker-compose.yaml`:

```yaml
version: '3.8'

services:
  integration-agent:
    image: ${APIM_REGISTRY:-graviteeio}/federation-agent-mulesoft:${AGENT_VERSION:-latest}
    restart: always
    environment:
      - gravitee_integration_connector_ws_endpoints_0=${WS_ENDPOINTS}
      - gravitee_integration_connector_ws_headers_0_name=Authorization
      - gravitee_integration_connector_ws_headers_0_value=bearer ${WS_AUTH_TOKEN}
      - gravitee_integration_providers_0_integrationId=${INTEGRATION_ID}
      - gravitee_integration_providers_0_type=mulesoft
      - gravitee_integration_providers_0_configuration_clientId=${CLIENT_ID}
      - gravitee_integration_providers_0_configuration_clientSecret=${CLIENT_SECRET}
      - gravitee_integration_providers_0_configuration_rootOrganizationId=${MULESOFT_ROOT_ORG_ID}
      # If you are using Gravitee NextGen Cloud, then you need to also include a Cloud Token for Federation Agent
      # - gravitee_cloud_token=${GRAVITEE_CLOUD_TOKEN}
```

Next, create a file named `.env` in the same directory. We will use it to set the required Docker Compose variables. Fill the values in this file from those you obtained in [step 2](mulesoft-anypoint.md#id-2.-configure-the-mulesoft-agent).

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
# AGENT_VERSION=1.3.0

## MULESOFT PARAMETERS ##

# Mulesoft Root Organization ID
MULESOFT_ROOT_ORG_ID=[your-mulesoft-root-org-id]

# Mulesoft Connected App Client ID
CLIENT_ID=[your-connected-app-client-id]

# Mulesoft Connected App Client Secret
CLIENT_SECRET=[your-connected-app-client-secret]
```

Run the following command to make sure you've got the latest available docker image:

```bash
docker compose pull
```

Then you can start the agent in the background with the following command:

```bash
docker compose up -d
```

In the Gravitee API Management console, after refreshing, you should now see the agent's status set to `Connected:`

<figure><img src="../../../.gitbook/assets/image (292).png" alt=""><figcaption></figcaption></figure>

If your **Agent Connection** still shows as `Disconnected`, then please inspect the agent's container logs. There you should find error logs that will help you troubleshoot.

## Limitations

The agent limits the size of the OpenAPI document to 1 000 000B (about 1MB). APIs with documentation in excess of this limit are ingested without documentation and generate a message in the agent logs:

{% code overflow="wrap" %}
```sh
The length of the API: ${apiId}/${ApiName} OAS document is too large ${sizeB} (${sizeHumanReadable}). The limit is {sizeB} (${sizeHumanReadable}). The document will not be ingested.
```
{% endcode %}
