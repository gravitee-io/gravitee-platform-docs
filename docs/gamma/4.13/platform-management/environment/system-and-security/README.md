---
hidden: false
noIndex: false
description: The System & Security group of the Environment section holds primary owner mode, Access Management, API review, gateways, alerts, notifications, API health check, SMTP, CORS, API logging, plan types, client registration, and audit.
---

# System & Security

The **System & Security** group of the **Environment** section holds the **Primary Owner Mode**, **Access Management**, **API Review**, **Gateways**, **Alerts**, **Notifications**, and **API Health Check** pages. It also holds the **SMTP**, **CORS**, **API Logging**, **Security Plan Types**, **Client Registration**, and **Audit** pages.

* [**Configure primary owner mode**](../../configure-primary-owner-mode.md). Decide who can be the primary owner of an API or API Product in the environment, and set the mode for APIs and for API Products.
* [**Configure Access Management**](../../configure-access-management.md). Connect the Gamma console to a Gravitee Access Management instance, and recover from a lost connection or an expired token.
* [**Monitor gateway instances**](../../monitor-gateway-instances.md). Read the status of a gateway instance, view its details, monitor its health metrics, and troubleshoot missing data.
* [**Configure environment alerts**](../../configure-environment-alerts.md). Create, edit, and delete alerts, and track their activity and history.
* [**Configure environment notifications**](../../configure-environment-notifications.md). Choose the events you see in the console, add an email or webhook notification, and edit or delete one.
* [**Monitor API health across an environment**](../../monitor-api-health-across-an-environment.md). Choose the window, read the report and the availability of each API, and open the dashboard of an API.
* [**Configure Security Plan Types**](../../configure-security-plan-types.md). Change which plan security types are available to the APIs of the environment.
* [**Configure client registration**](../../configure-client-registration.md). Allow simple applications, turn on Dynamic Client Registration, choose the allowed application types, and add, edit, or delete a client registration provider.
* [**Configure OpenTelemetry tracing and logs**](../../configure-opentelemetry-tracing-and-logs.md). Configure the Gateway to export trace data, the Management API to read it, and an OpenTelemetry Collector between them.
* [**Save observability dashboards with the Gamma API**](../../save-observability-dashboards.md). List, create, read, update, and delete the dashboards of an environment over the Gamma API.
* [**Configure OpenAPI viewer**](../../configure-openapi-viewer.md). Choose which viewer the Gamma console and Developer Portal use to render OpenAPI specifications.

The environment audit trail is covered on [Review organization and environment audit logs](../../review-audit-logs.md). The OpenTelemetry pipeline, the dashboards API, and the OpenAPI viewer have no sidebar item and are listed here because they configure the environment.
