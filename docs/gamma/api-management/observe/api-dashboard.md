---
hidden: false
noIndex: true
---

# Dashboard and metrics

The Gamma console features a redesigned homepage dashboard that provides a high-level overview of your API management and platform health. It offers per-module metrics, quick actions, and guidance for empty states when you are just getting started.

## Per-module metrics

The dashboard surfaces live metrics across different Gamma modules. For the API Management module, you can view:

* **API Count** — The total number of APIs you have deployed.
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

## Unified filter catalog

Across the Gamma console's observability views (such as the API analytics dashboard and the API log viewer), you can dynamically narrow your data using the unified filter catalog. This catalog provides a consistent set of available filters—such as filtering by time range, subscription plan, consumer application, response status code, or specific error keywords.

Filters are synchronized across widgets on a page; applying a filter to a specific chart or data table updates the entire view to match. The filter dimensions and values are fetched dynamically from the underlying `GET /observability/filters` API to ensure that only relevant values present in the system are offered as filter options.
