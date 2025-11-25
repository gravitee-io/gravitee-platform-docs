---
description: An overview about ibm api connect.
---

# IBM API Connect

IBM API Connect, or IBM APIC for short, is IBM's API management solution.

## Prerequisites

You'll need an IBM API Connect account. The agent works with both Cloud and on-premise versions of IBM APIC. It is generally expected to work with versions 10.0.5 and above, and may also work with older versions.

You'll also need to be running Gravitee API Management version 4.5 or above, with an enterprise license.

For the federation agent to authenticate with Gravitee API Management, you'll also need an access token. Head to our dedicated guide on [how to create a service account and an access token](../create-a-service-account-for-the-federation-agent.md) for the federation agent.

## 1. Create an IBM API Connect integration in the Gravitee APIM Console

Head to the Gravitee APIM Console, open the Integrations section in the left menu, and create a new IBM API Connect integration.

Once you've created the integration, copy the integration ID that will be visible on the integration overview tab, you'll use this later:

<figure><img src="broken-reference" alt=""><figcaption></figcaption></figure>

## 2. Configure the IBM API Connect agent

The Gravitee IBM API Connect federation agent will need the following configuration parameters in order to connect to your IBM APIC account:

* The URL of the IBM API Connect platform
* The name of the IBM API Connect organization
* Credentials to authenticate with IBM (client ID, client secret, and API key)

To locate the IBM API Connect organization name, open the IBM API Connect console and head to Home → Settings → Overview → Name.

The IBM API Connect federation agent requires an IBM API Connect API key in order to authenticate against the IBM management API.

An API key belongs to a user account in IBM. You can either create an API key for you personal user account, or (recommended) create a dedicated IBM APIC service account for the Gravitee federation agent.

Once you've chosen the account you want to use, to generate an API Key for that account you can click on the user profile icon in the top-right of the IBM APIC Console and select the **My API Keys** menu item. Alternatively, on older versions of IBM APIC, you can also append the `/apikey` path to the IBM APIC home page to access this page.

Once in the API key page, click on the **Add** button and generate a new key. If you don't see this button, you may not have the appropriate permissions in IBM to generate new API keys. Once you've created a key, IBM shows an example curl request that can be used to exchange the credentials against an access token that can be used to call the IBM APIC management API.

In this example curl request, you'll find the information you need to configure your agent:

* Client Id
* Client secret
* Platform API URL address

Copy these values, we'll use them to configure the agent.

{% hint style="info" %}
In case of trouble here you can find links to the official IBM documentation referring to this topic depending on the version you're using: [10.0.5](https://www.ibm.com/docs/en/api-connect/10.0.5.x_lts?topic=applications-managing-platform-rest-api-keys) / [10.0.8](https://www.ibm.com/docs/en/api-connect/10.0.8?topic=applications-managing-platform-rest-api-keys) / [SaaS](https://www.ibm.com/docs/en/api-connect/saas?topic=applications-managing-platform-rest-api-keys).
{% endhint %}

## 3. Run the IBM API Connect federation agent with Docker

In this guide, we'll run the federation agent using Docker.

Copy and save the following into a Docker Compose file called `docker-compose.yaml`:

```yaml
services:
  integration-agent:
    image: graviteeio/federation-agent-ibm-api-connect:1.0.0
    restart: always
    environment:
      - gravitee_integration_connector_ws_endpoints_0=${WS_ENDPOINTS}
      - gravitee_integration_connector_ws_headers_0_name=Authorization
      - gravitee_integration_connector_ws_headers_0_value=bearer ${WS_AUTH_TOKEN}
      - gravitee_integration_providers_0_integrationId=${INTEGRATION_ID}
      - gravitee_integration_providers_0_configuration_platformApiUrl=${PLATFORM_API_URL}
      - gravitee_integration_providers_0_configuration_clientId=${CLIENT_ID}
      - gravitee_integration_providers_0_configuration_clientSecret=${CLIENT_SECRET}
      - gravitee_integration_providers_0_configuration_organizationName=${ORGANIZATION_NAME}
      - gravitee_integration_providers_0_configuration_apiKey=${API_KEY}
      - gravitee_integration_providers_0_type=ibm-api-connect
```

Next, create a file named .env in the same directory. We'll use it to set the required Docker Compose variables. Fill the values in this file from those you obtained in [step 2](ibm-api-connect.md#id-2.-configure-the-ibm-api-connect-agent).

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

## IBM API CONNECT PARAMETERS ##

# IBM Platform API URL
PLATFORM_API_URL=[your-platform-api-url]

# IBM organization name
ORGANIZATION_NAME=[your-organization-name]

# IBM account client ID
CLIENT_ID=[your-client-id]

# IBM account client secret
CLIENT_SECRET=[your-client-secret]

# IBM account client secret
API_KEY=[your-api-key]
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

<figure><img src="broken-reference" alt=""><figcaption></figcaption></figure>

If your **Agent Connection** still shows as `Disconnected`, then please inspect the agent's container logs. There you should find error logs that will help you troubleshoot.
