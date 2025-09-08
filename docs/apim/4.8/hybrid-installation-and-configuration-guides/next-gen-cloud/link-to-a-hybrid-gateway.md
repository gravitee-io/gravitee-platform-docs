---
hidden: true
noIndex: true
---

# Link to a Hybrid Gateway

## Overview&#x20;

This guide explains how to link your new Cloud token to an existing hybrid Gateway.&#x20;

## Prerequisites

* A hybrid deployment.&#x20;
* A Cloud token.&#x20;
* A license key.&#x20;

For more information about acquiring these prerequisites, see [#prepare-your-installation](./#prepare-your-installation "mention").

## Link to a hybrid Gateway

* To link your Cloud token to a hybrid Gateway, follow the steps applicable to your installation method:

{% tabs %}
{% tab title="Docker Compose" %}
1.  In your `.env` file, add the following configuration for your deployment:

    ```
    # The Gateway version must match the Control Plane version to ensure compatibility.
    APIM_VERSION=4.8

    # Use a Redis version that is supported by Gravitee.
    # See the list of supported Redis versions: https://documentation.gravitee.io/apim/configure-apim/repositories/redis#supported-databases
    REDIS_VERSION=7.2-alpine

    # Change this default password before running in any non-local environment.
    REDIS_PASSWORD= <my-defaut-redis-password>

    # Replace with your actual values from Gravitee Cloud.
    CLOUD_TOKEN=<CLOUD_TOKEN>
    LICENSE_KEY=<LICENSE_KEY>
    ```

    * Replace `<CLOUD_TOKEN>` with the Cloud token for your hybrid Gateway.
    * Replace `<LICENSE_KEY>` with your license key.
2.  Restart APIM with the following command:

    ```bash
    docker-compose down
    docker compose -f docker-compose-apim.yml up -d
    ```
{% endtab %}

{% tab title="Kubernetes installations" %}
{% hint style="info" %}
These steps work for all Kubernetes installations.
{% endhint %}

1.  In your `values.yaml` file, navigate to the `env` section, and add the following configuration:

    ```yaml
    env:
      # Gravitee Cloud Token. This is the value gathered in your Gravitee Cloud Account when you install a new Hybrid Gateway.
      - name: gravitee_cloud_token
        value: "<cloud_token>"
    ```

    * Replace `<cloud_token>` with the Cloud token for your hybrid Gateway.
2.  Restart the Helm chart with the following command:

    <pre class="language-bash"><code class="lang-bash"><strong>helm upgrade  graviteeio-apim-gateway graviteeio/apim --namespace gravitee-apim -f ./values.yaml
    </strong></code></pre>
{% endtab %}
{% endtabs %}

### Verification

To verify that your hybrid Gateway is functional, complete the following steps:

*   Run the following command. Replace `{your_gateway_url}` with the URL for your Gateway.

    ```
    curl http://{your_gateway_url}/
    ```
*   Confirm that you receive the following response:&#x20;

    ```
    No context-path matches the request URI.
    ```
