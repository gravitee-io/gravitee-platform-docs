---
hidden: false
noIndex: false
---
# Docker

## Deployment methods

Install a fully self-hosted Gamma platform on a single host with one of the following Docker methods.

* [Docker Compose](docker-compose.md)
* [Docker CLI](docker-cli.md)

## Components

Both Docker methods run the same set of containers. The following table lists the Gamma components, their container names, and their published ports.

<table><thead><tr><th>Component</th><th>Container name</th><th>Published port</th></tr></thead><tbody><tr><td>API Gateway</td><td><code>gamma_gateway</code></td><td><code>8082</code></td></tr><tr><td>Management API (Gamma enabled)</td><td><code>gamma_management_api</code></td><td><code>8083</code></td></tr><tr><td>APIM Console</td><td><code>gamma_apim_console</code></td><td><code>8084</code></td></tr><tr><td>Developer Portal</td><td><code>gamma_portal</code></td><td><code>8085</code></td></tr><tr><td>Gamma console</td><td><code>gamma_console</code></td><td><code>8086</code></td></tr><tr><td>MongoDB</td><td><code>gamma_mongodb</code></td><td>n/a</td></tr><tr><td>Elasticsearch</td><td><code>gamma_elasticsearch</code></td><td>n/a</td></tr></tbody></table>

<!-- TODO: Add a Gamma self-hosted Docker architecture diagram -->
