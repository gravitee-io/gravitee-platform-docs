# Apigee X

Apigee X is Google Cloud Platform's predominant API management solution.

## Prerequisites

You'll need access to an Apigee X account that includes access to features like Apigee API products.

The account will need a minimum set of permissions in order for the federation agent to do its job. The minimum permissions are described in section [Minimum Apigee permissions required by the agent](apigee-x.md#minimum-apigee-permissions-required-by-the-agent).

You'll also need to be running Gravitee API Management version 4.4 or above, with an enterprise license.

For the federation agent to authenticate with Gravitee API Management, you'll also need an access token. Head to our dedicated guide on [how to create a service account and an access token](docs/apim/4.6/federation/federation-agent-service-account.md) for the federation agent.

## 1. Create an Apigee X integration in the Gravitee APIM Console

Head to the Gravitee APIM Console, open the Integrations section in the left menu, and create a new Apigee X integration.

Once you've created the integration, copy the integration ID that will be visible on the integration overview tab, you'll use this later:

<figure><img src="../../../../../.gitbook/assets/image (121).png" alt=""><figcaption></figcaption></figure>

## 2. Configure the Apigee X federation agent

The Apigee X federation agent will need the following configuration parameters in order to connect to your Apigee X account:

* A Google Cloud Platform **project ID**
* Google Cloud **Service Account** with the correct set of permissions
* **Service Account Key** for the Service Account

### Obtain the project ID

To find the ID of the Google Cloud project you want to work with, you can head to the GCP console and open the Project drop down in the header bar. In there, you should be able to find your desired project's ID:

<figure><img src="../../../../../.gitbook/assets/image (122).png" alt=""><figcaption></figcaption></figure>

### Create a GCP service account key for the agent

To generate a Service Account Key you need to create a service account first. Please view the dedicated GCP docs on [How to create a GCP Service Account](https://cloud.google.com/iam/docs/service-accounts-create).

Once your service account is created, enter the GCP IAM application and choose the _Service Accounts_ tab from the menu bar on the left side. Then select your service account and click on the _Keys_ tab → _Add key_ button → _Create new key_ button _→ Key type: JSON →_ Save the key on your compute&#x72;_._

<figure><img src="../../../../../.gitbook/assets/Screenshot 2024-10-09 at 17.52.53.png" alt=""><figcaption></figcaption></figure>

In step 3, we'll show you how to configure your agent's Docker Compose file. There are two ways in which you can pass the service account key as a parameter in Docker Compose.

1. Referencing the service account key file on your filesystem by providing a path
2. Passing the service account key inline

With the first option, you must include a `SERVICE_ACCOUNT_KEY_PATH` variable with your docker-compose configuration.

For the inline method, you need to provide the full content of your Service Account Key and paste it directly into your docker-compose file. **The key must be put in between apostrophes (`'content'`).** For this option, you must use the `SERVICE_ACCOUNT_KEY_INLINE`parameter name with your docker-compose file.

{% hint style="warning" %}
You can only choose one authentication method. Providing two authentication methods in one configuration will result in an error!
{% endhint %}

## 3. Run the Apigee X federation agent with Docker

In this guide, we'll run the federation agent using Docker.

Copy and save the following into a Docker Compose file called `docker-compose.yaml`:

```yaml
services:
  integration-agent:
    image: graviteeio/federation-agent-apigee:latest
    restart: always
    volumes:
      - ${SERVICE_ACCOUNT_KEY_PATH:-/dev/null}:/opt/graviteeio-integration-agent/config/key/key.json
    environment:
      - gravitee_integration_connector_ws_endpoints_0=${WS_ENDPOINTS}
      - gravitee_integration_connector_ws_headers_0_name=Authorization
      - gravitee_integration_connector_ws_headers_0_value=bearer ${WS_AUTH_TOKEN}
      - gravitee_integration_providers_0_integrationId=${INTEGRATION_ID}
      - gravitee_integration_providers_0_configuration_gcpProjectId=${GCP_PROJECT_ID}
      - gravitee_integration_providers_0_configuration_developerEmail=${APIGEE_DEV_EMAIL}
      - gravitee_integration_providers_0_configuration_developerFirstName=${APIGEE_DEV_FIRST_NAME}
      - gravitee_integration_providers_0_configuration_developerLastName=${APIGEE_DEV_LAST_NAME}
      - gravitee_integration_providers_0_configuration_developerUsername=${APIGEE_DEV_USERNAME}
      - gravitee_integration_providers_0_configuration_serviceAccountKeyInline=${SERVICE_ACCOUNT_KEY_INLINE}
      - gravitee_integration_providers_0_type=apigee
```

This Docker Compose file proposes both ways of passing the service account key (either inline or from a file), but you'll need to make sure to only set one of the associated variables in the **.env** file.

Next, create a file named `.env` in the same directory. We'll use it to set the required Docker Compose variables. Fill the values in this file from those you obtained in [step 2](apigee-x.md#id-2.-configure-the-apigee-x-federation-agent).

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

## APIGEE X PARAMETERS ##

# Google Cloud project ID
GCP_PROJECT_ID=[your-project-id]

# Apigee developer information
# This Apigee developer will be the owner of applications
# created by Gravitee in Apigee for managing subscriptions
# Gravitee will reuse a matching account, or create it 
# if it doesn't exist. 
# The provided email may receive notifications from Apigee
APIGEE_DEV_EMAIL=[your-dev-email]
APIGEE_DEV_FIRST_NAME=[your-dev-firstname]
APIGEE_DEV_LAST_NAME=[your-dev-lastname]
APIGEE_DEV_USERNAME=[your-dev-username]

# Service account key - select either PATH or INLINE
# SERVICE_ACCOUNT_KEY_PATH=[service-account-key-path]
SERVICE_ACCOUNT_KEY_INLINE='{
  "type": "service_account",
  "project_id": "1234",
  "private_key_id": "1234",
  "private_key": "-----BEGIN PRIVATE KEY-----\n1234==\n-----END PRIVATE KEY-----\n",
  "client_email": "abcd",
  "client_id": "1234",
  "auth_uri": "https://accounts.google.com/o/oauth2/auth",
  "token_uri": "https://oauth2.googleapis.com/token",
  "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
  "client_x509_cert_url": "abcd",
  "universe_domain": "googleapis.com"
}'
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

<figure><img src="../../../../../.gitbook/assets/Screenshot 2024-10-09 at 17.41.58.png" alt=""><figcaption></figcaption></figure>

If your **Agent Connection** still shows as `Disconnected`, then please inspect the agent's container logs. There you should find error logs that will help you troubleshoot.

## Minimum Apigee permissions required by the agent

Below is the list of minimum required permissions that have to be attached to the role used by the GCP Service Account:

* apigee.apiproducts.list
* apigee.appkeys.create
* apigee.appkeys.delete
* apigee.appkeys.get
* apigee.appkeys.manage
* apigee.apps.get
* apigee.developerapps.create
* apigee.developerapps.delete
* apigee.developerapps.get
* apigee.developers.create
* apigee.developers.get
* apigee.proxies.list
* apigee.proxyrevisions.get
