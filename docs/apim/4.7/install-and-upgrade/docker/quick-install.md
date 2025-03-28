# Quick Install

{% hint style="warning" %}
You cannot install Gravitee API Management (APIM) with custom plugins using this installation method. To install custom plugins, see the [Docker Compose](docker-compose.md) installation guide.
{% endhint %}

## Before you begin

* You must install Docker. For more information about installing Docker, go to [Install Docker Engine](https://docs.docker.com/engine/install/).
* If you are deploying the Enterprise Edition of Gravitee, ensure that you have your license key. For more information about license keys, see [Gravitee Platform Pricing](https://www.gravitee.io/pricing).

## Installing Gravitee API Management

1.  Download the `docker-compose.yml` file as `docker-compose-apim.yml` using the following command:

    ```bash
    curl -L https://bit.ly/docker-apim-4x -o docker-compose-apim.yml
    ```
2.  (Optional) If you are installing the Enterprise Edition, add you license key by completing the follow sub-steps:

    a. In a text editor, open `docker-compose-apim.yml.`

&#x20;       b. Navigate to `$services.management_api.volumes`.

&#x20;       c. On a new line, add the path to the license key. This addition ensures that the Gateway can access the licensing key.

```bash
 - /gravitee/license.key:/opt/graviteeio-gateway/license/license.key
```

3. Download, and then start the components using the following command:&#x20;

```bash
docker compose -f docker-compose-apim.yml up -d
```

{% hint style="info" %}
APIM can take up to a minute to fully initialize with Docker.&#x20;
{% endhint %}

4.  Once Docker is initialized, You can access the Console and the Developer Portal by following the following steps:

    a. To open the Console, start your browser, and then go to [http://localhost:8084](http://localhost:8084).

    b. To open the Developer Portal, start your browser, and then go to [http://localhost:8085](http://localhost:8085).

{% hint style="info" %}
* The default username for the Console and the Developer Portal is admin.
* The default password for the Developer Portal is admin.
{% endhint %}
