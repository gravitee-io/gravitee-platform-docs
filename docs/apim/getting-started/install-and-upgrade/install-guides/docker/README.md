# Docker

Our documentation describes three different ways you can install APIM using Docker.

* [Quick install with `docker compose`](https://docs.gravitee.io/apim/3.x/apim\_installation\_guide\_docker\_compose\_quickstart.html)
* [Custom install with `docker compose`](https://docs.gravitee.io/apim/3.x/apim\_installation\_guide\_docker\_compose.html)
* [Docker images install](https://docs.gravitee.io/apim/3.x/apim\_installation\_guide\_docker\_images.html)

The quick install gets APIM up and running quickly without any additional plugins. The custom install method, and the image-based method, give you more control over the location of persistence data and the ability to add custom plugins.

You should be familiar with [Docker](https://docs.docker.com/) before proceeding with this installation guide.

## Architecture

The following diagram shows the architecture that all of these installation methods use.

<figure><img src="https://docs.gravitee.io/images/apim/3.x/installation/docker/apim_simple_docker_architecture.png" alt=""><figcaption><p>Docker installation architecture</p></figcaption></figure>

The components have the following configuration.

| Component        | Docker container name     | Networks              | Published port | Storage (where used)            |
| ---------------- | ------------------------- | --------------------- | -------------- | ------------------------------- |
| API Gateway      | `gio_apim_gateway`        | `frontend`, `storage` | `8082`         | `/gravitee/apim-gateway`        |
| Management API   | `gio_apim_management_api` | `frontend`, `storage` | `8083`         | `/gravitee/apim-management-api` |
| Console          | `gio_apim_management_ui`  | `frontend`            | `8084`         | `/gravitee/apim-management-ui`  |
| Developer Portal | `gio_apim_portal_ui`      | `frontend`            | `8085`         | `/gravitee/apim-portal-ui`      |
| MongoDB          | `gio_apim_mongodb`        | `storage`             | n/a            | `/gravitee/mongodb`             |
| Elasticsearch    | `gio_apim_elasticsearch`  | `storage`             | n/a            | `/gravitee/elasticsearch`       |

If you need a different architecture, you can adapt these instructions to meet your needs.
