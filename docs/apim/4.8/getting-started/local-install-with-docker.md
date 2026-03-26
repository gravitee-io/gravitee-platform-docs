---
description: Setup guide for local install with docker.
---

# Local Install with Docker

### Prerequisites

* You must install Docker. For more information about installing Docker, go to [Docker Desktop](https://docs.docker.com/desktop/).
* You must create a working directory for Gravitee.

### Installing Gravitee API Management with Docker

1.  Download the `docker-compose.yml` file as `docker-compose-apim.yml` using the following command:

    ```bash
    curl -L https://bit.ly/docker-apim-4x -o docker-compose-apim.yml
    ```
2. (**Enterprise Edition only**) Add you license key by completing the follow sub-steps:
   1. In a text editor, open `docker-compose-apim.yml.`
   2. Navigate to `$services.management_api.volumes`.
   3.  On a new line, add the path to the license key. This addition ensures that the Management API can access the licensing key.

       ```bash
       - ./gravitee/license.key:/opt/graviteeio-management-api/license/license.key
       ```
3.  Start the components using the following command:

    ```bash
    docker compose -f docker-compose-apim.yml up -d
    ```

{% hint style="info" %}
APIM can take up to a minute to fully initialize with Docker.
{% endhint %}

### **Verification**

Once Docker is initialized, you can access the Console and the Developer Portal by following the following steps:

1. To open the Console, start your browser, and then go to `http://localhost:8084`.
   * Default username: admin
   * Default password: admin
2. To open the Developer Portal, start your browser, and then go to `http://localhost:8085`.
   * Default username: admin
   * Default password: admin
