# AWS API Gateway

## Overview

AWS API Gateway is AWS's built-in API management solution and is commonly used to expose services running in the AWS cloud to the public internet.

## Prerequisites

In order to Federate AWS API Management APIs into Gravitee, you'll need permission to access the AWS API Management console, or you'll at least need access to somebody who does so that they can provide you with credentials that the agent will use to authenticate against AWS.

The minimum permissions required by the federation agent are described in the section called [Minimum AWS permissions required by the agent](aws-api-gateway.md#minimum-aws-permissions-required-by-the-agent).

You'll also need to be running Gravitee API Management version 4.4 or above, with an enterprise license.

For the federation agent to authenticate with Gravitee API Management, you'll also need an access token. Head to our dedicated guide on [how to create a service account and an access token](../federation-agent-service-account.md) for the federation agent.

## 1. Create an AWS API Management integration in the Gravitee APIM Console

Head to the Gravitee APIM Console, open the Integrations section in the left menu, and create a new AWS API Management integration.

Once you've created the integration, copy the integration ID that will be visible on the integration overview tab, you'll use this later:

<figure><img src="../../../.gitbook/assets/image (39).png" alt=""><figcaption></figcaption></figure>

## 2. Configure the AWS APIM federation agent

The AWS APIM federation agent will need the following configuration parameters in order to connect to your AWS account:

* AWS region
* AWS credentials
  * either an access key and secret
  * or you can also use IAM role or instanceRole-based authentication

To learn how to create an AWS access key for the agent, please follow [the guide provided by AWS](https://docs.aws.amazon.com/IAM/latest/UserGuide/id_credentials_access-keys.html).

To learn how to use IAM role-based authentication, please reach out to your Gravitee customer service or account representative. We'll be able to provide you with AWS CloudFormation templates to help you set this up.

## 3. Run the AWS APIM federation agent with Docker

In this guide, we'll run the federation agent using Docker.

Copy and save the following into a Docker Compose file called `docker-compose.yaml`:

```yaml
services:
  integration-agent:
    image: graviteeio/federation-agent-aws-api-gateway:${AGENT_VERSION:-latest}
    restart: always
    environment:
      - gravitee_integration_connector_ws_endpoints_0=${WS_ENDPOINTS}
      - gravitee_integration_connector_ws_headers_0_name=Authorization
      - gravitee_integration_connector_ws_headers_0_value=bearer ${WS_AUTH_TOKEN}
      - gravitee_integration_providers_0_configuration_accessKeyId=${AWS_ACCESS_KEY_ID}
      - gravitee_integration_providers_0_configuration_region=${AWS_REGION}
      - gravitee_integration_providers_0_configuration_secretAccessKey=${AWS_SECRET_ACCESS_KEY}
      - gravitee_integration_providers_0_integrationId=${INTEGRATION_ID}
      - gravitee_integration_providers_0_type=aws-api-gateway
      - gravitee_integration_providers_0_configuration_0_stage=${AWS_0_STAGE:-}
      - gravitee_integration_providers_0_configuration_1_stage=${AWS_1_STAGE:-}
```

Next, create a file named `.env` in the same directory. We'll use it to set the required Docker Compose variables. Fill the values in this file from those you obtained in [step 2](aws-api-gateway.md#id-2.-configure-the-azure-federation-agent).

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
# AGENT_VERSION=1.1.0

## AWS API MANAGEMENT PARAMETERS ##

# AWS Region, example: us-west-2
AWS_REGION=[your-aws-region]

# AWS stage filter, optional
# AWS_0_STAGE=prod
# AWS_1_STAGE=dev

# AWS Credentials. 
# Optional if you're using IAM Role-based authentication
AWS_ACCESS_KEY_ID=[your-key-id]
AWS_SECRET_ACCESS_KEY=[your-access-key]

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

<figure><img src="../../../.gitbook/assets/image (40).png" alt=""><figcaption></figcaption></figure>

If your **Agent Connection** still shows as `Disconnected`, then please inspect the agent's container logs. There you should find error logs that will help you troubleshoot.

## Minimum AWS permissions required by the agent

The following AWS PolicyDocument describes the minimum permissions required for the agent to be able to perform discovery of AWS assets as well as management of subscriptions to AWS API usage plans.

```yaml
PolicyDocument:
    Version: '2012-10-17'
    Statement:
        - Effect: Allow
          Action:
              - apigateway:GET
          Resource:
              - arn:aws:apigateway:*::/restapis
              - arn:aws:apigateway:*::/restapis/*
              - arn:aws:apigateway:*::/restapis/*/stages/*
              - arn:aws:apigateway:*::/usageplans
        - Effect: Allow
          Action:
              - apigateway:POST
          Resource:
              - arn:aws:apigateway:*::/apikeys
              - arn:aws:apigateway:*::/usageplans/*/keys
        - Effect: Allow
          Action:
              - apigateway:DELETE
          Resource:
              - arn:aws:apigateway:*::/apikeys/*
```
