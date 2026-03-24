# MCP Dashboard Template Reference

## Widget Types

Four widget types support MCP dashboard visualizations:

* **time-series-line**: Line chart for displaying data over time
* **time-series-bar**: Stacked bar chart for displaying data over time
* **vertical-bar**: Vertical bar chart for displaying comparative data across categories
* **horizontal-bar**: Horizontal bar chart for displaying comparative data across categories

These widget types replace the legacy `line` and `bar` types. Time-series widgets (`time-series-line`, `time-series-bar`) are rendered by `TimeSeriesChartComponent`. Categorical widgets (`vertical-bar`, `horizontal-bar`) are rendered by `CategoryChartComponent`.


## Gateway Configuration

{% hint style="info" %}
For gateway configuration details, see [MCP Dashboard Overview](mcp-dashboard-overview.md#gateway-configuration).
{% endhint %}



