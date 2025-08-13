---
hidden: true
---

# AWS API Gateway Multi-Account and Multi-Region

## Overview

This guide explains how to configure the AWS API Gateway Federation Agent to discover, ingest, and manage APIs across multiple AWS accounts and regions.&#x20;

Multi-account and multi-region support enables organizations to:

* Manage API management across all AWS accounts
* Maintain security boundaries while enabling cross-account access
* Scale API discovery across global infrastructure
* Configure API governance for large enterprises

## Prerequisites&#x20;

Before configuring multi-account support, ensure you have:

1. AWS Organizations Setup (for StackSets deployment):
   * AWS Organization with All Features enabled
   * Administrator access to the management account
   * Trusted access enabled between AWS CloudFormation and AWS Organizations
2. Agent Requirements:
   * Agent running in an AWS environment with an IAM identity (e.g., EC2 instance role, ECS task role)
   * Network connectivity to AWS API Gateway endpoints and Gravitee APIM
3. IAM Permissions:
   * The IAM identity running the agent must have permission to assume target roles across accounts
   * Each target role must have proper trust relationships and required permissions

#### Components

1. Management Account: Hosts the Federation Agent
2. Agent IAM Role: Has permissions to assume roles in target accounts
3. Target Accounts: Contains API Gateway resources to be discovered
4. Discovery IAM Roles: Roles in each target account with API Gateway read permissions
5. Trust Relationships: Allow cross-account role assumption

### Setup Options&#x20;

You can configure multi-account support using two approaches:

1. [#cloudformation-stacksets-deployment](aws-api-gateway-multi-account-and-multi-region.md#cloudformation-stacksets-deployment "mention"): Automated deployment across accounts
2. [#manual-iam-configuration](aws-api-gateway-multi-account-and-multi-region.md#manual-iam-configuration "mention"): Create roles and policies manually



### CloudFormation StackSets Deployment&#x20;

This approach uses AWS CloudFormation StackSets to deploy roles across multiple accounts.

{% hint style="info" %}
Make sure to enable:&#x20;

* AWS Organizations with `All Features`
* &#x20;Trusted access between CloudFormation and Organizations&#x20;
  * Sign in to the AWS Management Console as an administrator in your **management account**
  * Navigate to **AWS Organizations** → **Services**
  * Search for `CloudFormation`
  * Click on **AWS CloudFormation StackSets**
  * Click **Enable trusted access**
{% endhint %}

#### Create Stackset Administration Role&#x20;

In the management account:

1.  Create CloudFormation stack using the following template file named `AWSCloudFormationStackSetAdministrationRole.yml` with the following `yaml` content:\


    ```yaml
    AWSTemplateFormatVersion: 2010-09-09
    Description: Configure the AWSCloudFormationStackSetAdministrationRole to enable use of AWS CloudFormation StackSets.

    Parameters:
      AdministrationRoleName:
        Type: String
        Default: AWSCloudFormationStackSetAdministrationRole
        Description: "The name of the administration role. Defaults to 'AWSCloudFormationStackSetAdministrationRole'."
      ExecutionRoleName:
        Type: String
        Default: AWSCloudFormationStackSetExecutionRole
        Description: "The name of the execution role that can assume this role. Defaults to 'AWSCloudFormationStackSetExecutionRole'."

    Resources:
      AdministrationRole:
        Type: AWS::IAM::Role
        Properties:
          RoleName: !Ref AdministrationRoleName
          AssumeRolePolicyDocument:
            Version: 2012-10-17
            Statement:
              - Effect: Allow
                Principal:
                  Service: cloudformation.amazonaws.com
                Action:
                  - sts:AssumeRole
          Path: /
          Policies:
            - PolicyName: AssumeRole-AWSCloudFormationStackSetExecutionRole
              PolicyDocument:
                Version: 2012-10-17
                Statement:
                  - Effect: Allow
                    Action:
                      - sts:AssumeRole
                    Resource:
                      - !Sub 'arn:*:iam::*:role/${ExecutionRoleName}'
    ```



    * Stack name: `StackSetAdministrationRole`
2. Verify the role `AWSCloudFormationStackSetAdministrationRole` was created in IAM

#### Deploy Roles to target Accounts via StackSet&#x20;

1. **Download the template**:
   * [gravitee-target-assumed-roles.yml](https://drive.google.com/file/d/1yf4XlPsKIM15ToGx1ZKv0cQxL3yLvTo9/view?usp=drive_link)
2. **Create StackSet**:
   * Navigate to CloudFormation → StackSets → Create StackSet
   * Choose `Service-managed permissions`
   * Upload the template file
   * Specify StackSet details:
     * StackSet name: `GraviteeFederationRoles`
     * Parameters:
       * `AdminAccountId`: Your management account ID
   * Configure deployment options:
     * Select target **Organizational Units (OUs)** or specific **Account IDs**
     * Choose deployment regions
     * Leave execution role name as default: `AWSCloudFormationStackSetExecutionRole`
3. **Monitor deployment**:
   * Check StackSet operations for successful deployment
   * Verify roles created in target accounts

#### Deploy Federation Agent&#x20;

Use the provided CloudFormation template to deploy the agent:&#x20;

1. Download the template: [gravitee-federation-agent.yaml](https://drive.google.com/file/d/18slpMjKkzpn7ltGgyTHrkWry6832UsqB/view?usp=drive_link)
2. **Create stack** in management account:
   * Parameters:
     * `GraviteeAuth`: Your APIM authentication token
     * `GraviteeFederationImage`: Agent Docker image
     * `GraviteeFederationRegion`: Comma-separated regions (e.g., `us-east-1,eu-west-1`)
     * `GraviteeFederationUrl`: APIM management API URL
     * `GraviteeIntegrationId`: Your integration ID
     * `RoleArns`: Comma-separated list of target role ARNs

### Manual IAM Configuration&#x20;

#### Create discovery role in each target account

For each target AWS account, create an IAM role with API Gateway read permissions.

1. Navigate to IAM Console in the target account
2. Create a new role:
   * Choose `AWS Account` as trusted entity
   * Select `Another AWS account`
   * Enter the Management Account ID
   * Role name: `GraviteeFederationDiscoveryRole`
3.  Attach the following policy:\


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
        },
        {
          "Effect": "Allow",
          "Action": [
            "logs:DescribeLogGroups",
            "logs:DescribeLogStreams",
            "logs:GetLogEvents"
          ],
          "Resource": "*"
        }
      ]
    }
    ```
4.  **Update the trust policy with the following**:\


    ```json
    {
      "Version": "2012-10-17",
      "Statement": [
        {
          "Effect": "Allow",
          "Principal": {
            "AWS": "arn:aws:iam::<MANAGEMENT-ACCOUNT-ID>:role/<AGENT-ROLE-NAME>"
          },
          "Action": "sts:AssumeRole"
        }
      ]
    }
    ```

#### Configure Agent IAM Role in Management Account&#x20;

1.  **Attach AssumeRole policy**:\


    ```json
    {
      "Version": "2012-10-17",
      "Statement": [
        {
          "Sid": "AllowAssumeCrossAccountRoles",
          "Effect": "Allow",
          "Action": "sts:AssumeRole",
          "Resource": [
            "arn:aws:iam::<TARGET-ACCOUNT-1>:role/GraviteeFederationDiscoveryRole",
            "arn:aws:iam::<TARGET-ACCOUNT-2>:role/GraviteeFederationDiscoveryRole",
            "arn:aws:iam::<TARGET-ACCOUNT-3>:role/GraviteeFederationDiscoveryRole"
          ]
        }
      ]
    }
    ```

#### Test Cross-Account Access

1.  Verify the configuration using AWS CLI command:\


    ```bash
    # From the management account, test assuming a target role
    aws sts assume-role \
      --role-arn "arn:aws:iam::<TARGET-ACCOUNT>:role/GraviteeFederationDiscoveryRole" \
      --role-session-name "test-session"
    ```

### Agent Configuration

#### Docker Compose Configuration

For Docker-based deployments, configure multi-account support:

1.  **Create `.env` file**:\


    ```bash
    # Gravitee Configuration
    WS_ENDPOINTS=https://your-apim-host/integration-controller
    WS_AUTH_TOKEN=your-gravitee-token
    INTEGRATION_ID=your-integration-id

    # AWS Multi-Account Configuration
    AWS_REGION=us-east-1,eu-west-1,ap-southeast-1
    AWS_ROLE_ARNS=arn:aws:iam::111122223333:role/GraviteeFederationDiscoveryRole,arn:aws:iam::444455556666:role/GraviteeFederationDiscoveryRole

    # Optional
    ACCEPT_API_WITHOUT_USAGE_PLAN=true
    ```
2.  **Create `docker-compose.yml`**:\


    ```yaml
    version: '3.8'

    services:
      federation-agent:
        image: graviteeio/federation-agent-aws-api-gateway:${AGENT_VERSION:-latest}
        restart: always
        environment:
          # Gravitee connection
          - gravitee_integration_connector_ws_endpoints_0=${WS_ENDPOINTS}
          - gravitee_integration_connector_ws_headers_0_name=Authorization
          - gravitee_integration_connector_ws_headers_0_value=bearer ${WS_AUTH_TOKEN}
          
          # AWS provider configuration
          - gravitee_integration_providers_0_type=aws-api-gateway
          - gravitee_integration_providers_0_integrationId=${INTEGRATION_ID}
          
          # Multi-account and multi-region settings
          - gravitee_integration_providers_0_configuration_region=${AWS_REGION}
          - gravitee_integration_providers_0_configuration_roleArn=${AWS_ROLE_ARNS}
          
          # Additional options
          - gravitee_integration_providers_0_configuration_acceptApiWithoutUsagePlan=${ACCEPT_API_WITHOUT_USAGE_PLAN:-false}
    ```
3.  **Start the agent**:\


    ```bash
    docker-compose up -d
    ```

#### Configuration Behaviour

* **Region × Account Matrix**: The agent discovers APIs in every combination of region and account
* **Parallel Discovery**: Multiple discoveries run concurrently for efficiency
* **Metadata Tagging**: Each discovered API is tagged with source account and region

#### Environment Variables Reference

| Variable                        | Description                         | Example                                                   |
| ------------------------------- | ----------------------------------- | --------------------------------------------------------- |
| `AWS_REGION`                    | Comma-separated list of AWS regions | `us-east-1,eu-west-1`                                     |
| `AWS_ROLE_ARNS`                 | Comma-separated list of role ARNs   | `arn:aws:iam::123:role/Role1,arn:aws:iam::456:role/Role2` |
| `ACCEPT_API_WITHOUT_USAGE_PLAN` | Include APIs without usage plans    | `true` or `false`                                         |

When both `AWS_REGION` and `AWS_ROLE_ARNS` are set, the agent performs discovery and ingestion for **every combination** of `<region, account>` — resulting in a full `regions × accounts` scan.

It is currently not possible to assign specific regions to specific AWS accounts. The agent will iterate over all combinations provided.

### Subscription Management

#### Multi-Account Subscription Support

The agent supports subscription operations across accounts:

1. Creating Subscriptions: Automatically routes to correct account/region
2. Revoking Subscriptions: Uses metadata to identify target account
3. API Key Management: Keys appear in both APIM Console and Portal

### Important Upgrade Considerations

Migrating from Single to Multi-Account (v4.8 to v4.9)

Migration Limitation: Existing subscriptions created in single-account mode cannot be revoked after upgrading to multi-account mode due to missing routing metadata.

Recommended Migration Process:

1. Create new integration for multi-account setup
2. Re-discover all APIs using new configuration
3. Recreate subscriptions as needed
4. Deprecate old integration once migration complete

No Action Required If:

* Continuing with single-account setup after upgrade
* Starting fresh with v4.9 or later
* Not migrating existing subscriptions

