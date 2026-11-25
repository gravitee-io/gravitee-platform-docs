---
hidden: false
noIndex: false
description: Filter, group, and display the values your Assign metrics policy writes as custom.<name> fields in Gamma observability.
---

# Use custom metrics in observability

Custom metrics are the values your APIs write with the **Assign metrics** policy. In Gamma observability each one is a field named `custom.<name>`, where `<name>` is the key you set in the policy. For example, a policy that writes `customer.tier` makes the field `custom.customer.tier` available.

{% hint style="warning" %}
Values your Assign metrics policy writes. They can hold personal data, and anyone who can read analytics can see and filter on them. Do not write secrets or personal data into custom metrics.
{% endhint %}

## What a custom metric is, and is not

* A custom metric is a **text value** attached to a request. Numbers are stored and compared as text.
* It is a **dimension, not a measure**. You can filter, group by, and display it, but you cannot use it as a metric (for example to compute a sum or an average). Gamma refuses it in a metric field and says why.
* Gamma offers it as soon as an API has recorded a value. You do not declare it first. In **Metrics configuration** (Platform › Environment › System & Security), custom rows are read-only.
* Two different keys can end up with the same label: `customer.tier` and `customer-tier` both read "Customer tier". They remain two separate custom metrics, never merged, and the technical name tells them apart.
* Labels are built from the name: `custom.customer.tier` is shown as "Customer tier". The technical name is in the hover tooltip in the pickers, and visible under the label in **Metrics configuration** and in the log detail.
* Custom metrics apply to v4 HTTP APIs (proxy, LLM, MCP, A2A) request logs. Message-level values of message APIs are not covered.

## Filter on a custom metric

1. Open **Logs** (or a dashboard with a filter bar) and select **Add filter**.
2. Under the **Custom** group, pick the field. If it is not listed, type `custom.<name>` in the free key box.
3. Choose an operator, **=** (one value) or **In** (several values), and a value. Custom fields have no exclude operator.

## Group by a custom metric

In a dashboard widget (for example a table or chart), choose the custom field as the **Group by** dimension and pair it with a measure such as latency or request size.

## Show a custom metric as a column

In **Logs**, open **Columns** and add the custom field. Requests without a value show a muted dash.

## See the values on a single request

Open a log entry. The **Custom** section, after **Overview**, lists every custom value of the request. Use **Filter by this value** on a row to add the matching filter.

## Next steps

* [View API logs](view-api-logs.md) — Inspect individual requests and filter the log table.
* [Monitor API usage](monitor-api-usage.md) — View aggregate metrics and dashboards for your API.
