# Deploy the MCP Dashboard Template

## Deploying the MCP Dashboard

To deploy the pre-built MCP dashboard template:

1. Navigate to **Observability > Dashboards**.
2. Click **Create dashboard > Create from template**.
3. Select the **MCP** template from the left panel.
4. Click **Use template**.

The template creates a 5-column grid with 11 widgets across 5 rows:

* **Row 1:** 5 latency statistics (average, max, P90, P99, total requests)
* **Row 2:** Method usage charts (vertical bar and time-series line)
* **Row 3:** Resource, status, and prompt analysis
* **Rows 4-5:** Tool usage and average response time

Each widget is pre-configured with `API_TYPE=MCP` filters and appropriate facets. Widget IDs are auto-generated during dashboard creation to ensure uniqueness across multiple deployments.

## End-User Configuration

After deploying the dashboard, you can customize the view:

* Adjust the timeframe to focus on specific periods.
* Apply additional filters to narrow results by MCP method, tool, resource, or prompt.
