---
description: An overview about Quick Install Gravitee API Management with Docker Compose.
---

# Quick Install Gravitee API Management with Docker Compose

## Overview

This page describes how to install and run Gravitee API Management (APIM) Community Edition or APIM Enterprise Edition in Docker containers on `localhost` using the `docker compose` command.

{% hint style="warning" %}
This installation method does not allow for custom plugins. To add custom plugins, see [Custom Install with Docker Compose](custom-install-with-docker-compose.md).
{% endhint %}

## Prerequisites

* Docker is installed and running
* The Enterprise Edition requires a [license key](https://www.gravitee.io/pricing)

## Install APIM

1.  Download the `docker-compose.yml` file as `docker-compose-apim.yml`:

    ```bash
    curl -L https://bit.ly/docker-apim-4x -o docker-compose-apim.yml
    ```
2. If you are installing the Enterprise Edition:
   1. Open `docker-compose-apim.yml` in a text editor
   2.  Add the following line under `$services.gateway.volumes`, where `/gravitee/license.key` is the full path to the license key. This ensures that the Gateway can access the license key.

       ```bash
        - /gravitee/license.key:/opt/graviteeio-gateway/license/license.key
       ```
   3.  Add the following line under `$services.management_api.volumes` , where `/gravitee/license.key` is the full path to the license key. This ensures that the Management API can access the license key.

       ```bash
        - /gravitee/license.key:/opt/graviteeio-management-api/license/license.key
       ```
3.  Run `docker compose` to download and start the components:

    ```bash
    docker compose -f docker-compose-apim.yml up -d
    ```
4.  In your browser:

    1. Go to `http://localhost:8084` to open the Console
    2. Go to `http://localhost:8085` to open the Developer Portal

    You can log in to both with username `admin` and password `admin`.

{% hint style="info" %}
**Container initialization**

APIM can take up to a minute to fully initialize with Docker. If you get an error when going to `http://localhost:8084` or `http://localhost:8085`, wait, then try again.
{% endhint %}

{% hint style="success" %}
Congratulations! Now that APIM is up and running, check out the [Quickstart Guide](../../../quickstart-guide/README.md) for your next steps.
{% endhint %}
