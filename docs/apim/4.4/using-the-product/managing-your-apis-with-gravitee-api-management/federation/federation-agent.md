# Federation Agent

## Overview

A federation agent is an executable (e.g., `docker-compose` and configuration files) that integrates with a 3rd-party provider and communicates with an integration defined in Gravitee. For an integration to function, its associated agent to be properly configured and deployed. Agents are necessary because the Gravitee control plane (APIM Console and Management API) may not have direct network access to the 3rd-party provider’s management API.

<figure><img src="../../../.gitbook/assets/federation agent diagram.png" alt=""><figcaption></figcaption></figure>

Follow the steps below to set up and run a local instance of a federation agent that connects to a 3rd-party provider.

## 1. Generate an APIM Console access token

When an agent and APIM are connected, APIM verifies an access token to authenticate and authorize the connection. The framework that manages the communication between the agent and APIM relies on this token to ensure that the user has the "create" permission on the integration entity.

To generate the APIM Console access token:

1. Log in to your APIM Console
2. Click on the profile icon in the top right corner
3. From the drop-down menu, select **My account**&#x20;
4.  Scroll down to the **Personal access tokens** section of the page and click **GENERATE TOKEN**&#x20;

    <figure><img src="../../../.gitbook/assets/agent_generate token.png" alt=""><figcaption></figcaption></figure>

{% hint style="warning" %}
The access token will be displayed only once, so be sure to store it securely.&#x20;
{% endhint %}

## 2. Get the 3rd-party Integration ID

The **Integration ID** of the 3rd-party integration is required to configure and run the agent. Either [open an existing 3rd-party integration](integrations.md#view-or-edit-an-integration) or [create a new one](integrations.md#create-an-integration) to access the **Integration ID**, which is displayed on the integration's **Overview** page.&#x20;

<figure><img src="../../../.gitbook/assets/integration id.png" alt=""><figcaption></figcaption></figure>

## 3. 3rd-party agent configuration values

This section describes how to obtain the 3rd-party agent configuration values for each supported provider.&#x20;

{% tabs %}
{% tab title="AWS API Gateway" %}
### Requirements

* AWS Access Key
* Secret Access Key

### Generate the access keys

1. Log in to AWS
2. Click on your account name in the top right corner&#x20;
3. From the drop-down menu, choose **Security credentials** to open a window with your account details
4. On the AWS IAM credentials tab, find the **Access key** group with the **Create access key** button
5. Complete the access key creation wizard to generate an access key and a secret access key. Connectivity between the agent and AWS relies on both.

{% hint style="info" %}
There is a limit of two access keys per account. A deactivated access key still counts toward your limit of two access keys. Click [here](https://docs.aws.amazon.com/IAM/latest/UserGuide/id\_credentials\_access-keys.html) for more information.
{% endhint %}
{% endtab %}

{% tab title="Solace" %}
### Requirements

* Solace PubSub+ Cloud account access
* Solace API Token
* Solace integration created

### Generate the Solace API Token

To generate the Solace API Token, you must have a Solace PubSub+ Cloud account.

1. Log in to your Solace PubSub+ Cloud account
2. Click on your profile icon&#x20;
3. Choose the **Token Management** option
4. Click **Create token** in the top right corner to open the API Token creation wizard

{% hint style="info" %}
For more information, see the [Solace documentation](https://docs.solace.com/Cloud/ght\_api\_tokens.htm).
{% endhint %}
{% endtab %}
{% endtabs %}

## 3. Run the agent

The federation agent can be run using either Docker Compose or Helm. Instructions for how to run the supported 3rd-party agents using each method are detailed below.

### Docker Compose

The parameters required by the agent can be specified within a `docker-compose` file or using environment variables.

{% tabs %}
{% tab title="AWS API Gateway" %}
### Required parameters

* To connect to the right APIM integration:
  * Authorization token
  * Organization ID
  * Endpoint
* For the AWS API Gateway federation plugin:
  * Provider type (AWS API Gateway)
  * Gravitee Integration ID
  * AWS connection parameters (accessKeyId, secretAccessKey, region)

### 1. Create the `docker-compose` configuration

Use the example below as the basis for a `docker-compose` configuration file that will connect the federation agent image with APIM. This template relies on environment variables instead of hardcoded values.

```yaml
version: '3.8'

services:
  integration-agent:
    image: ${APIM_REGISTRY:-graviteeio}/integration-agent:${AGENT_VERSION:-latest}
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
```

### 2. Create the `.env` file

1.  Use the example below as the basis for the `.env` file that contains the variables to properly connect the agent to the AWS and APIM accounts.

    ```bash
    WS_ENDPOINTS=https://apim-master-api.team-apim.gravitee.dev/integration-controller
    WS_ORG_ID=DEFAULT
    APIM_REGISTRY=graviteeio.azurecr.io
    AGENT_VERSION=main-latest

    INTEGRATION_ID=[integration-id]
    AWS_ACCESS_KEY_ID=[aws-access-key]
    AWS_SECRET_ACCESS_KEY=[aws-secret-access-key]
    AWS_REGION=[aws-region]
    WS_AUTH_TOKEN=[ws-auth-token]
    ```



    {% hint style="warning" %}
    The `docker-compose` and `.env` files must be placed in the same folder.
    {% endhint %}
2. Replace the variable placeholders with the values appropriate to your environment:
   * Use the APIM access token as the value of WS\_AUTH\_TOKEN
   * Use the Integration ID as the value of INTEGRATION\_ID
   * Use the AWS Access Key as the value of AWS\_ACCESS\_KEY\_ID
   * Use the Secret Access Key as the value of AWS\_SECRET\_ACCESS\_KEY

### 3. Run `docker-compose`

Run the command `docker-compose up -d`&#x20;

### 4. Verify the connection between the agent and APIM

To verify that the connection between the agent and APIM has been established:

1. Log in to your APIM Console
2. Select **Integrations** from the left nav
3. Click on your AWS API Gateway integration
4. Select **Overview** from the inner left nav
5. Confirm the **Agent Connection** status is **Connected**

<figure><img src="https://slabstatic.com/prod/uploads/6lql0jy7/posts/images/preload/jqDkZSoYc4hjruKyh3pI6EXT.png" alt=""><figcaption></figcaption></figure>

{% hint style="info" %}
In case of issues with agent configuration, refer to the container logs.
{% endhint %}
{% endtab %}

{% tab title="Solace" %}
### 1. Create the `docker-compose` configuration

Use the example below as the basis for a `docker-compose` configuration file that will connect the federation agent image with APIM. This template relies on environment variables instead of hardcoded values.

```yaml
version: '3.8'

services:
  integration-agent:
    image: ${APIM_REGISTRY:-graviteeio}/federation-agent-solace:${AGENT_VERSION:-latest}
    restart: always
    environment:
      - gravitee_integration_connector_ws_endpoints_0=${WS_ENDPOINTS}
      - gravitee_integration_connector_ws_headers_0_name=Authorization
      - gravitee_integration_connector_ws_headers_0_value=bearer ${WS_AUTH_TOKEN}
      - gravitee_integration_providers_0_configuration_authToken=${SOLACE_AUTH_TOKEN}
      - gravitee_integration_providers_0_integrationId=${INTEGRATION_ID}
      - gravitee_integration_providers_0_type=solace
      - gravitee_integration_providers_0_configuration_url=${SOLACE_ENDPOINT:-https://api.solace.cloud/api/v2/architecture}
```

### 2. Create the `.env` file

1.  Use the example below as the basis for the `.env` file that contains the variables to properly connect the agent to the Solace and APIM accounts.

    ```bash
    WS_ENDPOINTS=https://apim-master-api.team-apim.gravitee.dev/integration-controller
    WS_ORG_ID=DEFAULT
    APIM_REGISTRY=graviteeio.azurecr.io
    AGENT_VERSION=main-latest

    INTEGRATION_ID=[integration-id]

    # in development phase we use this endpoint
    SOLACE_ENDPOINT=https://apim-production-api.solace.cloud/api/v2/apim
    SOLACE_AUTH_TOKEN=[solace-auth-token]
    WS_AUTH_TOKEN=[ws-auth-token]
    ```



    {% hint style="warning" %}
    The `docker-compose` and `.env` files must be placed in the same folder.
    {% endhint %}
2. Replace the variable placeholders with the values appropriate to your environment:
   * Use the APIM access token as the value of WS\_AUTH\_TOKEN
   * Use the Integration ID as the value of INTEGRATION\_ID
   * Use the Solace API Token as the value of SOLACE\_AUTH\_TOKEN

### 3. Run `docker-compose`

Run the command `docker-compose up -d`&#x20;

### 4. Verify the connection between the agent and APIM

To verify that the connection between the agent and APIM has been established:

1. Log in to your APIM Console
2. Select **Integrations** from the left nav
3. Click on your Solace integration
4. Select **Overview** from the inner left nav
5. Confirm the **Agent Connection** status is **Connected**

<figure><img src="https://slabstatic.com/prod/uploads/6lql0jy7/posts/images/preload/zDwPPaBJBgkrpcaX_aVxyaI6.png" alt=""><figcaption></figcaption></figure>

{% hint style="info" %}
In case of issues with agent configuration, refer to the container logs.
{% endhint %}
{% endtab %}
{% endtabs %}

### Run the agent using Helm

{% tabs %}
{% tab title="AWS API Gateway" %}

{% endtab %}

{% tab title="Solace" %}

{% endtab %}
{% endtabs %}

