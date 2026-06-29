---
hidden: false
noIndex: true
---
# Docker

## Deployment methods

Deploy a hybrid Gamma Gateway on a single host with one of the following Docker methods.

* [Docker Compose](docker-compose.md)
* [Docker CLI](docker-cli.md)

## Components

A hybrid Docker deployment runs the data plane only. The following table lists the containers, their names, and their published ports.

<table><thead><tr><th>Component</th><th>Container name</th><th>Published port</th></tr></thead><tbody><tr><td>API Gateway</td><td><code>gio_gamma_hybrid_gateway</code></td><td><code>8082</code></td></tr><tr><td>Redis (rate limiting)</td><td><code>gio_gamma_hybrid_redis</code></td><td><code>6379</code></td></tr></tbody></table>

<!-- TODO: Add a Gamma hybrid Docker architecture diagram -->
