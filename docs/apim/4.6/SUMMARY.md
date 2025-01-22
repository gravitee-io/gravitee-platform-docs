# Table of contents

## Overview

* [Introduction to APIM](README.md)
* [Architecture](overview/architecture.md)
* [Execution Engine](overview/execution-engine.md)
* [Enterprise Edition](overview/enterprise-edition.md)
* [Release Notes](overview/release-notes/README.md)
  * [APIM 4.6](overview/release-notes/apim-4.6.md)
  * [APIM 4.5](https://documentation.gravitee.io/apim/4.5/overview/release-notes/apim-4.5)
  * [APIM 4.4](https://documentation.gravitee.io/apim/4.4/overview/release-notes/apim-4.4)
  * [APIM 4.3](https://documentation.gravitee.io/apim/v/4.3/overview/release-notes/apim-4.3)
  * [APIM 4.2](https://documentation.gravitee.io/apim/v/4.2/overview/release-notes/apim-4.2)
  * [APIM 4.1](https://documentation.gravitee.io/apim/v/4.1/releases-and-changelog/release-notes/apim-4.1)
  * [APIM 4.0](https://documentation.gravitee.io/apim/v/4.0-5/releases-and-changelog/release-notes/apim-4.0)
* [Changelog](overview/changelog/README.md)
  * [APIM 4.5.x](https://documentation.gravitee.io/apim/4.5/overview/changelog/apim-4.5.x)
  * [APIM 4.4.x](https://documentation.gravitee.io/apim/4.4/overview/release-notes/apim-4.4)
  * [APIM 4.3.x](https://documentation.gravitee.io/apim/v/4.3/overview/changelog/apim-4.3.x)
  * [APIM 4.2.x](https://documentation.gravitee.io/apim/v/4.2/overview/changelog/apim-4.2.x)
  * [APIM 4.1.x](https://documentation.gravitee.io/apim/v/4.1/releases-and-changelog/changelogs/apim-4.1.x-changelog)
  * [APIM 4.0.x](https://documentation.gravitee.io/apim/v/4.0-5/releases-and-changelog/changelogs/apim-4.0.x-changelog)
* [Support](overview/support.md)

## Getting started

* [Production-ready Environment](getting-started/production-ready-environment/README.md)
  * [Best Practices](getting-started/production-ready-environment/best-practices.md)
  * [Internal APIs](getting-started/production-ready-environment/internal-apis.md)
  * [Deployments](getting-started/production-ready-environment/deployments.md)
  * [Authentication](getting-started/production-ready-environment/authentication.md)
  * [Protections](getting-started/production-ready-environment/protections.md)
  * [Settings](getting-started/production-ready-environment/settings.md)
* [Integrations](getting-started/integrations.md)
* [Plugins](getting-started/plugins/README.md)
  * [Deployment](getting-started/plugins/deployment.md)
  * [Customization](getting-started/plugins/customization.md)
* [Gravitee Expression Language](getting-started/gravitee-expression-language.md)
* [Use Case Tutorials](getting-started/use-case-tutorials/README.md)
  * [Rate Limit REST APIs](getting-started/use-case-tutorials/rate-limit-rest-apis.md)
  * [Configure JWT Security](getting-started/use-case-tutorials/configure-jwt-security.md)
  * [Add RBAC to your JWT Plan](getting-started/use-case-tutorials/add-rbac-to-your-jwt-plan.md)
  * [Configure DCR](getting-started/use-case-tutorials/configure-dcr.md)
  * [Secure and Expose gRPC Services](getting-started/use-case-tutorials/secure-and-expose-grpc-services.md)
  * [Expose SOAP Webservices as REST APIs](getting-started/use-case-tutorials/expose-soap-webservices-as-rest-apis.md)

## Install and upgrade

* [Docker](install-and-upgrade/docker/README.md)
  * [Quick Install](install-and-upgrade/docker/quick-install.md)
  * [Docker Compose](install-and-upgrade/docker/docker-compose.md)
  * [Docker Images](install-and-upgrade/docker/docker-images.md)
  * [Customize your Installation](install-and-upgrade/docker/customize-your-installation.md)
* [.ZIP](install-and-upgrade/.zip.md)
* [Kubernetes](install-and-upgrade/kubernetes.md)
* [OpenShift](install-and-upgrade/openshift.md)
* [RPM](install-and-upgrade/rpm/README.md)
  * [Quick install](install-and-upgrade/rpm/quick-install.md)
  * [Manual install](install-and-upgrade/rpm/manual-install.md)
  * [Troubleshooting](install-and-upgrade/rpm/troubleshooting.md)
  * [Upgrade with RPM](install-and-upgrade/rpm/upgrade-with-rpm.md)
* [Multi-tenancy](install-and-upgrade/multi-tenancy.md)
* [Upgrade Guide](install-and-upgrade/upgrade-guide.md)
* [Breaking Changes and Deprecations](install-and-upgrade/breaking-changes-and-deprecations.md)

## Hybrid Deployment

* [Overview](hybrid-deployment/overview.md)
* [Hybrid Install with Docker](hybrid-deployment/hybrid-install-with-docker.md)
* [Hybrid Install with Kubernetes](hybrid-deployment/hybrid-install-with-kubernetes.md)
* [Hybrid Install with .ZIP](hybrid-deployment/hybrid-install-with-.zip.md)
* [SaaS Alert Engine](hybrid-deployment/saas-alert-engine.md)
* [Redis](hybrid-deployment/redis.md)
* [Logstash](hybrid-deployment/logstash.md)
* [Fluentd](hybrid-deployment/fluentd.md)

## Configure APIM

* [APIM Components](configure-apim/apim-components/README.md)
  * [Gravitee Gateway](configure-apim/apim-components/gravitee-gateway.md)
  * [Management API](configure-apim/apim-components/management-api.md)
  * [APIM Console](configure-apim/apim-components/apim-console.md)
  * [Developer Portal](configure-apim/apim-components/developer-portal.md)
* [Cache](configure-apim/cache.md)
* [Environment Properties](configure-apim/environment-properties.md)
* [Repositories](configure-apim/repositories/README.md)
  * [MongoDB](configure-apim/repositories/mongodb.md)
  * [ElasticSearch](configure-apim/repositories/elasticsearch.md)
  * [JDBC](configure-apim/repositories/jdbc.md)
  * [Redis](configure-apim/repositories/redis.md)
* [Secrets Managers](configure-apim/secrets-managers.md)
* [Distributed Sync Process](configure-apim/distributed-sync-process.md)

## Administration

* [Organizations and Environments](administration/organizations-and-environments.md)
* [Authentication](administration/authentication/README.md)
  * [Gravitee Access Management](administration/authentication/gravitee-access-management.md)
  * [Authentication Providers](administration/authentication/authentication-providers.md)
  * [Social Providers](administration/authentication/social-providers.md)
  * [OpenID Connect](administration/authentication/openid-connect.md)
  * [Azure Entra ID](administration/authentication/azure-entra-id.md)
* [User Management](administration/user-management.md)
* [Applications](administration/applications.md)

## Create APIs

* [Overview](create-apis/overview.md)
* [Import APIs](create-apis/import-apis.md)
* [v2 and v4 API Comparison](create-apis/v2-and-v4-api-comparison.md)
* [v2 API Creation Wizard](create-apis/v2-api-creation-wizard.md)
* [v4 API Creation Wizard](create-apis/v4-api-creation-wizard.md)

## Configure v4 APIs

* [General Settings](configure-v4-apis/general-settings.md)
* [Entrypoints](configure-v4-apis/entrypoints/README.md)
  * [HTTP GET](configure-v4-apis/entrypoints/http-get.md)
  * [HTTP POST](configure-v4-apis/entrypoints/http-post.md)
  * [Server-sent Events](configure-v4-apis/entrypoints/server-sent-events.md)
  * [Webhook](configure-v4-apis/entrypoints/webhook.md)
  * [WebSocket](configure-v4-apis/entrypoints/websocket.md)
* [Endpoints](configure-v4-apis/endpoints/README.md)
  * [Azure Service Bus](configure-v4-apis/endpoints/azure-service-bus.md)
  * [Kafka](configure-v4-apis/endpoints/kafka.md)
  * [Mock](configure-v4-apis/endpoints/mock.md)
  * [MQTT5](configure-v4-apis/endpoints/mqtt5.md)
  * [Solace](configure-v4-apis/endpoints/solace.md)
  * [RabbitMQ](configure-v4-apis/endpoints/rabbitmq.md)
* [User Permissions](configure-v4-apis/user-permissions.md)
* [Quality of Service](configure-v4-apis/quality-of-service.md)
* [Response Templates](configure-v4-apis/response-templates.md)
* [CORS](configure-v4-apis/cors.md)
* [Health-checks](configure-v4-apis/health-checks.md)
* [Documentation](configure-v4-apis/documentation.md)
* [Audit Logs](configure-v4-apis/audit-logs.md)
* [Version History](configure-v4-apis/version-history.md)

## Configure v2 APIs

* [General Settings](configure-v2-apis/general-settings.md)
* [Proxy Settings](configure-v2-apis/proxy-settings.md)
* [Load-balancing, Failover, and Health-checks](configure-v2-apis/load-balancing-failover-and-health-checks.md)
* [Service Discovery](configure-v2-apis/service-discovery.md)
* [User and Group Access](configure-v2-apis/user-and-group-access.md)
* [Documentation](configure-v2-apis/documentation.md)

## Kafka Gateway

* [Overview](kafka-gateway/overview.md)
* [Configure the Kafka Gateway and Client](kafka-gateway/configure-the-kafka-gateway-and-client.md)
* [Create Kafka APIs](kafka-gateway/create-kafka-apis.md)
* [Configure Kafka APIs](kafka-gateway/configure-kafka-apis/README.md)
  * [Configuration](kafka-gateway/configure-kafka-apis/configuration.md)
  * [Entrypoints](kafka-gateway/configure-kafka-apis/entrypoints.md)
  * [Endpoints](kafka-gateway/configure-kafka-apis/endpoints.md)
  * [Policies](kafka-gateway/configure-kafka-apis/policies.md)
  * [Consumers](kafka-gateway/configure-kafka-apis/consumers.md)
  * [Documentation](kafka-gateway/configure-kafka-apis/documentation.md)
  * [Deployment](kafka-gateway/configure-kafka-apis/deployment.md)
* [Plans](kafka-gateway/plans.md)
* [Policies](kafka-gateway/policies/README.md)
  * [Kafka ACL](kafka-gateway/policies/kafka-acl.md)
  * [Kafka Topic Mapping](kafka-gateway/policies/kafka-topic-mapping.md)
  * [Kafka Quota](kafka-gateway/policies/kafka-quota.md)
* [Applications](kafka-gateway/applications.md)
* [Subscriptions](kafka-gateway/subscriptions.md)
* [Other ways Gravitee supports Kafka](kafka-gateway/other-ways-gravitee-supports-kafka.md)

## Federation

* [Overview](federation/overview.md)
* [Integrations](federation/integrations.md)
* [Discovery](federation/discovery.md)
* [Federated APIs](federation/federated-apis.md)
* [Federation Agent Service Account](federation/federation-agent-service-account.md)
* [3rd-Party Providers](federation/3rd-party-providers/README.md)
  * [AWS API Gateway](federation/3rd-party-providers/aws-api-gateway.md)
  * [Solace](federation/3rd-party-providers/solace.md)
  * [IBM API Connect](federation/3rd-party-providers/ibm-api-connect.md)
  * [Azure API Management](federation/3rd-party-providers/azure-api-management.md)
  * [Confluent Platform](federation/3rd-party-providers/confluent-platform.md)
  * [Apigee X](federation/3rd-party-providers/apigee-x.md)

## Policies

* [Overview](policies/overview.md)
* [Resources](policies/resources.md)
* [v4 API Policy Studio](policies/v4-api-policy-studio.md)
* [v2 API Policy Studio](policies/v2-api-policy-studio.md)
* [Shared Policy Groups](policies/shared-policy-groups.md)
* [Custom Policies](policies/custom-policies.md)
* [Policy reference](policies/policy-reference.md)
* [Assign Metrics](policies/assign-metrics.md)
* [Avro to JSON transformation](policies/avro-to-json-transformation.md)
* [AVRO to Protobuf Transformation](policies/avro-to-protobuf-transformation.md)
* [Data Logging Masking](policies/data-logging-masking.md)
* [GeoIP Filtering](policies/geoip-filtering.md)
* [GraphQL Rate Limit](policies/graphql-rate-limit.md)
* [InterOPS](policies/interops.md)
* [Kafka Quota](policies/kafka-quota.md)
* [Kafka Topic Mapping](policies/kafka-topic-mapping.md)
* [OAS Validation](policies/oas-validation.md)
* [Protobuf to JSON Transformation](policies/protobuf-to-json-transformation.md)
* [WS Security Authentication](policies/ws-security-authentication.md)
* [CloudEvents](policies/cloudevents.md)
* [WS Security Sign](policies/ws-security-sign.md)
* [XSLT transformer policy](policies/xslt-transformer-policy.md)

## Expose APIs

* [Overview](expose-apis/overview.md)
* [Plans](expose-apis/plans/README.md)
  * [Keyless](expose-apis/plans/keyless.md)
  * [API Key](expose-apis/plans/api-key.md)
  * [OAuth2](expose-apis/plans/oauth2.md)
  * [JWT](expose-apis/plans/jwt.md)
  * [Push](expose-apis/plans/push.md)
  * [mTLS](expose-apis/plans/mtls.md)
* [Applications](expose-apis/applications/README.md)
  * [Global Settings](expose-apis/applications/global-settings.md)
  * [User and Group Access](expose-apis/applications/user-and-group-access.md)
  * [Metadata](expose-apis/applications/metadata.md)
  * [Subscriptions](expose-apis/applications/subscriptions.md)
  * [Notifications](expose-apis/applications/notifications.md)
* [Subscriptions](expose-apis/subscriptions.md)

## API Analytics

* [Dashboards](api-analytics/dashboards.md)
* [API Quality](api-analytics/api-quality.md)
* [Audit Trail](api-analytics/audit-trail.md)

## Gravitee Gateway

* [Internal API](gravitee-gateway/internal-api.md)
* [Dictionaries](gravitee-gateway/dictionaries.md)
* [Tenants](gravitee-gateway/tenants.md)
* [Sharding Tags](gravitee-gateway/sharding-tags.md)
* [Logging](gravitee-gateway/logging.md)
* [OpenTelemetry](gravitee-gateway/opentelemetry.md)
* [Reporters](gravitee-gateway/reporters/README.md)
  * [Formats](gravitee-gateway/reporters/formats.md)
* [Notifications](gravitee-gateway/notifications.md)
* [Alerts](gravitee-gateway/alerts.md)

## Management API

* [Internal API](management-api/internal-api.md)
* [Security](management-api/security.md)
* [Management Settings](management-api/management-settings.md)
* [User Settings](management-api/user-settings.md)
* [Management API Reference](management-api/management-api-reference.md)

## Developer Portal

* [Configuration File](developer-portal/configuration-file.md)
* [Settings](developer-portal/settings.md)
* [Layout and Theme](developer-portal/layout-and-theme.md)
* [Manage Users](developer-portal/manage-users.md)
* [Webhook Subscriptions](developer-portal/webhook-subscriptions.md)
* [Create an Application](developer-portal/create-an-application.md)
* [API Documentation](developer-portal/api-documentation.md)

## Community

* [Community Forum](community/community-forum.md)
* [Contribute to APIM](community/contribute-to-apim.md)
