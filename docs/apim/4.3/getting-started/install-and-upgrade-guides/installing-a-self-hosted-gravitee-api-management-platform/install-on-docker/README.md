---
description: Configuration guide for Installing Gravitee API Management with Docker.
---

# Installing Gravitee API Management with Docker

There are three methods for installing Gravitee API Management (APIM) with Docker:

<table data-view="cards"><thead><tr><th data-type="content-ref"></th><th></th><th></th><th data-hidden data-card-target data-type="content-ref"></th></tr></thead><tbody><tr><td><a href="quick-install-with-docker-compose.md">quick-install-with-docker-compose.md</a></td><td>With this method, you install Gravitee API Management quickly without any additional plugins.</td><td></td><td><a href="quick-install-with-docker-compose.md">quick-install-with-docker-compose.md</a></td></tr><tr><td><a href="custom-install-with-docker-compose.md">custom-install-with-docker-compose.md</a></td><td>With this method, you install Gravitee API Management with additional plugins, and you control the location of the persistent data.</td><td></td><td><a href="custom-install-with-docker-compose.md">custom-install-with-docker-compose.md</a></td></tr><tr><td><a href="docker-images-install.md">docker-images-install.md</a></td><td>With this method, you create all the components to install Gravitee API Management using the command line.</td><td></td><td><a href="docker-images-install.md">docker-images-install.md</a></td></tr></tbody></table>

## Architecture of Gravitee API Management with Docker

The following diagram shows the architecture that is common each Docker installation method:

<figure><img src="https://docs.gravitee.io/images/apim/3.x/installation/docker/apim_simple_docker_architecture.png" alt=""><figcaption><p>Docker installation architecture</p></figcaption></figure>

## Configuration of the individual components

The following table shows the configuration of the components for the installations methods on Docker:

| Component        | Docker container name     | Networks              | Published port | Storage (where used)            |
| ---------------- | ------------------------- | --------------------- | -------------- | ------------------------------- |
| API Gateway      | `gio_apim_gateway`        | `frontend`, `storage` | `8082`         | `/gravitee/apim-gateway`        |
| Management API   | `gio_apim_management_api` | `frontend`, `storage` | `8083`         | `/gravitee/apim-management-api` |
| Console          | `gio_apim_management_ui`  | `frontend`            | `8084`         | `/gravitee/apim-management-ui`  |
| Developer Portal | `gio_apim_portal_ui`      | `frontend`            | `8085`         | `/gravitee/apim-portal-ui`      |
| MongoDB          | `gio_apim_mongodb`        | `storage`             | n/a            | `/gravitee/mongodb`             |
| Elasticsearch    | `gio_apim_elasticsearch`  | `storage`             | n/a            | `/gravitee/elasticsearch`       |
