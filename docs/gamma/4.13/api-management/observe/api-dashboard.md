---
hidden: false
noIndex: false
description: The Gamma homepage dashboard shows per-module metrics, quick actions, and guidance for empty states. Learn what each metric and quick action does.
---

# Dashboard and metrics

The Gamma console features a redesigned homepage dashboard that provides a high-level overview of your API management and platform health. It offers per-module metrics, quick actions, and guidance for empty states when you are just getting started.

## Per-module metrics

The dashboard surfaces live metrics across different Gamma modules. For the API Management module, you can view:

* **API Count** — The HTTP Proxy, TCP Proxy, and federated APIs of the environment, the same APIs the **API Proxies** list shows. Federated APIs count once Federation is turned on and the installation has a valid Enterprise Edition license.
* **Agent Count** — The number of connected AI agents.
* **Application Count** — The number of registered consumer applications.
* **Policy Count** — The number of deployed authorization policies.

Metrics are loaded dynamically and display rounded, compact numbers (e.g., 1.2k) for large datasets.

## Quick actions

If your environment has no APIs or policies yet, the dashboard provides empty states with actionable "Call to Action" buttons to help you get started:

* **Create your first API** — Quickly launch the API creation wizard.
* **Add Integration** — Import a new AI model or integration.
* **Register an application** — Jump directly to the Platform Management application registration form.
* **Create your first policy** — Start configuring an Authorization Management policy.

Once resources are created, the empty states resolve to display your live resource counts.

The **Developer Portals** card opens the Developer Portal settings in a new tab. For more information, see [Open the Developer Portal settings](../../platform-management/open-the-developer-portal-settings.md).

## Filters on the Logs and Dashboards pages

The **Logs** and **Dashboards** pages of a module filter on the properties of its recorded requests, such as **API**, **Plan**, **Application**, and **Status Code**. Some properties apply to logs only, such as **Request URI**. See [View API logs](view-api-logs.md#filter-the-logs).
