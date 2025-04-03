# Docker

There are three methods for installing Gravitee API Management (APIM) with Docker:

<table data-view="cards"><thead><tr><th data-type="content-ref"></th><th></th><th data-hidden data-card-target data-type="content-ref"></th></tr></thead><tbody><tr><td><a href="quick-install.md">quick-install.md</a></td><td>Quickly install Docker without any additional plugins</td><td><a href="quick-install.md">quick-install.md</a></td></tr><tr><td><a href="docker-compose.md">docker-compose.md</a></td><td>Add additional plugins and control the location of the persistent data             </td><td><a href="docker-compose.md">docker-compose.md</a></td></tr><tr><td><a href="docker-images.md">docker-images.md</a></td><td>Create all the components for the installation using the command line        </td><td><a href="docker-images.md">docker-images.md</a></td></tr></tbody></table>

## Architecture of Gravitee API Management with Docker

The following diagram shows the architecture that is common each Docker installation method:

<figure><img src="https://docs.gravitee.io/images/apim/3.x/installation/docker/apim_simple_docker_architecture.png" alt="Diagram showing the architecture of Gravitee API Management installed on Docker"><figcaption><p>Docker installation architecture</p></figcaption></figure>



## Configuration of the individual components

The following table shows the configuration of the components for the installations methods on Docker:

<table><thead><tr><th width="140">Component</th><th width="227">Docker container name</th><th width="103">Networks</th><th width="152">Published port</th><th>Storage</th></tr></thead><tbody><tr><td>API Gateway</td><td><code>gio_apim_gateway</code></td><td><code>frontend</code>, <code>storage</code></td><td><code>8082</code></td><td><code>/gravitee/apim-gateway</code></td></tr><tr><td>Management API</td><td><code>gio_apim_management_api</code></td><td><code>frontend</code>, <code>storage</code></td><td><code>8083</code></td><td><code>/gravitee/apim-management-api</code></td></tr><tr><td>Console</td><td><code>gio_apim_management_ui</code></td><td><code>frontend</code></td><td><code>8084</code></td><td><code>/gravitee/apim-management-ui</code></td></tr><tr><td>Developer Portal</td><td><code>gio_apim_portal_ui</code></td><td><code>frontend</code></td><td><code>8085</code></td><td><code>/gravitee/apim-portal-ui</code></td></tr><tr><td>MongoDB</td><td><code>gio_apim_mongodb</code></td><td><code>storage</code></td><td>n/a</td><td><code>/gravitee/mongodb</code></td></tr><tr><td>Elasticsearch</td><td><code>gio_apim_elasticsearch</code></td><td><code>storage</code></td><td>n/a</td><td><code>/gravitee/elasticsearch</code></td></tr></tbody></table>
