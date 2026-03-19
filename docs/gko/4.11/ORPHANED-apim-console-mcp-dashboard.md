# Creating an MCP Dashboard

To create an MCP dashboard:

1. Navigate to the dashboard template selection modal in the APIM Console.
2. Select the **MCP** template. The template is labeled with `Focus: MCP` and `Theme: AI`.

When you instantiate the template, the system creates 12 pre-configured widgets. Each widget receives a unique ID generated via `crypto.randomUUID()`. The dashboard includes:

* Request volume stats
* Latency percentiles: average, max, P90, P99
* Method usage distribution
* Top-5 rankings for resources, prompts, and tools

All widgets query HTTP-based metrics filtered to MCP APIs and faceted by MCP proxy dimensions.
