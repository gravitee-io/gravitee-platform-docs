# Confluent Platform

## Prerequisites

The Confluent Platform federation agent supports both enterprise and community editions of Confluent Platform.

You'll also need to be running Gravitee API Management version 4.5 or above, with an enterprise license.

For the federation agent to authenticate with Gravitee API Management, you'll also need an access token. Head to our dedicated guide on [how to create a service account and an access token](../federation-agent-service-account.md) for the federation agent.

### Spinning up a test Confluent Platform environment

Confluent provides a demo project that you can easily be run locally.

It is a practical way to get started with the Confluent Platform federation agent.

A dedicated Git project is provided by Confluent and can be installed by following the instructions provided here:

{% embed url="https://docs.confluent.io/platform/current/tutorials/cp-demo/on-prem.html#docker" %}

For those that want a TL;DR, you can check out the repo and run a lightweight version of the project (with minimal dependencies) like so:

```bash
git clone https://github.com/confluentinc/cp-demo
cd cp-demo
git checkout 7.7.1-post
VIZ=false ./scripts/start.sh
```

Once started (which can take a few minutes), you should be able to open the Confluent Platform web console at [http://localhost:9021](http://localhost:9021).

## 1. Create a Confluent Platform integration in the Gravitee APIM Console

Head to the Gravitee APIM Console, open the Integrations section in the left menu, and create a new Confluent Platform integration.

Once you've created the integration, copy the integration ID that will be visible on the integration overview tab, you'll use this later:

<figure><img src="../../../../../.gitbook/assets/image (3).png" alt=""><figcaption></figcaption></figure>

## 2. Configure the Confluent Platform federation agent

The Confluent Platform federation agent will need the following configuration parameters in order to connect to your Confluent Platform instance:

* Cluster API endpoint
* Schema registry endpoint
* Confluent Platform credentials (user/password)

### Determine your cluster and schema registry endpoints

If you're running the Confluent demo project mentioned in the [Prerequisites](confluent-platform.md#prerequisites) on your local machine, which is where you also plan to run the agent for testing, then you can determine the cluster and schema registry endpoints as follows.

To find your local IP, run the following command in the terminal:

```bash
ipconfig getifaddr en0
```

This should provide an IP address as the output, for example `192.168.1.27`.

Based on this, the addresses you need are likely to be of the form:

```properties
CLUSTER_API_ENDPOINT=https://192.168.1.27:8091/kafka
SCHEMA_REGISTRY_ENDPOINT=https://192.168.1.27:8085
```

### Obtain Confluent credentials for the agent

The Confluent Platform federation agent needs credentials to be able to connect to the cluster and schema registry APIs.

If you're using the demo project mentioned in the Prerequisites, you can simply use the default super user account, where both user and password are set to `superUser`.

For non-development environments, we recommend that you create a dedicate principal in Confluent to be used by the Gravitee agent.

## 3. Run the Confluent Platform federation agent with Docker

In this guide, we'll run the federation agent using Docker.

Copy and save the following into a Docker Compose file called `docker-compose.yaml`:

```yaml
services:
    integration-agent:
        image: graviteeio/federation-agent-confluent-platform:latest
        restart: always
        environment:
            - gravitee_integration_connector_ws_endpoints_0=${WS_ENDPOINTS}
            - gravitee_integration_connector_ws_headers_0_name=Authorization
            - gravitee_integration_connector_ws_headers_0_value=Bearer ${WS_AUTH_TOKEN}
            - gravitee_integration_providers_0_integrationId=${INTEGRATION_ID}
            - gravitee_integration_providers_0_type=confluent-platform
            - gravitee_integration_providers_0_configuration_cluster_api_endpoint=${CLUSTER_API_ENDPOINT}
            - gravitee_integration_providers_0_configuration_schema_registry_endpoint=${SCHEMA_REGISTRY_ENDPOINT}
            - gravitee_integration_providers_0_configuration_auth_password=${BASIC_AUTH_LOGIN:-}
            - gravitee_integration_providers_0_configuration_auth_username=${BASIC_AUTH_PASSWORD:-}
            - gravitee_integration_providers_0_configuration_topic_prefix=${PREFIX:-}
            - gravitee_integration_providers_0_configuration_trust_all=${TRUST_ALL:-}
```

Next, create a file named `.env` in the same directory. We'll use it to set the required Docker Compose variables. Fill the values in this file from those you obtained in [step 2](confluent-platform.md#id-2.-configure-the-confluent-platform-federation-agent).

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

## CONFLUENT PLATFORM PARAMETERS ##

# Cluster API endpoint, example: https://192.168.1.27:8091/kafka
CLUSTER_API_ENDPOINT=[your-cluster-endpoint]

# Schema registry endpoint, example: https://192.168.1.27:8085
SCHEMA_REGISTRY_ENDPOINT=[your-schema-registry-endpoint]

# Credentials for Confluent Platform, example: superUser/superUser
BASIC_AUTH_LOGIN=[your-login]
BASIC_AUTH_PASSWORD=[your-password]

# Optional topic prefix filter
# Gravitee creates one API per topic in the cluster
# PREFIX allows you to only create APIs for topics that match the prefix
PREFIX=[your-prefix]

# Optional, for example set to TRUE to accept the self-signed cert when 
# using the Confluent Platform demo project
TRUST_ALL=true
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

<figure><img src="../../../../../.gitbook/assets/image (4).png" alt=""><figcaption></figcaption></figure>

If your **Agent Connection** still shows as `Disconnected`, then please inspect the agent's container logs. There you should find error logs that will help you troubleshoot.
