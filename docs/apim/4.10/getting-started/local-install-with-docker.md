### Overview

This guide explains how to install a complete self-hosted Gravitee API Management (APIM) platform using Docker Compose. This installation method is suitable for development, testing, and quick-start scenarios.

{% hint style="warning" %}
This installation guide is for development and quick-start purposes only. Do not use it for production environments. For production deployment guidance, contact your Technical Account Manager.
{% endhint %}

### Prerequisites

Before installing Gravitee APIM with Docker, ensure you have:

* Docker installed on your system. For installation instructions, see [Docker Desktop](https://docs.docker.com/desktop/).
* A working directory for Gravitee files.
* **(Enterprise Edition only)** A valid license key. For more information, see [enterprise-edition.md](../readme/enterprise-edition.md "mention").

### Installation steps

#### 1. Download the Docker Compose file

Download the `docker-compose.yml` file to your working directory:

```bash
curl -L https://bit.ly/docker-apim-4x -o docker-compose-apim.yml
```

#### 2. (Enterprise Edition only) Configure the license key

If you are using Enterprise Edition, complete the following steps:

1. In your working directory, create a subfolder named `gravitee`.
2. Copy your license key file into the `gravitee` subfolder.
3. Open `docker-compose-apim.yml` in a text editor.
4. Navigate to the `services.management_api` section.
5. Add a `volumes` section if it does not already exist.
6. Add the following volume mount to make the license key accessible to the Management API:

```yaml
volumes:
  - ./gravitee/license.key:/opt/graviteeio-management-api/license/license.key
```

#### 3. Start the APIM components

Run the following command to start all APIM components:

```bash
docker compose -f docker-compose-apim.yml up -d
```

{% hint style="info" %}
APIM can take up to a minute to fully initialize with Docker.
{% endhint %}

### Verification

After the containers start, verify the installation:

* **APIM Console**: Navigate to `http://localhost:8084`. Log in with username `admin` and password `admin`.
* **Developer Portal**: Navigate to `http://localhost:8085`. Log in with username `admin` and password `admin`.

### Next steps

* Create your first API. For more information, see [create-and-publish-your-first-api](create-and-publish-your-first-api/ "mention").