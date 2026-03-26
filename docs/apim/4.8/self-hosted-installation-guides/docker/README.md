---
description: Configuration guide for docker.
---

# Docker

## Deployment methods

* [docker-compose.md](docker-compose.md "mention")
* [docker-cli.md](docker-cli.md "mention")

## Architecture of Gravitee API Management with Docker

The following diagram shows the architecture that is common to each Docker installation method:

<figure><img src="https://docs.gravitee.io/images/apim/3.x/installation/docker/apim_simple_docker_architecture.png" alt="Diagram showing the architecture of Gravitee API Management installed on Docker"><figcaption><p>Docker installation architecture</p></figcaption></figure>

## Configuration of the individual components

The following table shows the component configurations for Docker installation methods:

<table><thead><tr><th width="140">Component</th><th width="227">Docker container name</th><th width="103">Networks</th><th width="152">Published port</th><th>Storage</th></tr></thead><tbody><tr><td>API Gateway</td><td><code>gio_apim_gateway</code></td><td><code>frontend</code>, <code>storage</code></td><td><code>8082</code></td><td><code>/gravitee/apim-gateway</code></td></tr><tr><td>Management API</td><td><code>gio_apim_management_api</code></td><td><code>frontend</code>, <code>storage</code></td><td><code>8083</code></td><td><code>/gravitee/apim-management-api</code></td></tr><tr><td>Console</td><td><code>gio_apim_management_ui</code></td><td><code>frontend</code></td><td><code>8084</code></td><td><code>/gravitee/apim-management-ui</code></td></tr><tr><td>Developer Portal</td><td><code>gio_apim_portal_ui</code></td><td><code>frontend</code></td><td><code>8085</code></td><td><code>/gravitee/apim-portal-ui</code></td></tr><tr><td>MongoDB</td><td><code>gio_apim_mongodb</code></td><td><code>storage</code></td><td>n/a</td><td><code>/gravitee/mongodb</code></td></tr><tr><td>Elasticsearch</td><td><code>gio_apim_elasticsearch</code></td><td><code>storage</code></td><td>n/a</td><td><code>/gravitee/elasticsearch</code></td></tr></tbody></table>
