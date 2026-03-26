---
description: Set up IAM role-based authentication for the AWS API Gateway federation agent.
---

# AWS IAM Role-Based Authentication

## Overview

IAM role-based authentication enables the AWS API Gateway federation agent to authenticate without static access keys. The agent uses an EC2 instance role to assume a dedicated federation role, removing the need to manage and rotate long-lived credentials.

{% hint style="info" %}
To use IAM role-based authentication, deploy the federation agent on AWS (for example, an EC2 instance) and use federation agent version 4.7.5 or later. To deploy the agent with an access key ID and secret instead, on AWS or locally, use any federation agent version (4.x.x).
{% endhint %}

## Prerequisites

Before you begin, verify the following:

* Gravitee API Management version 4.4 or later, with an enterprise license. For more information about Enterprise edition, see [Enterprise Edition Licensing](https://documentation.gravitee.io/platform-overview/gravitee-platform/gravitee-offerings-ce-vs-ee/enterprise-edition-licensing#license-support).
* A Federation agent service account. For more information, see [Federation agent service account](https://documentation.gravitee.io/apim/govern-apis/federation/federation-agent-service-account).
* An AWS API Gateway integration created in the Gravitee APIM Console. For more information, see [Create an AWS API Management integration in the Gravitee APIM Console](https://documentation.gravitee.io/apim/govern-apis/federation/3rd-party-providers/aws-api-gateway#create-an-aws-api-management-integration-in-the-gravitee-apim-console).
* An EC2 instance running Amazon Linux 2 or Ubuntu, with Docker installed.
* The EC2 instance has internet access, or an appropriate NAT setup if it is in a private subnet.

## Set up IAM roles

IAM role-based authentication requires two roles:

1. **EC2 IAM role**: Attached to the EC2 instance. Grants permission to assume the federation instance role.
2. **Federation instance role**: Contains the API Gateway permissions that the federation agent requires. Trusts the EC2 IAM role.

### Create the EC2 IAM role

1. In the AWS IAM Console, click **Roles**, and then click **Create role**.
2. Select **AWS service** as the trusted entity type, and then select **EC2**.
3. Click **Next** to skip the permissions step (you add an inline policy after creation).
4. Name the role (for example, `gravitee-federation-ec2-role`) and click **Create role**.
5. Open the newly created role and click **Add permissions**, then **Create inline policy**.
6.  Switch to the **JSON** tab and paste the following policy:

    ```json
    {
      "Version": "2012-10-17",
      "Statement": [
        {
          "Effect": "Allow",
          "Action": "sts:AssumeRole",
          "Resource": "arn:aws:iam::<account-id>:role/federation-instance-role"
        }
      ]
    }
    ```

    Replace `<account-id>` with your AWS account ID.
7. Name the policy (for example, `AllowAssumeFederationRole`) and click **Create policy**.
8. Navigate to the EC2 Console, select your instance, click **Actions** > **Security** > **Modify IAM role**, and attach the EC2 IAM role.

AWS automatically configures the following trust relationship for this role:

```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Principal": {
        "Service": "ec2.amazonaws.com"
      },
      "Action": "sts:AssumeRole"
    }
  ]
}
```

### Create the federation instance role

1. In the AWS IAM Console, click **Roles**, and then click **Create role**.
2.  Select **Custom trust policy** and paste the following trust relationship:

    ```json
    {
      "Version": "2012-10-17",
      "Statement": [
        {
          "Effect": "Allow",
          "Principal": {
            "AWS": "arn:aws:iam::<account-id>:role/<EC2-role-name>"
          },
          "Action": "sts:AssumeRole"
        }
      ]
    }
    ```

    Replace `<account-id>` with your AWS account ID and `<EC2-role-name>` with the name of the EC2 IAM role you created (for example, `gravitee-federation-ec2-role`).
3. Click **Next** to skip the managed permissions step.
4. Name the role `federation-instance-role` and click **Create role**.
5. Open the newly created role and click **Add permissions**, then **Create inline policy**.
6.  Switch to the **JSON** tab and paste the following policy:

    ```json
    {
      "Version": "2012-10-17",
      "Statement": [
        {
          "Effect": "Allow",
          "Action": [
            "apigateway:GET"
          ],
          "Resource": [
            "arn:aws:apigateway:*::/restapis",
            "arn:aws:apigateway:*::/restapis/*",
            "arn:aws:apigateway:*::/restapis/*/stages/*",
            "arn:aws:apigateway:*::/usageplans"
          ]
        },
        {
          "Effect": "Allow",
          "Action": [
            "apigateway:POST"
          ],
          "Resource": [
            "arn:aws:apigateway:*::/apikeys",
            "arn:aws:apigateway:*::/usageplans/*/keys"
          ]
        },
        {
          "Effect": "Allow",
          "Action": [
            "apigateway:DELETE"
          ],
          "Resource": [
            "arn:aws:apigateway:*::/apikeys/*"
          ]
        }
      ]
    }
    ```
7. Name the policy (for example, `FederationAPIGatewayAccess`) and click **Create policy**.

## Configure and deploy the federation agent

After setting up the IAM roles, deploy the federation agent on the EC2 instance using Docker Compose.

1.  SSH into the EC2 instance and create a file named `docker-compose.yml` with the following content:

    ```yaml
    services:
      integration-agent:
        image: graviteeio/federation-agent-aws-api-gateway:${AGENT_VERSION:-latest}
        restart: always
        environment:
          - gravitee_integration_connector_ws_endpoints_0=${WS_ENDPOINTS}
          - gravitee_integration_connector_ws_headers_0_name=Authorization
          - gravitee_integration_connector_ws_headers_0_value=bearer ${WS_AUTH_TOKEN}
          - gravitee_integration_providers_0_type=aws-api-gateway
          - gravitee_integration_providers_0_integrationId=${INTEGRATION_ID}
          - gravitee_integration_providers_0_configuration_region=${AWS_REGION}
          # IAM role-based authentication
          - gravitee_integration_providers_0_configuration_roleArn=${AWS_ROLE_ARN}
          # Optional: Only if using Gravitee NextGen Cloud
          # - gravitee_cloud_token=${GRAVITEE_CLOUD_TOKEN}
    ```

    <div data-gb-custom-block data-tag="hint" data-style="info" class="hint hint-info"><p>When using IAM role-based authentication, do not include the <code>accessKeyId</code> and <code>secretAccessKey</code> environment variables. The agent uses the EC2 instance role to assume the federation instance role automatically.</p></div>
2.  Create a file named `.env` in the same directory and add the following environment variables:

    ```bash
    ## GRAVITEE PARAMETERS ##

    # Gravitee APIM management API URL, typically suffixed with /integration-controller
    WS_ENDPOINTS=https://[your-APIM-management-API-host]/integration-controller

    # Gravitee APIM token for the agent
    WS_AUTH_TOKEN=[your-token]

    # ID of the APIM integration you created for this agent
    INTEGRATION_ID=[your-integration-id]

    # If using Gravitee Next-Gen Cloud, include a Cloud Token for the Federation Agent
    # GRAVITEE_CLOUD_TOKEN=[your-cloud-token]

    # Specify a version of the agent (4.7.5 or later for IAM role-based auth)
    AGENT_VERSION=latest

    ## AWS PARAMETERS ##

    # AWS region, for example: us-west-2
    AWS_REGION=[your-aws-region]

    # ARN of the federation instance role
    AWS_ROLE_ARN=arn:aws:iam::[your-account-id]:role/federation-instance-role
    ```
3.  Replace the placeholder values with your own configuration:

    | Placeholder                       | Description                                     |
    | --------------------------------- | ----------------------------------------------- |
    | `[your-APIM-management-API-host]` | Your Gravitee APIM management API URL           |
    | `[your-token]`                    | Your Gravitee APIM service account access token |
    | `[your-integration-id]`           | The Integration ID from the Gravitee Console    |
    | `[your-aws-region]`               | Your AWS region (for example, `us-west-2`)      |
    | `[your-account-id]`               | Your AWS account ID                             |
4.  Pull the latest Docker image:

    ```bash
    docker compose pull
    ```
5.  Start the agent in the background:

    ```bash
    docker compose up -d
    ```
6.  Monitor the agent logs to verify it starts successfully:

    ```bash
    docker compose logs -f
    ```

### Verification

1. In the Gravitee API Management Console, refresh the Integrations page.
2. Verify that the agent status is **Connected**.
3.  If the agent status shows **Disconnected**, inspect the agent container logs for error messages:

    ```bash
    docker compose logs integration-agent
    ```

### What's next

* To discover APIs across multiple AWS accounts and regions using IAM roles, see [Multi-account and multi-region AWS API Gateway federation](https://documentation.gravitee.io/apim/govern-apis/federation/3rd-party-providers/aws-api-gateway/multi-account-and-multi-region-aws-api-gateway-federation).
* To learn about minimum AWS permissions required by the agent, see [Minimum AWS permissions required by the agent](https://documentation.gravitee.io/apim/govern-apis/federation/3rd-party-providers/aws-api-gateway#minimum-aws-permissions-required-by-the-agent).
* For more information about federation agent service accounts, see [Federation agent service account](https://documentation.gravitee.io/apim/govern-apis/federation/federation-agent-service-account).
