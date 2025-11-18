# Apigee X

## Overview

Apigee X is Google Cloud Platform's predominant API management solution.

## Prerequisites

Before you install the Apigee X federation agent, complete the following steps:

* Access to an Apigee X account that includes features such as Apigee API products.
* The account needs a minimum set of permissions for the federation agent. See [#minimum-apigee-permissions-required-by-the-agent](apigee-x.md#minimum-apigee-permissions-required-by-the-agent "mention") for the complete list.
* Gravitee API Management version 4.4 or later, with an enterprise license. For more information about Enterprise edition, see [Enterprise Edition Licensing](https://documentation.gravitee.io/platform-overview/gravitee-platform/gravitee-offerings-ce-vs-ee/enterprise-edition-licensing#license-support).
* An access token. For more information, see [how to create a service account and an access token](../federation-agent-service-account.md).
* A Google Cloud Platform project ID
* Google Cloud Platform service account with a service account key in JSON format. For more information, see [How to create a GCP Service Account.](https://cloud.google.com/iam/docs/service-accounts-create)

## Integrate Apigee x with Grvaitee APIM

To integrate Apigee X with Gravitee APIM, complete the following steps:

1. [#create-an-apigee-x-integration-in-the-gravitee-apim-console](apigee-x.md#create-an-apigee-x-integration-in-the-gravitee-apim-console "mention")
2. [#configure-the-apigee-x-federation-agent](apigee-x.md#configure-the-apigee-x-federation-agent "mention")
3. [#run-the-apigee-x-federation-agent](apigee-x.md#run-the-apigee-x-federation-agent "mention")

### Create an Apigee X integration in the Gravitee APIM Console

1.  From the Dashboard, click **Integrations**

    <figure><img src="../../../.gitbook/assets/select-integrations-left-menu-apigee.png" alt=""><figcaption></figcaption></figure>
2.  Click **Create Integration.**&#x20;

    <figure><img src="../../../.gitbook/assets/create-integration-apigee.png" alt=""><figcaption></figcaption></figure>
3.  Select **Apigee X,** and then click **Next**\


    <figure><img src="../../../.gitbook/assets/select-apigee-integration-from-integrations.png" alt=""><figcaption></figcaption></figure>
4.  Enter the **Integration** **Name**

    <figure><img src="../../../.gitbook/assets/image (15).png" alt=""><figcaption></figcaption></figure>
5.  (Optional) Enter a **Description** for the integration.

    <figure><img src="../../../.gitbook/assets/name-and-description-apigee-x.png" alt=""><figcaption></figcaption></figure>
6.  Click **Create Integration.**

    <figure><img src="../../../.gitbook/assets/click-on-create-integration.png" alt=""><figcaption></figcaption></figure>
7.  From the Integration overview tab, copy the **Integration ID**. You need this ID for the agent configuration.

    <figure><img src="../../../.gitbook/assets/apigee-federation-agent-connection.png" alt=""><figcaption></figcaption></figure>

### Run the Apigee X federation Agent

You can deploy the Apigee X federation agent using either of the following installation methods:

* [#docker-compose](apigee-x.md#docker-compose "mention")
* [#helm](apigee-x.md#helm "mention")

### Docker Compose&#x20;

{% hint style="warning" %}
You can only choose one authentication method. Providing two authentication methods in one configuration results in an error.
{% endhint %}

There are two ways to pass the service account key as a parameter in Docker Compose.

1. Referencing the service account key file on your filesystem by providing a path.
2. Passing the service account key inline.

With the first option, you must include a `SERVICE_ACCOUNT_KEY_PATH` variable in your `docker-compose` configuration.

For the inline method, you need to provide the full content of your Service Account Key and paste it directly into your Docker Compose file. **The key must be put in between apostrophes (`'content'`).** For this option, you must use the `SERVICE_ACCOUNT_KEY_INLINE`parameter name with your Docker Compose file.

{% hint style="warning" %}
This Docker Compose file supports passing the service account key either inline or from a file. However, you must ensure that only one of the associated variables in the `.env` file is set.
{% endhint %}

1.  Copy the following configuration, and then save it to your Docker Compose file:

    ```yaml
    services:
      integration-agent:
        image: graviteeio/federation-agent-apigee:${AGENT_VERSION:-latest}
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
          # If you are using Gravitee NextGen Cloud, then you need to also include a Cloud Token for Federation Agent
          # - gravitee_cloud_token=${GRAVITEE_CLOUD_TOKEN}
    ```
2.  Create a file named `.env` in the same directory as your Docker Compose file, and then add the following environment variables:

    ```dotenv
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
      "project_id": "your-prject-id",
      "private_key_id": "your-private-key-id",
      "private_key": "-----BEGIN PRIVATE KEY-----\n1234==\n-----END PRIVATE KEY-----\n",
      "client_email": "abcd",
      "client_id": "your-client-id",
      "auth_uri": "https://accounts.google.com/o/oauth2/auth",
      "token_uri": "https://oauth2.googleapis.com/token",
      "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
      "client_x509_cert_url": "abcd",
      "universe_domain": "googleapis.com"
    }'
    ```
3. Replace the following placeholder values with your own configuration:
   * `[your-APIM-management-API-host]`: Your Gravitee APIM management API URL.
   * `[your-token]`: Your Gravitee APIM access token.
   * `[your-integration-id]`: The Integration ID from the Gravitee Console.
   * `[organization-id]`: (for example, DEFAULT) Your APIM organization ID.&#x20;
   * `[your-project-id]`: Your Google Cloud Platform project ID.
   * `[your-dev-email]`: Developer email for the Apigee developer account.
   * `[your-dev-firstname]`: Developer's first name.
   * `[your-dev-lastname]`: Developer's last name.
   * `[your-dev-username]`: Developer username.
4.  Pull the latest Docker image using the following command:

    ```shellscript
    docker compose pull
    ```
5.  Start the agent in the background with the following command:

    ```shellscript
    docker compose up -d
    ```

#### Verification&#x20;

1. In the Gravitee API Management console, after refreshing, you should now see the agent's status set to `Connected:`

<figure><img src="../../../.gitbook/assets/connected.png" alt=""><figcaption></figcaption></figure>

2. If the Agent Connection shows as `Disconnected`, inspect the agent container logs for error messages.

### Helm&#x20;

To deploy the federation agent to your Kubernetes cluster, complete the following steps:

#### Update your Helm Chart

Add the Gravitee Helm repository and update it to ensure you have access to the latest charts:

```shellscript
helm repo add gravitee https://helm.gravitee.io

helm repo update
```

#### Configure the Federation Agent Helm values

Create the Helm values file based on your APIM management API's certificate setup. You can use the standard configuration or custom certificate configuration.

* [#standard-configuration](apigee-x.md#standard-configuration "mention")
* [#custom-certificate-configuration](apigee-x.md#custom-certificate-configuration "mention")

#### **Standard configuration**&#x20;

1.  This configuration uses the default Java truststore for your APIM management API certificates. Create a file named `federation-agent-apigee-values.yaml` in your working directory, and then copy the following configuration:

    ```yaml
    # =========================
    # Kubernetes / RBAC
    # =========================
    kubernetes:
      serviceAccount:
        managed: true
        roleRules:
          - apiGroups:
              - ""
            resources:
              - configmaps
              - secrets
            verbs:
              - get
              - list
              - watch

      deployment:
        image:
          repository: graviteeio
          name: federation-agent-apigee
          tag: 4.8.4

        resources:
          requests:
            memory: "256Mi"
            cpu: "100m"
          limits:
            memory: "512Mi"
            cpu: "250m"

    # =========================
    # Gravitee / Apigee Agent
    # =========================
    config:
      graviteeYml:
        services:
          core:
            http:
              enabled: true
              port: 18084
              host: 0.0.0.0
              authentication:
                type: basic
                users:
                  admin: adminadmin
          metrics:
            enabled: false
            prometheus:
              enabled: false
        
        # Optional: Only if using Gravitee Cloud
        cloud:
          token: [your-cloud-token]
        
        integration:
          connector:
            ws:
              endpoints:
                - https://[your-APIM-management-API-host]/integration-controller
              headers:
                - name: Authorization
                  value: bearer [your-token]
          
          providers:
            - type: apigee
              integrationId: [your-integration-id]
              configuration:
                gcpProjectId: [your-project-id]
                developerEmail: [your-dev-email]
                developerFirstName: [your-dev-firstname]
                developerLastName: [your-dev-lastname]
                developerUsername: [your-dev-username]
                serviceAccountKeyInline: |
                  {
                    "type": "service_account",
                    "project_id": "your-project-id",
                    "private_key_id": "your-private-key-id",
                    "private_key": "-----BEGIN PRIVATE KEY-----\nYOUR-KEY-HERE\n-----END PRIVATE KEY-----\n",
                    "client_email": "your-sa@project.iam.gserviceaccount.com",
                    "client_id": "your-client-id",
                    "auth_uri": "https://accounts.google.com/o/oauth2/auth",
                    "token_uri": "https://oauth2.googleapis.com/token",
                    "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
                    "client_x509_cert_url": "https://www.googleapis.com/robot/v1/metadata/x509/your-sa%40project.iam.gserviceaccount.com",
                    "universe_domain": "googleapis.com"
                  }
    ```
2. Make the following modifications to your `federation-agent-apigee-values.yaml` file:&#x20;
   * Replace `[your-cloud-token]` with your Gravitee Cloud token or remove the entire `cloud:` section if using self-hosted APIM.
   * Replace `[your-APIM-management-API-host]` with your APIM management API URL. For example, `apim.example.com` or `gravitee-apim-api.gravitee-apim.svc.cluster.local:8083` for internal Kubernetes service.
   * Replace `[your-token]` with your service account bearer token from the [#prerequisites](apigee-x.md#prerequisites "mention")  section.
   * Replace `[your-integration-id]` with the Integration ID.&#x20;
   * Replace `[your-project-id]` with your GCP Project ID.&#x20;
   * Replace `[your-dev-email]` with the developer email for the Apigee developer account. For example: `gravitee-integration@yourcompany.com`
   * Replace `[your-dev-firstname]` with the developer's first name for the Apigee developer account. For example:`Gravitee`
   * Replace `[your-dev-lastname]` with the developer's last name for the Apigee developer account. For example, `Integration`
   * Replace `[your-dev-username]` with the developer username for the Apigee developer account. For example:, `gravitee-integration`.
   * Replace the Service Account Key JSON placeholder with your complete GCP service account key.&#x20;
3.  Deploy the federation agent to your Kubernetes cluster by running the following command:

    ```shellscript
    helm install federation-agent-apigee \
      gravitee/federation-agent \
      -f federation-agent-apigee-values.yaml \
      -n gravitee-apim \
      --create-namespace
    ```

#### **Custom certificate configuration**

1.  This configuration includes custom truststore volume mounts for certificates from private certificate authorities or self-signed certificates. Create a file named `federation-agent-apigee-values.yaml`, and then copy the following configuration:

    ```yaml
    # =========================
    # Kubernetes / RBAC
    # =========================
    kubernetes:
      serviceAccount:
        managed: true
        roleRules:
          - apiGroups:
              - ""
            resources:
              - configmaps
              - secrets
            verbs:
              - get
              - list
              - watch
      
      extraVolumes: |
        - name: custom-truststore
          secret:
            secretName: apigee-truststore

      deployment:
        image:
          repository: graviteeio
          name: federation-agent-apigee
          tag: 4.8.4
        
        extraVolumeMounts: |
          - name: custom-truststore
            mountPath: /opt/graviteeio-federation-agent/truststore
            readOnly: true

        resources:
          requests:
            memory: "256Mi"
            cpu: "100m"
          limits:
            memory: "512Mi"
            cpu: "250m"

    # =========================
    # Gravitee / Apigee Agent
    # =========================
    config:
      graviteeYml:
        services:
          core:
            http:
              enabled: true
              port: 18084
              host: 0.0.0.0
              authentication:
                type: basic
                users:
                  admin: adminadmin
          metrics:
            enabled: false
            prometheus:
              enabled: false
        
        # Optional: Only if using Gravitee Cloud
        cloud:
          token: [your-cloud-token]
        
        integration:
          connector:
            ws:
              endpoints:
                - https://[your-APIM-management-API-host]/integration-controller
              headers:
                - name: Authorization
                  value: bearer [your-token]
              ssl:
                truststore:
                  # Type can be: JKS, PKCS12, or PEM
                  type: PKCS12
                  path: /opt/graviteeio-federation-agent/truststore/my_truststore.p12
                  password: secret://kubernetes/apigee-truststore:password?namespace=gravitee-apim
          
          providers:
            - type: apigee
              integrationId: [your-integration-id]
              configuration:
                gcpProjectId: [your-project-id]
                developerEmail: [your-dev-email]
                developerFirstName: [your-dev-firstname]
                developerLastName: [your-dev-lastname]
                developerUsername: [your-dev-username]
                serviceAccountKeyInline: |
                  {
                    "type": "service_account",
                    "project_id": "your-project-id",
                    "private_key_id": "your-private-key-id",
                    "private_key": "-----BEGIN PRIVATE KEY-----\nYOUR-KEY-HERE\n-----END PRIVATE KEY-----\n",
                    "client_email": "your-sa@project.iam.gserviceaccount.com",
                    "client_id": "your-client-id",
                    "auth_uri": "https://accounts.google.com/o/oauth2/auth",
                    "token_uri": "https://oauth2.googleapis.com/token",
                    "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
                    "client_x509_cert_url": "https://www.googleapis.com/robot/v1/metadata/x509/your-sa%40project.iam.gserviceaccount.com",
                    "universe_domain": "googleapis.com"
                  }
    ```

{% hint style="info" %}
If your APIM management API uses certificates that require a custom truststore, you must create the truststore and add it to Kubernetes as a secret before deploying the agent.&#x20;
{% endhint %}

2. Make the following modifications to your `federation-agent-apigee-values.yaml` file:&#x20;

* Replace `[your-cloud-token]` with your Gravitee Cloud token or remove the entire `cloud:` section if using self-hosted APIM.
* Replace `[your-APIM-management-API-host]` with your APIM management API URL. For example, `apim.example.com` or `gravitee-apim-api.gravitee-apim.svc.cluster.local:8083` for internal Kubernetes service.
* Replace `[your-token]` with your service account bearer token from the [#prerequisites](apigee-x.md#prerequisites "mention")  section.
* Replace `[your-integration-id]` with the Integration ID.&#x20;
* Replace `[your-project-id]` with your GCP Project ID.&#x20;
* Replace `[your-dev-email]` with the developer email for the Apigee developer account. For example: `gravitee-integration@yourcompany.com`
* Replace `[your-dev-firstname]` with the developer's first name for the Apigee developer account. For example:`Gravitee`
* Replace `[your-dev-lastname]` with the developer's last name for the Apigee developer account. For example, `Integration`
* Replace `[your-dev-username]` with the developer username for the Apigee developer account. For example:, `gravitee-integration`.
* Replace the Service Account Key JSON placeholder with your complete GCP service account key.&#x20;

3.  Deploy the federation agent to your Kubernetes cluster by running the following command:

    ```shellscript
    helm install federation-agent-apigee \
      gravitee/federation-agent \
      -f federation-agent-apigee-values.yaml \
      -n gravitee-apim \
      --create-namespace
    ```

### Verification&#x20;

1.  When the deployment is successful, verify the installation is running using the following command:

    ```shellscript
    kubectl get pods -n gravitee-apim -l app.kubernetes.io/name=federation-agent
    ```

    \
    The output should show the federation agent ready and running:

    ```shellscript
    NAME                                      READY     STATUS    RESTARTS    AGE
    federation-agent-apigee-xxxxx-yyyyy        1/1     Running    0          30s
    ```
2.  Return to the Gravitee API Management console, refresh the page, and verify that the agent's status is set to Connected:

    <figure><img src="../../../.gitbook/assets/image (32).png" alt=""><figcaption></figcaption></figure>

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
