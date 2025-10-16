# Solace

## Overview

Solace is an advanced event broker that enables an event mesh architecture.

## Prerequisites

Event Portal is a Solace product that acts like an API portal, but for Events. Gravitee's Solace federation agent relies in part on the Solace Event portal.

In order to Federate Solace Event APIs into Gravitee, you'll need permission to access the Solace console, or you'll at least need access to somebody who does so that they can provide you with credentials that the agent will use to authenticate against Solace's management API.

For more information about how to use the Solace Event portal to manage Event API, check out the getting started guide: [https://api.solace.dev/cloud/reference/apim-getting-started](https://api.solace.dev/cloud/reference/apim-getting-started).&#x20;

The minimum permissions required by the federation agent are described in the section called [Minimum Solace permissions required by the agent](solace.md#minimum-solace-permissions-required-by-the-agent). It is also worth taking a look at the Solace documentation about [authenticating against the Solace management API](https://api.solace.dev/cloud/reference/apim-getting-started#api-authentication).

You'll also need to be running Gravitee API Management version 4.4 or above, with an enterprise license.&#x20;

For the federation agent to authenticate with Gravitee API Management, you'll also need an access token. Head to our dedicated guide on [how to create a service account and an access token](../federation-agent-service-account.md) for the federation agent.

## 1. Create a Solace integration in the Gravitee APIM Console

Head to the Gravitee APIM Console, open the Integrations section in the left menu, and create a new Solace integration.&#x20;

Once you've created the integration, copy the integration ID that will be visible on the integration overview tab, you'll use this later:

<figure><img src="../../../.gitbook/assets/image (71).png" alt=""><figcaption></figcaption></figure>

## 2. Configure the Solace federation agent

The Solace federation agent will need the following configuration parameters in order to connect to your Solace instance:

* Solace endpoint
* Solace API token

The Solace endpoint to be used is common for all Solace customers:&#x20;

```properties
https://apim-production-api.solace.cloud/api/v2/apim
```

To generate Solace API Token you need to have Solace PubSub+ Cloud account first with a **manager** role (or higher).

When logged in, click on the profile icon and choose the _Token Management_ option.

In the top right corner, a Create token button opens a wizard for the API Token creation.

Please refer to the [Minimum Solace permissions required for the agent](solace.md#minimum-solace-permissions-required-by-the-agent).

## 3. Run the Solace federation agent with Docker

In this guide, we'll run the federation agent using Docker.

Copy and save the following into a Docker Compose file called `docker-compose.yaml`:

```yaml
services:
  integration-agent:
    image: graviteeio/federation-agent-solace:${AGENT_VERSION:-latest}
    restart: always
    environment:
      - gravitee_integration_connector_ws_endpoints_0=${WS_ENDPOINTS}
      - gravitee_integration_connector_ws_headers_0_name=Authorization
      - gravitee_integration_connector_ws_headers_0_value=bearer ${WS_AUTH_TOKEN}
      - gravitee_integration_providers_0_integrationId=${INTEGRATION_ID}
      - gravitee_integration_providers_0_type=solace
      - gravitee_integration_providers_0_configuration_authToken=${SOLACE_AUTH_TOKEN}
      - gravitee_integration_providers_0_configuration_url=${SOLACE_ENDPOINT:-https://apim-production-api.solace.cloud/api/v2/apim}
      - gravitee_integration_providers_0_configuration_0_appDomains=${SOLACE_APPLICATION_0_DOMAIN:-}
      # If you are using Gravitee NextGen Cloud, then you need to also include a Cloud Token for Federation Agent
      # - gravitee_cloud_token=${GRAVITEE_CLOUD_TOKEN}
```

Next, create a file named `.env` in the same directory. We'll use it to set the required Docker Compose variables. Fill the values in this file from those you obtained in [step 2](solace.md#id-2.-configure-the-azure-federation-agent).

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
# AGENT_VERSION=1.1.0

## SOLACE PARAMETERS ##

# Solace endpoint, this is common for all
SOLACE_ENDPOINT=https://apim-production-api.solace.cloud/api/v2/apim

# Solace API token
SOLACE_AUTH_TOKEN=[your-token]

# Optionally you can filter for one or more Solace application domains
SOLACE_APPLICATION_0_DOMAIN=[your-application-domain]
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

<figure><img src="../../../.gitbook/assets/Screenshot 2024-10-10 at 00.27.32.png" alt=""><figcaption></figcaption></figure>

If your **Agent Connection** still shows as `Disconnected`, then please inspect the agent's container logs. There you should find error logs that will help you troubleshoot.

## Minimum Solace permissions required by the agent

Below are the minimum permissions required by the agent in order to perform required operations against the Solace management API. Please review the details on [the official Solace documentation](https://api.solace.dev/cloud/reference/apim-getting-started#api-authentication) too.

```bash
mission_control:access
services:get:self
service_requests:post:client_profile
services:get
ep_environment:get:*
modeled_event_broker:get:*
modeled_event_mesh:get:*
apim_event_api_product:*:*
apim_event_api_product:get:*
application_domain:get:*
event_designer:access
```
