# Install on Docker

## Overview

Choose from the following options to install Gravitee API Management (APIM) with Docker:

<table data-view="cards"><thead><tr><th></th><th></th><th></th><th data-hidden data-card-target data-type="content-ref"></th></tr></thead><tbody><tr><td></td><td>Quick install with <code>docker compose</code></td><td></td><td><a href="quick-install-with-docker-compose.md">quick-install-with-docker-compose.md</a></td></tr><tr><td></td><td>Custom install with <code>docker compose</code></td><td></td><td><a href="custom-install-with-docker-compose.md">custom-install-with-docker-compose.md</a></td></tr><tr><td></td><td>Docker images install</td><td></td><td><a href="docker-images-install.md">docker-images-install.md</a></td></tr></tbody></table>

* The quick install brings up APIM quickly without additional plugins.&#x20;
* The custom install and image-based methods give you the ability to add custom plugins and more control over the location of persistence data.

## Architecture

The diagram below shows the architecture common to all Docker installations.

<figure><img src="https://docs.gravitee.io/images/apim/3.x/installation/docker/apim_simple_docker_architecture.png" alt=""><figcaption><p>Docker installation architecture</p></figcaption></figure>

Components are configured as follows:

| Component        | Docker container name     | Networks              | Published port | Storage (where used)            |
| ---------------- | ------------------------- | --------------------- | -------------- | ------------------------------- |
| API Gateway      | `gio_apim_gateway`        | `frontend`, `storage` | `8082`         | `/gravitee/apim-gateway`        |
| Management API   | `gio_apim_management_api` | `frontend`, `storage` | `8083`         | `/gravitee/apim-management-api` |
| Console          | `gio_apim_management_ui`  | `frontend`            | `8084`         | `/gravitee/apim-management-ui`  |
| Developer Portal | `gio_apim_portal_ui`      | `frontend`            | `8085`         | `/gravitee/apim-portal-ui`      |
| MongoDB          | `gio_apim_mongodb`        | `storage`             | n/a            | `/gravitee/mongodb`             |
| Elasticsearch    | `gio_apim_elasticsearch`  | `storage`             | n/a            | `/gravitee/elasticsearch`       |
