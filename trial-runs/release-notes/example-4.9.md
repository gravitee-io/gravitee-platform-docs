# Example: 4.9

## Release Date: October 16, 2025

## Highlights

* New Kafka Console provides a user interface to manage and monitor Kafka clusters.
* New Gravitee Expression Language assistant employs AI to assist with writing expression language.
* Gravitee APIM MCP Server enables AI assistants and MCP clients to use APIM via tools.
* Gravitee SaaS Gateways can be deployed in multiple providers and regions for a single environment.
* Gravitee SaaS Gateways can be deployed in Google Cloud Provider.
* Gravitee APIM Terraform provider supports Applications & Subscriptions.
* New integration with Ambassador Edge Stack enables discovery and governance of Edge Stack APIs.
* Migration tool converts Gravitee v2 APIs to v4 APIs.
* Improved observability and debugging capabilities.
* Execution transparency analytics provide detailed diagnostics for API execution errors and warnings.
* MongoDB index upgrades introduce 11 new indexes to improve query performance for large datasets.
* New API-level analytics dashboard for Kafka Gateway APIs.

## Breaking Changes

#### **Update to OpenShift compatibility**

* Prior to APIM version 4.9.0, users had to override the `runAsGroup` securityContext to set the GID to 1000. With APIM 4.9.0, users must set the `runAsGroup` securityContext to `null` to let OpenShift select the root group.

*   
    Adds drop-down filters on the APIs screen for type, status, sharding tags, categories, Portal status, and Portal visibility. This lets users quickly narrow large API inventories without crafting Lucene queries.

    <figure><img src="../.gitbook/assets/image (4).png" alt=""><figcaption></figcaption></figure>

    ```yaml
    api:
      federation:
        ingress:
          enabled: true
          path: /integration-controller(/.*)?
          pathType: Prefix
          hosts:
            - apim.example.com
          annotations:
            kubernetes.io/ingress.class: nginx
            nginx.ingress.kubernetes.io/proxy-read-timeout: 3600   
    ```

#### C**ustomization on Federation ingress**

* If the `integration-controller` ingress uses the same host as the `management` ingress, it no longer inherits the annotation of the `management` ingress. With APIM 4.9.0, you must configure the `integration-controller` ingress with the following values:\
  \
  <br>

```yaml
api:
  federation:
    ingress:
      enabled: true
      path: /integration-controller(/.*)?
      pathType: Prefix
      hosts:
        - apim.example.com
      annotations:
        kubernetes.io/ingress.class: nginx
        nginx.ingress.kubernetes.io/proxy-read-timeout: 3600   
```

```yaml
api:
  federation:
    ingress:
      enabled: true
      path: /integration-controller(/.*)?
      pathType: Prefix
      hosts:
        - apim.example.com
      annotations:
        kubernetes.io/ingress.class: nginx
        nginx.ingress.kubernetes.io/proxy-read-timeout: 3600   
```

* **Elasticsearch template updates required**\
  When you upgrade to 4.9.0, you must update Elasticsearch templates to support execution transparency analytics with error and warning component tracking. If you manage your own Elasticsearch installation, update index templates before you upgrade. Elasticsearch auto-generates templates if you do not manually update them, but this results in suboptimal field mappings. Gravitee-managed Elasticsearch or SaaS deployments update automatically.

## New Features

* **API traffic dashboard**\
  Introduces an API traffic dashboard for v4 proxy APIs. This dashboard provides the following key metrics for users to quickly spot issues and usage patterns: total requests, min/max/average response times, and requests per second.
* **v2 to v4 API migration**\
  The APIM Console includes a new API migration workflow that guides users through converting v2 APIs to v4 APIs. Migrated v2 APIs can be verified to be fully compatible with the v4 API definition, allowing teams to adopt the supported v4 model safely.\
  Historical analytics are not available after migration, and analytics are reset for the migrated API. Migration is reversible, but users should plan for analytics gaps until continuity is delivered in a future release.
*   **New Developer Portal homepage customization**

    <div data-gb-custom-block data-tag="hint" data-style="warning" class="hint hint-warning"><p>This feature is in tech preview.</p></div>

    Enables customization of the New Developer Portal homepage using standard Markdown or Gravitee Markdown (GMD). GMD is standard Markdown enriched with Gravitee Markdown components.
* **Expression Language (EL) assistant**\
  Introduces the Gravitee Expression Language (EL) assistant. This assistant converts prompts into expression language that can be used in any field that supports EL.
* **AWS multi-account Federation**\
  Introduces multi-account and multi-region support for the AWS API Gateway Federation Agent. Supports StackSets and manual IAM setups with CloudFormation/ECS, enabling enterprises to discover and manage APIs across many AWS accounts and regions from APIM.
* **Edge Stack Federation agent**\
  New Edge Stack Federation provider enables Edge Stack APIs to be discovered and governed from APIM. Once the Edge Stack integration is created, the agent can be run via Docker Compose or Helm.
* **Kafka cluster management**\
  The APIM Console now allows users to create and manage Kafka clusters, configure cluster connection information, and manage user access and permissions.
*   **Kafka Console**

    <div data-gb-custom-block data-tag="hint" data-style="warning" class="hint hint-warning"><p>This feature is available in private tech preview. Contact your account manager if you are interested.</p></div>

    Introduces Gravitee Kafka Console, which integrates with APIM to provide a user interface with which to browse and manage core Kafka resources, such as topics, partitions, and consumer groups, and to produce and consume messages. Kafka Console is based on Kafbat UI and communicates with the APIM Management API through JWT-based authentication. This feature is available only for self-hosted deployments and not compatible with next-gen cloud.
* **Expose APIM as an MCP Server**\
  The Gravitee MCP Server allows AI assistants and other MCP clients to manage APIM resources. For example, clients such as Cursor or Claude Code can list APIs, view API logs, and manage subscriptions and documentation. This feature enables natural-language workflows with permissions scoped by the service account.
* **Execution transparency analytics**\
  Introduces execution transparency analytics that provide clear, actionable diagnostics when errors occur during API execution. This feature enables troubleshooting by exposing detailed information about the root cause of failures and warnings. Available for v4 APIs and v2 APIs running on the v4 execution engine.
* **MongoDB index upgrades**\
  Introduces 11 new MongoDB indexes designed to improve query performance for large datasets.
* **Expose Kafka analytics**\
  Introduces a new Kafka analytics dashboard that displays operational metrics for Kafka APIs for deployments that use the Elasticsearch reporter. The metrics are stored as time‑series data, which enables real‑time monitoring and analysis of Kafka API performance, message activity, and connection patterns.

## Updated features

* **API logging**\
  The logs for an individual API are now accessible directly from the API's navigation. The v4 proxy API log table has been enriched with additional information that is easily surfaced via improved searchability. The detailed view for individual logs has been updated for clarity and to facilitate analysis.
* **DCR trusted certificates**\
  KeyStore and TrustStore trusted certificates can now be used to configure Dynamic Client Registration (DCR).
* **User roles and groups mappings**\
  Token payloads can now be parsed in role and group mapping conditions. Mappings can now reference `accessToken` and `idToken` objects to drive fine-grained access decisions.
* **API list column visibility**\
  Introduces column visibility controls on the APIs screen with choices saved in browser storage. Users can tailor the list view to show only the details they care about and persist those preferences. The following details can be displayed: name, type, status, access, quality, sharding tags, categories, owner, Portal status, and Portal visibility.
*   **API list filters**\
*   Adds drop-down filters on the APIs screen for type, status, sharding tags, categories, Portal status, and Portal visibility. 

    <figure><img src="../.gitbook/assets/image (4).png" alt=""><figcaption></figcaption></figure>
* **Policy Studio search and navigation**\
  Adds navigation and search tips to the v4 Policy Studio, explaining how plans and flows are labeled and how the single search box filters by plan name, flow name, or path. It also shows how to search the policy selector by name/description, making it faster to find and manage flows and policies in complex APIs.
* **Developer Portal CSS tokens**\
  Adds component-specific CSS tokens for layout and theme customization. This helps Portal administrators customize typography and UI elements consistently across the New Developer Portal.
* **Secret renewal**\
  Users can set the `renewable` parameter to `true` to automatically renew a secret. Setting the `reloadOnChange` parameter to `true` reloads the API when there is a new secret value.
*   **Terraform resources**

    <div data-gb-custom-block data-tag="hint" data-style="warning" class="hint hint-warning"><p>This feature is in tech preview.</p></div>

    The Gravitee Terraform provider now supports Application and Subscription resources.
