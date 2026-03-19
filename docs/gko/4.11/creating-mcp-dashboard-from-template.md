# Creating an MCP Dashboard from Template

## Prerequisites

Before creating an MCP dashboard, complete the following steps:

* Configure an Elasticsearch cluster with MCP API analytics data indexed
* Deploy MCP APIs and generate traffic with `additional-metrics` fields populated
* Configure the analytics service to process MCP-specific field mappings

## Creating an MCP Dashboard

To create an MCP dashboard:

1. Navigate to the dashboard creation interface.
2. Select the **MCP** template from the template library. The template is labeled with `Focus: MCP` and `Theme: AI`.
3. The system generates a new dashboard instance with unique widget IDs and applies default settings:
   * Time range: 7 days
   * Interval: 5 minutes for time-series widgets

The MCP dashboard template includes 12 widgets:

* **Latency statistics (5 widgets):** Average latency, max latency, P90 latency, P95 latency, P99 latency
* **Method usage (2 widgets):** Vertical bar chart showing method distribution, time-series line chart showing method usage over time
* **Top resources:** Vertical bar chart displaying the top 5 most-used resources
* **Top prompts:** Vertical bar chart displaying the top 5 most-used prompts
* **Top tools:** Vertical bar chart displaying the top 5 most-used tools
* **Response status distribution:** Doughnut chart showing response status breakdown
* **Average response time:** Time-series line chart showing average response time over time

All widgets filter on `API_TYPE = MCP`. Customize widget filters, time ranges, or metrics as needed.
