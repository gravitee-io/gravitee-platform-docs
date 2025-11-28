---
description: An overview about ibm api connect.
---

# IBM API Connect

## Overview

IBM API Connect is IBM's API management solution. The agent works with both Cloud and on-premise versions of IBM API Connect (APIC).

## Prerequisites

Before you install the IBM API Connect federation agent, complete the following steps:

* Access to an IBM API Connect account: Cloud or on-premise, version 10.0.5.
* Verify you have Gravitee API Management version 4.5 or later, with an enterprise license. For more information about Enterprise edition, see[ Enterprise Edition Licensing.](https://documentation.gravitee.io/platform-overview/gravitee-platform/gravitee-offerings-ce-vs-ee/enterprise-edition-licensing#license-support)
* Create an access token. For more information, [see how to create a service account and an access token.](../federation-agent-service-account.md)
* Obtain your IBM API Connect platform URL, and your IBM API Connect organization name.
* Obtain your IBM API Connect credentials: Client ID, Client Secret, and API Key. The requirements vary by instance type. For more information about the credentials required for your instance type, [see defining connection credentials](https://www.ibm.com/docs/fi/explorer-for-zos/3.2.0?topic=connections-defining-connection-credentials)

{% hint style="info" %}
For more information, see IBM API connect documentation based on the versions you are using: [10.0.5](https://www.ibm.com/docs/en/api-connect/10.0.5.x_lts?topic=applications-managing-platform-rest-api-keys) / [10.0.8](https://www.ibm.com/docs/en/api-connect/10.0.8?topic=applications-managing-platform-rest-api-keys) / [SaaS](https://www.ibm.com/docs/en/api-connect/saas?topic=applications-managing-platform-rest-api-keys).
{% endhint %}

## Integrate IBM API Connect with Gravitee APIM

To integrate IBM API Connect with Gravitee APIM, complete the following steps:

1. [#create-an-ibm-api-connect-integration-in-the-gravitee-apim-console](ibm-api-connect.md#create-an-ibm-api-connect-integration-in-the-gravitee-apim-console "mention")
2. [#run-the-ibm-api-connect-federation-agent](ibm-api-connect.md#run-the-ibm-api-connect-federation-agent "mention")

### Create an IBM API Connect integration in the Gravitee APIM Console

1.  From the Dashboard, click **Integrations**.<br>

    <figure><img src="../../../.gitbook/assets/image (56) (1).png" alt=""><figcaption></figcaption></figure>
2.  Click **Create Integration**.

    <figure><img src="../../../.gitbook/assets/image (57) (1).png" alt=""><figcaption></figcaption></figure>
3.  Select **IBM API Connect**, and then click **Next**.<br>

    <figure><img src="../../../.gitbook/assets/click-next-on-integrations-workflow (1).png" alt=""><figcaption></figcaption></figure>
4.  Type the **Integration Name**.<br>

    <figure><img src="../../../.gitbook/assets/ibm-connect-name-and-description.png" alt=""><figcaption></figcaption></figure>
5.  (Optional) Type the **Description** for the integration.<br>

    <figure><img src="../../../.gitbook/assets/ibm-connect-name-and-description (1).png" alt=""><figcaption></figcaption></figure>
6.  Click **Create Integration**.

    <figure><img src="../../../.gitbook/assets/create-integration-ibm-connect.png" alt=""><figcaption></figcaption></figure>
7.  From the Integration overview tab, copy the **Integration ID**. You need this ID for the agent configuration.<br>

    <figure><img src="../../../.gitbook/assets/ibm-connect-integraiton-id (1).png" alt=""><figcaption></figcaption></figure>

### Run the IBM API Connect federation agent

You can deploy the IBM API Connect federation agent using either of the following installation methods:

* [#docker-compose](ibm-api-connect.md#docker-compose "mention")
* [#helm](ibm-api-connect.md#helm "mention")

### Docker Compose

1.  Copy the following configuration, and then save it to your Docker Compose file:

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
          # If you are using Gravitee NextGen Cloud, then you need to also include a Cloud Token for Federation Agent
          # - gravitee_cloud_token=${GRAVITEE_CLOUD_TOKEN}
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
2. Create a file named `.env` in the same directory as your Docker Compose file. The configuration varies by IBM instance type:

* [#ibm-cloud-or-self-hosted-instances](ibm-api-connect.md#ibm-cloud-or-self-hosted-instances "mention")
* [#ibm-cloud-reserved-instance](ibm-api-connect.md#ibm-cloud-reserved-instance "mention")
* [#optional-configure-catalog-filtering](ibm-api-connect.md#optional-configure-catalog-filtering "mention")

{% hint style="info" %}
The following configuration varies based on your **IBM API Connect** instance type not your Gravitee hosting type. Choose the appropriate section for your IBM instance.
{% endhint %}

#### **IBM Cloud or Self-hosted instances**

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
# AGENT_VERSION=1.3.0

## IBM API CONNECT PARAMETERS ##

# IBM Platform API URL
PLATFORM_API_URL=[your-platform-api-url]

# IBM organization name
ORGANIZATION_NAME=[your-organization-name]

# IBM Instance Type
# Use "cloud" for IBM Cloud instances
# Use "self-hosted" for IBM self-hosted instances
IBM_INSTANCE_TYPE=cloud

# IBM credentials (required for Cloud and Self-hosted)
CLIENT_ID=[your-client-id]
CLIENT_SECRET=[your-client-secret]
API_KEY=[your-api-key]
```

#### IBM Cloud Reserved instance

{% hint style="info" %}
Cloud reserved instances require only an API key. Do not include Client ID or Client Secret.
{% endhint %}

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
# AGENT_VERSION=1.3.0

## IBM API CONNECT PARAMETERS ##

# IBM Platform API URL
PLATFORM_API_URL=[your-platform-api-url]

# IBM organization name
ORGANIZATION_NAME=[your-organization-name]

# IBM Instance Type
IBM_INSTANCE_TYPE=cloud-reserved-instance

# IBM credentials (API key only for Cloud Reserved)
API_KEY=[your-api-key]
```

3. Replace the following placeholder values with your own configuration:
   * `[your-APIM-management-API-host]`: Your Gravitee APIM management API URL.
   * `[your-token]`: Your Gravitee APIM access token.
   * `[your-integration-id]`: The Integration ID from the Gravitee Console.
   * `[organization-id]`: Your APIM organization ID. For example: DEFAULT
   * `[your-platform-api-url]`: Your IBM API Connect platform URL.
   * `[your-organization-name]`: Your IBM API Connect organization name.
   * `[your-client-id]`: Your IBM client ID (required for Cloud and Self-hosted instances only).
   * `[your-client-secret]`: Your IBM client secret (required for Cloud and Self-hosted instances only).
   * `[your-api-key]`: Your IBM API key
4.  Pull the latest Docker image using the following command:

    ```bash
    docker compose pull
    ```
5.  Start the agent in the background with the following command:

    ```bash
    docker compose up -d
    ```

#### (Optional) Configure catalog filtering

1.  To filter specific catalogs, add catalog configurations to your `docker-compose.yaml`:

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
2.  Create your `.env` file and then add the following catalog parameters to your `.env` file:

    ```bash
    # Optional catalog filtering
    IBM_0_CATALOG=[your-first-catalog]
    IBM_1_CATALOG=[your-second-catalog]
    ```

### Verification

1.  In the Gravitee API Management console, after refreshing, you should now see the agent's status set to **Connected**.

    <figure><img src="../../../.gitbook/assets/ibm-connect-integraiton-id.png" alt=""><figcaption></figcaption></figure>
2. (Optional) If the Agent Connection shows as **Disconnected**, inspect the agent container logs for error messages.

### Helm

To deploy the federation agent to your Kubernetes cluster, complete the following steps:

#### Update your Helm Chart

Add the Gravitee Helm repository and update it to ensure you have access to the latest charts:

```bash
helm repo add gravitee https://helm.gravitee.io

helm repo update
```

#### Configure the Federation Agent Helm values

Create the Helm values file based on your APIM management API's certificate setup and IBM instance type. You can use the standard configuration or custom certificate configuration.

* [#default-configuration-cloud-and-self-hosted-instances](ibm-api-connect.md#default-configuration-cloud-and-self-hosted-instances "mention")
* [#default-configuration-cloud-reserved-instance](ibm-api-connect.md#default-configuration-cloud-reserved-instance "mention")
* [#custom-certificate-configuration](ibm-api-connect.md#custom-certificate-configuration "mention")

#### Default configuration: cloud and self-hosted instances

1.  This configuration uses the default Java truststore for your APIM management API certificates. Create a file named `federation-agent-ibm-values.yaml` in your working directory, and then copy the following configuration:

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
          name: federation-agent-ibm-api-connect
          tag: 4.8.4

        resources:
          requests:
            memory: "256Mi"
            cpu: "100m"
          limits:
            memory: "512Mi"
            cpu: "250m"

    # =========================
    # Gravitee / IBM Agent
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
            - type: ibm-api-connect
              integrationId: [your-integration-id]
              configuration:
                apiKey: [your-api-key]
                clientId: [your-client-id]
                clientSecret: [your-client-secret]
                ibmInstanceType: cloud
                organizationName: [your-organization-name]
                platformApiUrl: [your-platform-api-url]
    ```
2. Make the following modifications to your `federation-agent-ibm-values.yaml` file:
   * Replace `[your-cloud-token]` with your Gravitee Cloud token or remove the entire `cloud:` section if using self-hosted APIM.
   * Replace `[your-APIM-management-API-host]` with your APIM management API URL. For example, `apim.example.com` or `gravitee-apim-api.gravitee-apim.svc.cluster.local:8083` for internal Kubernetes service.
   * Replace `[your-token]` with your service account bearer token.
   * Replace `[your-integration-id]` with the Integration ID.
   * Replace `[your-api-key]` with your IBM API key.
   * Replace `[your-client-id]` with your IBM client ID.
   * Replace `[your-client-secret]` with your IBM client secret.
   * Replace `[your-organization-name]` with your IBM API Connect organization name.
   * Replace `[your-platform-api-url]` with your IBM API Connect platform URL.
   * For self-hosted instances, change `ibmInstanceType: cloud` to `ibmInstanceType: self-hosted`.
3.  Deploy the federation agent to your Kubernetes cluster by running the following command:

    ```bash
    helm install federation-agent-ibm \
      gravitee/federation-agent \
      -f federation-agent-ibm-values.yaml \
      -n gravitee-apim \
      --create-namespace
    ```

#### Default configuration: Cloud reserved instance

1.  For Cloud reserved instances, use the following configuration:

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
          name: federation-agent-ibm-api-connect
          tag: 4.8.4

        resources:
          requests:
            memory: "256Mi"
            cpu: "100m"
          limits:
            memory: "512Mi"
            cpu: "250m"

    # =========================
    # Gravitee / IBM Agent
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
            - type: ibm-api-connect
              integrationId: [your-integration-id]
              configuration:
                apiKey: [your-api-key]
                ibmInstanceType: cloud-reserved-instance
                organizationName: [your-organization-name]
                platformApiUrl: [your-platform-api-url]
    ```
2. Make the following modifications to your `federation-agent-ibm-values.yaml` file:
   * Replace `[your-cloud-token]` with your Gravitee Cloud token or remove the entire `cloud:` section if using self-hosted APIM.
   * Replace `[your-APIM-management-API-host]` with your APIM management API URL. For example, `apim.example.com` or `gravitee-apim-api.gravitee-apim.svc.cluster.local:8083` for internal Kubernetes service.
   * Replace `[your-token]` with your service account bearer token.
   * Replace `[your-integration-id]` with the Integration ID.
   * Replace `[your-api-key]` with your IBM API key.
   * Replace `[your-organization-name]` with your IBM API Connect organization name.
   * Replace `[your-platform-api-url]` with your IBM API Connect platform URL
3.  Deploy the federation agent to your Kubernetes cluster by running the following command:

    ```bash
    helm install federation-agent-ibm \
      gravitee/federation-agent \
      -f federation-agent-ibm-values.yaml \
      -n gravitee-apim \
      --create-namespace
    ```

#### **Custom certificate configuration**

1.  This configuration includes custom truststore volume mounts for certificates from private certificate authorities or self-signed certificates. Create a file named `federation-agent-ibm-values.yaml`, and then copy the following configuration:

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
            secretName: ibm-truststore

      deployment:
        image:
          repository: graviteeio
          name: federation-agent-ibm-api-connect
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
    # Gravitee / IBM Agent
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
                  password: secret://kubernetes/ibm-truststore:password?namespace=gravitee-apim
          
          providers:
            - type: ibm-api-connect
              integrationId: [your-integration-id]
              configuration:
                apiKey: [your-api-key]
                clientId: [your-client-id]
                clientSecret: [your-client-secret]
                ibmInstanceType: cloud
                organizationName: [your-organization-name]
                platformApiUrl: [your-platform-api-url]
    ```

{% hint style="info" %}
(optional) If your APIM management API uses certificates that require a custom truststore, you must create the truststore and add it to Kubernetes as a secret before deploying the agent.
{% endhint %}

2. Make the following modifications to your `federation-agent-ibm-values.yaml` file:
   * Replace `[your-cloud-token]` with your Gravitee Cloud token or remove the entire `cloud:` section if using self-hosted APIM.
   * Replace `[your-APIM-management-API-host]` with your APIM management API URL. For example, `apim.example.com` or `gravitee-apim-api.gravitee-apim.svc.cluster.local:8083` for internal Kubernetes service.
   * Replace `[your-token]` with your service account bearer token.
   * Replace `[your-integration-id]` with the Integration ID.
   * Replace `[your-api-key]` with your IBM API key.
   * Replace `[your-client-id]` with your IBM client ID (omit for cloud-reserved-instance).
   * Replace `[your-client-secret]` with your IBM client secret (omit for cloud-reserved-instance).
   * Replace `[your-organization-name]` with your IBM API Connect organization name.
   * Replace `[your-platform-api-url]` with your IBM API Connect platform URL.
   * For self-hosted instances, change `ibmInstanceType: cloud` to `ibmInstanceType: self-hosted`.
   * For cloud reserved instances, change `ibmInstanceType: cloud` to `ibmInstanceType: cloud-reserved-instance` and remove `clientId` and `clientSecret` fields.
3.  Deploy the federation agent to your Kubernetes cluster by running the following command:

    ```bash
    helm install federation-agent-ibm \
      gravitee/federation-agent \
      -f federation-agent-ibm-values.yaml \
      -n gravitee-apim \
      --create-namespace
    ```

### Verification

1.  When the deployment is successful, verify the installation is running using the following command:

    ```bash
    kubectl get pods -n gravitee-apim -l app.kubernetes.io/name=federation-agent
    ```

    \
    The output should show the federation agent ready and running:

    ```bash
    NAME                                    READY   STATUS    RESTARTS   AGE
    federation-agent-ibm-xxxxx-yyyyy        1/1     Running   0          30s
    ```
2.  Return to the Gravitee API Management console, refresh the page, and verify that the agent's status is set to **Connected**.

    <figure><img src="../../../.gitbook/assets/image (72).png" alt=""><figcaption></figcaption></figure>

## Limitations

The agent limits the size of the OpenAPI document to 1 000 000B (about 1MB). APIs with documentation in excess of this limit are ingested without documentation and generate a message in the agent logs:

{% code overflow="wrap" %}
```sh
The length of the API: ${apiId}/${ApiName} OAS document is too large ${sizeB} (${sizeHumanReadable}). The limit is {sizeB} (${sizeHumanReadable}). The document will not be ingested.
```
{% endcode %}
