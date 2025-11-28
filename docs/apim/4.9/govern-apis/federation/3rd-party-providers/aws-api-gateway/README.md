---
description: An overview about aws api gateway.
---

# AWS API Gateway

## Overview

AWS API Gateway is AWS's built-in API management solution and is used to expose services running in the AWS cloud to the public internet.

## Prerequisites

Before you install the AWS API Gateway federation agent, complete the following steps:

* An AWS account with permissions to access the AWS API Gateway console.
* AWS authentication credentials: access key and secret, or IAM `role/instanceRole-based` authentication.
* The account needs a minimum set of permissions for the federation agent. See [#minimum-aws-permissions-required-by-the-agent](./#minimum-aws-permissions-required-by-the-agent "mention") for the complete list.
* Gravitee API Management version 4.4 or later, with an enterprise license. For more information about Enterprise edition, see [Enterprise Edition Licensing.](https://documentation.gravitee.io/platform-overview/gravitee-platform/gravitee-offerings-ce-vs-ee/enterprise-edition-licensing#license-support)
* A Federation agent service account. For more information,[ see how to create a service account and an access token.](../../federation-agent-service-account.md)

## Integrate AWS API Gateway with Gravitee APIM

To integrate AWS API Gateway with Gravitee APIM, complete the following steps:

1. [#create-an-aws-api-management-integration-in-the-gravitee-apim-console](./#create-an-aws-api-management-integration-in-the-gravitee-apim-console "mention")
2. [#run-the-aws-api-gateway-federation-agent](./#run-the-aws-api-gateway-federation-agent "mention")

### Create an AWS API Management integration in the Gravitee APIM Console

1.  From the Dashboard, click **Integrations.**<br>

    <figure><img src="../../../../.gitbook/assets/image (56).png" alt=""><figcaption></figcaption></figure>
2.  Click **Create Integration.**<br>

    <figure><img src="../../../../.gitbook/assets/image (57).png" alt=""><figcaption></figcaption></figure>
3.  Select **AWS API Gateway**, and then click **Next.**

    <figure><img src="../../../../.gitbook/assets/select-aws-api-gateway.png" alt=""><figcaption></figcaption></figure>
4.  Type the **Integration Name.**

    <figure><img src="../../../../.gitbook/assets/enter-the-aws-api-integration-name.png" alt=""><figcaption></figcaption></figure>
5.  (Optional) Type a **Description** for the integration.

    <figure><img src="../../../../.gitbook/assets/image (58).png" alt=""><figcaption></figcaption></figure>
6.  Click **Create Integration.**

    <figure><img src="../../../../.gitbook/assets/click-create-integration-for-aws-api-gateway.png" alt=""><figcaption></figcaption></figure>
7.  From the Integration overview tab, copy the **Integration ID**. You need this ID for the agent configuration.

    <figure><img src="../../../../.gitbook/assets/aws-api-gateway-integration.png" alt=""><figcaption></figcaption></figure>

### Run the AWS API Gateway Federation Agent

You can deploy the AWS API Gateway federation agent using either of the following installation methods:

* [#docker-compose](./#docker-compose "mention")
* [#helm](./#helm "mention")

### Docker Compose

1.  Copy the following configuration, and then save it to your Docker Compose file:

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
          - gravitee_integration_providers_0_configuration_accessKeyId=${AWS_ACCESS_KEY_ID}
          - gravitee_integration_providers_0_configuration_secretAccessKey=${AWS_SECRET_ACCESS_KEY}
          - gravitee_integration_providers_0_configuration_region=${AWS_REGION}
          - gravitee_integration_providers_0_configuration_acceptApiWithoutUsagePlan=${ACCEPT_API_WITHOUT_USAGE_PLAN:-false}
          # If you are using Gravitee NextGen Cloud, then you need to also include a Cloud Token for Federation Agent
          # - gravitee_cloud_token=${GRAVITEE_CLOUD_TOKEN}
    ```
2.  Create a file named `.env` in the same directory as your Docker Compose file, and then add the following environment variables:

    ```shellscript
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

    ## AWS API GATEWAY PARAMETERS ##

    # AWS Region, example: us-west-2
    AWS_REGION=[your-aws-region]

    # AWS Credentials
    # Optional if you're using IAM Role-based authentication
    AWS_ACCESS_KEY_ID=[your-key-id]
    AWS_SECRET_ACCESS_KEY=[your-access-key]

    # Discover APIs without usage plan (default: false)
    # ACCEPT_API_WITHOUT_USAGE_PLAN=true
    ```
3. Replace the following placeholder values with your own configuration:
   * `[your-APIM-management-API-host]`: Your Gravitee APIM management API URL.
   * `[your-token]`: Your Gravitee APIM access token.
   * `[your-integration-id]`: The Integration ID from the Gravitee Console.
   * `[organization-id]`: (for example, DEFAULT) Your APIM organization ID.
   * `[your-aws-region]`: Your AWS region. For example, us-west-2.
   * `[your-key-id]`: Your AWS access key ID.
   * `[your-access-key]`: Your AWS secret access key.
4.  Pull the latest Docker image using the following command:

    ```bash
    docker compose pull
    ```
5.  Start the agent in the background with the following command:

    ```bash
    docker compose up -d
    ```

#### Verification

1.  In the Gravitee API Management console, after refreshing, you should now see the agent's status set to `Connected`.<br>

    <figure><img src="../../../../.gitbook/assets/image (55) (2).png" alt=""><figcaption></figcaption></figure>
2. (Optional) If the Agent Connection shows as `Disconnected`, inspect the agent container logs for error messages.

### Helm <a href="#helm" id="helm"></a>

To deploy the federation agent to your Kubernetes cluster, complete the following steps:

**Update your Helm Chart**

Add the Gravitee Helm repository and update it to ensure you have access to the latest charts:

```bash
helm repo add gravitee https://helm.gravitee.io

helm repo update
```

#### Configure the Federation Agent Helm Values

Create the Helm values file based on your APIM management API's certificate setup. You can use the standard configuration or custom certificate configuration:

* [#standard-configuration](./#standard-configuration "mention")
* [#custom-certificate-configuration](./#custom-certificate-configuration "mention")

#### Standard configuration

1.  This configuration uses the default Java truststore for your APIM management API certificates. Create a file named `federation-agent-aws-values.yaml` in your working directory, and then copy the following configuration:

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
          name: federation-agent-aws-api-gateway
          tag: 4.8.4

        resources:
          requests:
            memory: "256Mi"
            cpu: "100m"
          limits:
            memory: "512Mi"
            cpu: "250m"

    # =========================
    # Gravitee / AWS Agent
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
            - type: aws-api-gateway
              integrationId: [your-integration-id]
              configuration:
                region: [your-aws-region]
                accessKeyId: [your-key-id]
                secretAccessKey: [your-access-key]
                acceptApiWithoutUsagePlan: false
    ```
2. Make the following modifications to your `federation-agent-aws-values.yaml` file:

* Replace `[your-cloud-token]` with your Gravitee Cloud token or remove the entire `cloud:` section if using self-hosted APIM.
* Replace `[your-APIM-management-API-host]` with your APIM management API URL. For example, `apim.example.com` or `gravitee-apim-api.gravitee-apim.svc.cluster.local:8083` for the internal Kubernetes service.
* Replace `[your-token]` with your service account bearer token.
* Replace `[your-integration-id]` with the Integration ID.
* Replace `[your-aws-region]` with your AWS region. For example, us-west-2.
* Replace `[your-key-id]` with your AWS access key ID.
* Replace `[your-access-key]` with your AWS secret access key.

3.  Deploy the federation agent to your Kubernetes cluster by running the following command:

    ```bash
    helm install federation-agent-aws \
      gravitee/federation-agent \
      -f federation-agent-aws-values.yaml \
      -n gravitee-apim \
      --create-namespace
    ```

#### Custom certificate configuration

1.  This configuration includes custom truststore volume mounts for certificates from private certificate authorities or self-signed certificates. Create a file named `federation-agent-aws-values.yaml`, and then copy the following configuration:

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
            secretName: aws-truststore

      deployment:
        image:
          repository: graviteeio
          name: federation-agent-aws-api-gateway
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
    # Gravitee / AWS Agent
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
                  password: secret://kubernetes/aws-truststore:password?namespace=gravitee-apim
          
          providers:
            - type: aws-api-gateway
              integrationId: [your-integration-id]
              configuration:
                region: [your-aws-region]
                accessKeyId: [your-key-id]
                secretAccessKey: [your-access-key]
                acceptApiWithoutUsagePlan: false
    ```

{% hint style="info" %}
If your APIM management API uses certificates that require a custom truststore, you must create the truststore and add it to Kubernetes as a secret before deploying the agent.
{% endhint %}

2. Make the following modifications to your `federation-agent-aws-values.yaml` file:
   * Replace `[your-cloud-token]` with your Gravitee Cloud token or remove the entire `cloud:` section if using self-hosted APIM.
   * Replace `[your-APIM-management-API-host]` with your APIM management API URL. For example, `apim.example.com` or `gravitee-apim-api.gravitee-apim.svc.cluster.local:8083` for the internal Kubernetes service.
   * Replace `[your-token]` with your service account bearer token.
   * Replace `[your-integration-id]` with the Integration ID.
   * Replace `[your-aws-region]` with your AWS region. For example, us-west-2.
   * Replace `[your-key-id]` with your AWS access key ID.
   * Replace `[your-access-key]` with your AWS secret access key.
3.  Deploy the federation agent to your Kubernetes cluster by running the following command:

    ```bash
    helm install federation-agent-aws \
      gravitee/federation-agent \
      -f federation-agent-aws-values.yaml \
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
    federation-agent-aws-xxxxx-yyyyy        1/1     Running   0          30s
    ```
2.  Return to the Gravitee API Management console, refresh the page, and verify that the agent's status is set to Connected:

    <figure><img src="../../../../.gitbook/assets/image (55) (2).png" alt=""><figcaption></figcaption></figure>

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

## Discover AWS APIs that are not part of a usage plan

By default, the AWS agent only discovers REST APIs that are attached to a usage plan in AWS. To ingest REST APIs that are not attached to a usage plan, use the `acceptApiWithoutUsagePlan` parameter.

{% hint style="info" %}
If you ingest an API that is attached to a usage plan, Gravitee creates a plan for that API. If you detach an API from a usage plan, the plan that is created is not automatically removed, and you must remove the plan manually.
{% endhint %}
