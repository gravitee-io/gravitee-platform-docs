---
description: An overview about Quick Install with Docker Compose.
---

# Quick Install with Docker Compose

## Overview

This page describes how to install and run Gravitee API Management (APIM) Community Edition or APIM Enterprise Edition in Docker containers on `localhost` using the `docker compose` command. If you need granular control over where persistence data is stored, or if you need to add plugins, use the [Custom Install with Docker Compose ](custom-install-with-docker-compose.md)or [Docker Images Install.](docker-images-install.md)

{% hint style="warning" %}
This installation method does not allow for custom plugins. If you plan on adding custom plugins, check out the [Custom Install with Docker Compose](custom-install-with-docker-compose.md).
{% endhint %}

## Prerequisites

Docker must be installed and running. For more information about installing Docker, see the [Docker website](https://www.docker.com/).

If you want to install the Enterprise Edition, you must have a license key. For more information about getting a license key, visit the [Gravitee pricing page](https://www.gravitee.io/pricing).

## Installing APIM

1. Download the `docker-compose.yml` file as `docker-compose-apim.yml`.

```
curl -L https://bit.ly/docker-apim-4x -o docker-compose-apim.yml
```

2. If you are installing the Enterprise Edition, open `docker-compose-apim.yml` in a text editor, and under `$services.gateway.volumes` add the following line.

```
 - /gravitee/license.key:/opt/graviteeio-gateway/license/license.key
```

Where `/gravitee/license.key` is the full path to the license key. This ensures that the Gateway can access the license key.

3. If you are installing the Enterprise Edition, under `$services.management_api.volumes` add the following line.

```
 - /gravitee/license.key:/opt/graviteeio-management-api/license/license.key
```

Where `/gravitee/license.key` is the full path to the license key. This ensures that the Management API can access the license key.

4. Run `docker compose` to download and start all of the components.

```
docker compose -f docker-compose-apim.yml up -d
```

5. In your browser, go to `http://localhost:8084` to open the Console, and go to `http://localhost:8085` to open the Developer Portal. You can log in to both with the username `admin` and password `admin`.

{% hint style="info" %}
**Container initialization**

APIM can take up to a minute to fully initialize with Docker. If you get an error when going to `http://localhost:8084` or `http://localhost:8085`, wait a few minutes and try again.
{% endhint %}

{% hint style="success" %}
Congratulations! Now that APIM is up and running, check out the [Quickstart Guide](../../quickstart-guide/) for your next steps.
{% endhint %}
