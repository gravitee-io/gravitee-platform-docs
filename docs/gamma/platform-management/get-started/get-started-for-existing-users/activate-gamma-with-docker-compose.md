---
hidden: false
noIndex: false
---
# Activate Gamma with Docker Compose
<!-- GAP-STRUCTURAL: Missing procedural content source -->

Gravitee Gamma is Gravitee's next-generation unified control plane. It brings API Management, Event Management, Agent Management, Authorization Management, and Platform Management together in a single console, so you manage your APIs, Kafka streams, AI agents and MCP servers, and authorization policies from one place.

{% hint style="warning" %}
Gamma ships in 4.12 (`4.12.0`). Activating Gamma moves your stack to that build. Use this for development and quick-start purposes only. For best practices for production environments, contact your Technical Account Manager.
{% endhint %}

## Overview

If you already run Gravitee API Management with Docker Compose, you turn Gamma on by moving to the Gamma build, enabling Gamma on the Management API, and adding the Gamma console. This page covers only those changes. For the full stack from scratch, see [Run Gamma with Docker Compose](../../install/self-hosted-installation-guides/docker/docker-compose.md).

## Activate Gamma

1. Use the Gamma build. Set the image tags for the Management API, Gateway, APIM Console, and Developer Portal to `4.12.0`.
2. Enable Gamma on the Management API. Add the following environment variables to the Management API service. Adjust the CORS origin to the URL where you serve the Gamma console:

   ```yaml
   - gravitee_gamma_enabled=true
   - gravitee_http_cors_enabled=true
   - gravitee_http_cors_allow-origin=http://localhost:8086
   - gravitee_http_cors_allow-credentials=true
   - gravitee_http_cookie_sameSite=Lax
   - gravitee_http_cookie_secure=false
   ```
3. Enable Gamma on the Gateway. Add the following environment variable to the Gateway service. This is required to sync AuthZ policies (PDP) for Authorization Management:

   ```yaml
   - gravitee_gamma_enabled=true
   ```
4. Add the Gamma console. Add a service for `graviteeio/gamma-ui`, pointed at the Management API `/gamma`:

   ```yaml
   gamma-console:
     image: graviteeio/gamma-ui:4.12.0
     ports:
       - "8086:8080"
     environment:
       - GAMMA_API_URL=http://localhost:8083/gamma
       - GAMMA_CONSOLE_BASE_HREF=/
       - HTTP_PORT=8080
       - SERVER_NAME=localhost
   ```
5. Recreate the stack:

   ```bash
   docker compose up -d
   ```

For the full single-host layout, the complete CORS and cookie reasoning, and the enterprise license step for Agent Management, see [Run Gamma with Docker Compose](../../install/self-hosted-installation-guides/docker/docker-compose.md).

## Verification

* Confirm the Management API is ready, then sign in to the Gamma console:

  ```bash
  curl -s -o /dev/null -w "%{http_code}\n" http://localhost:8083/management/v2/ui/bootstrap
  ```

  \
  The command returns `200` once the platform is up. You can then sign in to the Gamma console at `http://localhost:8086` with `admin` / `admin`.

## Next steps

* Create your first MCP server. For more information, see [Create your first MCP server](../../../agent-management/get-started/create-your-first-mcp-server.md).
