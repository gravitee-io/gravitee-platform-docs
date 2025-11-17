# Custom Install with Docker Compose

## Overview

This page describes how to install and run APIM Community Edition or APIM Enterprise Edition in Docker containers on `localhost` using the `docker compose` command and a specified filesystem for persistence and plugins. Compared to the [Quick Install with Docker Compose](quick-install-with-docker-compose.md), installing in this way gives more granular control of where persistence data is stored and the ability to add custom plugins.

## Prerequisites

Docker must be installed and running. For more information about installing Docker, see the [Docker website](https://www.docker.com/).

If you want to install the Enterprise Edition, you must have a license key for the APIM Enterprise Edition. For more information about getting a license key, visit the [Gravitee pricing page](https://www.gravitee.io/pricing).

## Installing APIM

### Create the filesystem and download the Docker compose file

1. We need the following directory structure for persisting data, storing plugins, and keeping a copy of the Docker Compose file.

```
/gravitee
 ├── docker-compose-apim.yaml
 ├── apim-gateway
 │    ├── logs
 │    └── plugins
 ├── apim-management-api
 │    ├── logs
 │    └── plugins
 ├── apim-management-ui
 │    └── logs
 ├── apim-portal-ui
 │    └── logs
 ├── elasticsearch
 │    └── data
 └── mongodb
     └── data
```

Create it with the following command.

{% code overflow="wrap" %}
```sh
mkdir -p ./gravitee/{mongodb/data,elasticsearch/data,apim-gateway/plugins,apim-gateway/logs,apim-management-api/plugins,apim-management-api/logs,apim-management-ui/logs,apim-portal-ui/logs}
```
{% endcode %}

2. Enter the `/gravitee` directory.
3. Download the `docker-compose.yml` file as `docker-compose-apim.yml`.

```
curl -L https://bit.ly/docker-apim-4x -o docker-compose-apim.yml
```

### Edit `docker-compose-apim.yml`

We are now going to edit `docker-compose-apim.yml` so the installation uses the `/gravitee` filesystem.

1. Open `docker-compose-apim.yml` in a text editor.
2. Remove the following lines.

```
volumes:
  data-elasticsearch:
  data-mongo:
```

3. Change `$services.mongodb.volumes` from

```
    volumes:
      - data-mongo:/data/db
      - ./logs/apim-mongodb:/var/log/mongodb
```

to

```
    volumes:
      - ./mongodb/data:/data/db
```

{% hint style="info" %}
The MongoDB container logs should be accessed using the `docker logs gio_apim_mongodb` command.
{% endhint %}

4. Change `$services.elasticsearch.volumes` from

```
    volumes:
      - data-elasticsearch:/usr/share/elasticsearch/data
```

to

```
    volumes:
      - ./elasticsearch/data:/var/lib/elasticsearch/data
```

{% hint style="info" %}
The Elasticsearch container logs should be accessed using the `docker logs gio_apim_elasticsearch` command.
{% endhint %}

5. Change `$services.gateway.volumes` from

```
    volumes:
      - ./logs/apim-gateway:/opt/graviteeio-gateway/logs
```

to

```
    volumes:
      - ./apim-gateway/logs:/opt/graviteeio-gateway/logs
      - ./apim-gateway/plugins:/opt/graviteeio-gateway/plugins-ext
```

6. Add the following lines to `$services.gateway.environment`.

```
      - gravitee_plugins_path_0=/opt/graviteeio-gateway/plugins
      - gravitee_plugins_path_1=/opt/graviteeio-gateway/plugins-ext
```

7. Remove `$services.management_api.links`.
8. Change `$services.management_api.volumes` from

```
    volumes:
      - ./logs/apim-management-api:/opt/graviteeio-management-api/logs
```

to

```
    volumes:
      - ./apim-management-api/logs:/opt/graviteeio-management-api/logs
      - ./apim-management-api/plugins:/opt/graviteeio-management-api/plugins-ext
```

9. Add the following lines to `$services.management_api.environment`.

```
      - gravitee_plugins_path_0=/opt/graviteeio-management-api/plugins
      - gravitee_plugins_path_1=/opt/graviteeio-management-api/plugins-ext
```

10. Change `$services.management_ui.volumes` from

```
    volumes:
      - ./logs/apim-management-ui:/var/log/nginx
```

to

```
    volumes:
      - ./apim-management-ui/logs:/var/log/nginx
```

11. Change `$services.portal_ui.volumes` section from

```
    volumes:
      - ./logs/apim-portal-ui:/var/log/nginx
```

to

```
    volumes:
      - ./apim-portal-ui/logs:/var/log/nginx
```

### Add the license key

If you are installing the Enterprise Edition, you need to add the license key. If you are installing the Community Edition, skip these steps.

1. Copy your license key to `/gravitee/license.key`.
2. Open `docker-compose-apim.yml` in a text editor, and under `$services.gateway.volumes` add the following line.

```
 - ./license.key:/opt/graviteeio-gateway/license/license.key
```

3. Under `$services.management_api.volumes` add the following line.

```
 - ./license.key:/opt/graviteeio-management-api/license/license.key
```

### Run `docker compose`

1. Run `docker compose` to download and start all of the components.

```
docker compose -f docker-compose-apim.yml up -d
```

2. In your browser, go to `http://localhost:8084` to open the Console, and go to `http://localhost:8085` to open the Developer Portal. You can log in to both with the username `admin` and password `admin`.

{% hint style="info" %}
**Container initialization**

APIM can take up to a minute to fully initialize with Docker. If you get an error when going to `http://localhost:8084` or `http://localhost:8085`, wait a few minutes and try again.
{% endhint %}

You can adapt the above instructions to suit your architecture if you need to.

{% hint style="success" %}
Congratulations! Now that APIM is up and running, check out the [Quickstart Guide](../../quickstart-guide/README.md) for your next steps.
{% endhint %}
