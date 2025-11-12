# Fully self-hosted installation with Docker

{% hint style="warning" %}
This installation guide is for only development and quick start purposes. Do not use it for production environments. For more information about best practices for production environments, contact Gravitee.
{% endhint %}

## Prerequisites

* Install Docker. For more information about installing Docker, see [Docker Desktop](https://docs.docker.com/desktop/).
* Create a working directory for Gravitee.
* **(Enterprise Edition only)** Obtain a license key. For more information about Enterprise Edition, see [enterprise-edition.md](docs/apim/4.9/readme/enterprise-edition.md "mention").

## Install Gravitee API Management with Docker

1.  Download the `docker-compose.yml` file to your working directory as `docker-compose-apim.yml` using the following command:

    ```bash
    curl -L https://bit.ly/docker-apim-4x -o docker-compose-apim.yml
    ```
2. **(Enterprise Edition only)** In your working directory, create a sub-folder called `gravitee`, and then add your license key to this sub-folder.
3. **(Enterprise Edition only)** Add your license key to your `docker-compose-apim.yml` by completing the following sub-steps:
   1. In a text editor, open `docker-compose-apim.yml`.
   2. Navigate to `$services.management_api`, and then add a `volumes` section.
   3.  In the volumes section, add the path to the license key. This addition ensures that the Management API can access the license key.

       ```yaml
       - ./gravitee/license.key:/opt/graviteeio-management-api/license/license.key
       ```
4.  Start the components using the following command:

    ```bash
    docker compose -f docker-compose-apim.yml up -d
    ```

{% hint style="info" %}
APIM can take up to a minute to fully initialize with Docker.
{% endhint %}

## **Verification**

* To open the APIM Console, go to `http://localhost:8084`. The default username and password are both `admin`.
* To open the Developer Portal, go to `http://localhost:8085`. The default username and password are both `admin`.

## Next steps

* Create your first API. For more information about creating your first API, see [create-and-publish-your-first-api](create-and-publish-your-first-api/ "mention").
