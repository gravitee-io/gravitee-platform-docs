# IBM API Connect

## Prerequisites

You'll need an IBM API Connect account. The agent works with both Cloud and on-premise versions of IBM APIC. It is generally expected to work with versions 10.0.5 and above, and may also work with older versions.

You'll also need to be running Gravitee API Management version 4.5 or above, with an enterprise license.&#x20;

For the federation agent to authenticate with Gravitee API Management, you'll need an access token. Head to our dedicated guide on [how to create a service account and an access token](../federation-agent-service-account.md) for the federation agent.

## 1. Create an IBM API Connect integration in the Gravitee APIM Console

Head to the Gravitee APIM Console, open the Integrations section in the left menu, and create a new IBM API Connect integration.&#x20;

Once you've created the integration, copy the integration ID that will be visible on the integration overview tab (you'll use this later):

<figure><img src="../../../.gitbook/assets/image (44).png" alt=""><figcaption></figcaption></figure>

## 2. Configure the IBM API Connect agent

The Gravitee IBM API Connect federation agent will need the following configuration parameters to connect to your IBM APIC account:

* The URL of the IBM API Connect platform
* The name of the IBM API Connect organization
* Credentials to authenticate with IBM (client ID, client secret, and API key)

To locate the IBM API Connect organization name, open the IBM API Connect console and head to Home → Settings → Overview → Name.&#x20;

The IBM API Connect federation agent requires an IBM API Connect API key in order to authenticate against the IBM management API.

An API key belongs to a user account in IBM. You can either create an API key for you personal user account, or (recommended) create a dedicated IBM APIC service account for the Gravitee federation agent.

Once you've chosen the account you want to use, to generate an API Key for that account you can click on the user profile icon in the top-right of the IBM APIC Console and select the **My API Keys** menu item. Alternatively, on older versions of IBM APIC, you can also append the `/apikey` path to the IBM APIC home page to access this page.

Once in the API key page, click on the **Add** button and generate a new key. If you don't see this button, you may not have the appropriate permissions in IBM to generate new API keys. Once you've created a key, IBM shows an example curl request that can be used to exchange the credentials against an access token that can be used to call the IBM APIC management API.

In this example curl request, you'll find the information you need to configure your agent:

* Client Id
* Client secret&#x20;
* Platform API URL address

Copy these values, we'll use them to configure the agent.

{% hint style="info" %}
In case of trouble here you can find links to the official IBM documentation referring to this topic depending on the version you're using: [10.0.5](https://www.ibm.com/docs/en/api-connect/10.0.5.x_lts?topic=applications-managing-platform-rest-api-keys) / [10.0.8](https://www.ibm.com/docs/en/api-connect/10.0.8?topic=applications-managing-platform-rest-api-keys) / [SaaS](https://www.ibm.com/docs/en/api-connect/saas?topic=applications-managing-platform-rest-api-keys).
{% endhint %}

## 3. Run the IBM API Connect federation agent with Docker

In this guide, we'll run the federation agent using Docker.

Copy and save the following into a Docker Compose file called `docker-compose.yaml`:

```yaml
version: '3.8'

services:
  integration-agent:
    image: ${APIM_REGISTRY:-graviteeio}/federation-agent-ibm-api-connect:${AGENT_VERSION:-latest}
    restart: always
    environment:
      - gravitee_integration_connector_ws_endpoints_0=${WS_ENDPOINTS}
      - gravitee_integration_connector_ws_headers_0_name=Authorization
      - gravitee_integration_connector_ws_headers_0_value=bearer ${WS_AUTH_TOKEN}
      - gravitee_integration_providers_0_integrationId=${INTEGRATION_ID}
      # If you are using Gravitee Next-Gen Cloud, then you need to also include a Cloud Token for Federation Agent
      # - gravitee_cloud_token=${GRAVITEE_CLOUD_TOKEN}
      - gravitee_integration_providers_0_type=ibm-api-connect
      # authentication
      - gravitee_integration_providers_0_configuration_apiKey=${API_KEY}
      - gravitee_integration_providers_0_configuration_clientId=${CLIENT_ID}
      - gravitee_integration_providers_0_configuration_clientSecret=${CLIENT_SECRET}
      - gravitee_integration_providers_0_configuration_ibmInstanceType=${IBM_INSTANCE_TYPE:-cloud}
      # targeting
      - gravitee_integration_providers_0_configuration_organizationName=${ORGANIZATION_NAME}
      - gravitee_integration_providers_0_configuration_platformApiUrl=${PLATFORM_API_URL}
```

* If you are using a self-hosted instance or a cloud reserved instance, replace `cloud` with either `self-hosted` for a self-hosted instance or `cloud-reserved-instance` for a cloud reserved instance.&#x20;

Next, create a file named `.env` in the same directory. We'll use it to set the required Docker Compose variables. Fill the values in this file from those you obtained in [step 2](ibm-api-connect.md#id-2.-configure-the-ibm-api-connect-agent).&#x20;

Also, add the appropriate values according to your `IBM_INSTANCE_TYPE` configuration option. The configuration option has the following options:

* Cloud
* Self hosted&#x20;
* Cloud reserved instance

#### Cloud and self hosted instances

To authenticate your IBM API Connect federation agent to a Cloud or self hosted instance, you must provide the following details:

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

## IBM API CONNECT PARAMETERS ##

# IBM Platform API URL
PLATFORM_API_URL=[your-platform-api-url]

# IBM organization name
ORGANIZATION_NAME=[your-organization-name]

# IBM Instance Type (default is "cloud")
IBM_INSTANCE_TYPE=cloud

# IBM account client ID
CLIENT_ID=[your-client-id]

# IBM account client secret
CLIENT_SECRET=[your-client-secret]

# IBM account client secret
API_KEY=[your-api-key]
```

* If you are authenticating a self-hosted instance, change `IBM_INSTANCE_TYPE=cloud` to `IBM_INSTANCE_TYPE=self-hosted`.
* Replace \[your-client-id] with your client ID.
* Replace \[your-client-secret] with your client secret.
* Replace \[your-api-key] with your API key.

#### Cloud reserved instance

{% hint style="info" %}
You have to provide only your API key. If you provide a client id and a client secret, an error is returned.&#x20;
{% endhint %}

To authenticate your IBM API Connect federation agent to a Cloud reserved instance, you must provide the following details:

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
# AGENT_VERSION=1.3.0

## IBM API CONNECT PARAMETERS ##

# IBM Platform API URL
PLATFORM_API_URL=[your-platform-api-url]

# IBM organization name
ORGANIZATION_NAME=[your-organization-name]

# IBM Instance Type (default is "cloud")
IBM_INSTANCE_TYPE=cloud-reserved-instance

# IBM account client secret
API_KEY=[your-api-key]
```

* By default, the `IBM_INSTANCE_TYPE` is set to cloud. Ensure that you change the `IBM_INSTANCE_TYPE` to `cloud-reserved-instance`.
* Replace \[your-api-key] with your API key.

#### Configuring catalog filtering

You can configure your IBM API Connect agent to filter your catalogs that you wish to APIs from. To filter your catalogs, you must add the catalogs to your `docker-compose.yaml` like the following example:

```sh
version: '3.8'

services:
  integration-agent:
    image: ${APIM_REGISTRY:-graviteeio}/federation-agent-ibm-api-connect:${AGENT_VERSION:-latest}
    restart: always
    environment:
      - gravitee_integration_connector_ws_endpoints_0=${WS_ENDPOINTS}
      - gravitee_integration_connector_ws_headers_0_name=Authorization
      - gravitee_integration_connector_ws_headers_0_value=bearer ${WS_AUTH_TOKEN}
      - gravitee_integration_providers_0_integrationId=${INTEGRATION_ID}
      - gravitee_integration_providers_0_type=ibm-api-connect
      # authentication
      - gravitee_integration_providers_0_configuration_apiKey=${API_KEY}
      - gravitee_integration_providers_0_configuration_clientId=${CLIENT_ID}
      - gravitee_integration_providers_0_configuration_clientSecret=${CLIENT_SECRET}
      - gravitee_integration_providers_0_configuration_ibmInstanceType=${IBM_INSTANCE_TYPE:-cloud}
      # targeting
      - gravitee_integration_providers_0_configuration_organizationName=${ORGANIZATION_NAME}
      - gravitee_integration_providers_0_configuration_platformApiUrl=${PLATFORM_API_URL}
      - gravitee_integration_providers_0_configuration_0_catalog=${IBM_0_CATALOG:-}
      - gravitee_integration_providers_0_configuration_1_catalog=${IBM_1_CATALOG:-}
```

Also, in your `.env` file, add the following catalog parameters like the following example:&#x20;

```
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
# AGENT_VERSION=1.3.0

## IBM API CONNECT PARAMETERS ##

# IBM Platform API URL
PLATFORM_API_URL=[your-platform-api-url]

# IBM organization name
ORGANIZATION_NAME=[your-organization-name]

# IBM Instance Type (default is "cloud")
IBM_INSTANCE_TYPE=cloud-reserved-instance

# IBM account client secret
API_KEY=[your-api-key]

#Optional catalog filtering
#IBM_0_CATALOG=
#IBM_1_CATALOG=
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

<figure><img src="../../../.gitbook/assets/image (46).png" alt=""><figcaption></figcaption></figure>

If your **Agent Connection** still shows as `Disconnected`, then please inspect the agent's container logs. There you should find error logs that will help you troubleshoot.

## Limitations

The agent limits the size of the OpenAPI document to 1 000 000B (about 1MB). APIs with documentation in excess of this limit are ingested without documentation and generate a message in the agent logs:

{% code overflow="wrap" %}
```sh
The length of the API: ${apiId}/${ApiName} OAS document is too large ${sizeB} (${sizeHumanReadable}). The limit is {sizeB} (${sizeHumanReadable}). The document will not be ingested.
```
{% endcode %}

IBM API Connect, or IBM APIC for short, is IBM's API management solution.
