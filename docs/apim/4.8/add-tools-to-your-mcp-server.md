# Add Tools to your MCP Server

{% include ".gitbook/includes/v4-proxy-only-feature.md" %}

## Prerequisites&#x20;

* A v4 proxy API with the MCP server enabled. For more information about how to convert your API to an MCP server, see [convert-your-apis-to-mcp-servers.md](convert-your-apis-to-mcp-servers.md "mention").
* An OpenAPI specification to generate the MCP tools definition.

## Add tools to your MCP server

1.  From the **Dashboard**, click **APIs**.\


    <figure><img src=".gitbook/assets/3AFC7359-4334-44DE-A2AA-3732BE173718_1_105_c.jpeg" alt=""><figcaption></figcaption></figure>
2.  Find the API that you have converted to an MCP Server. \


    <figure><img src=".gitbook/assets/EFADEF2D-0D48-41A3-9668-C4C2A6F806DA_1_105_c.jpeg" alt=""><figcaption></figcaption></figure>
3.  Click **Entrypoints**.\


    <figure><img src=".gitbook/assets/35CF5451-4B63-46D3-B173-BEBBB47EAC95_1_105_c.jpeg" alt=""><figcaption></figcaption></figure>
4.  In the **Entrypoints** screen, click **MCP Entrypoint**. \


    <figure><img src=".gitbook/assets/99414568-4C10-4A53-B2F0-757C10D6EDC2_1_201_a.jpeg" alt=""><figcaption></figcaption></figure>
5.  Click **+Generate Tools from OpenAPI**.\


    <figure><img src=".gitbook/assets/2AA002A5-4D84-419D-8340-7600F9A9C5CD_1_201_a.jpeg" alt=""><figcaption></figcaption></figure>
6.  In the **Generate Tools from OpenAPI** pop-up window, add your OpenAPI specification.\


    <figure><img src=".gitbook/assets/C99740F9-79DA-45B6-859A-489774F0A88D_1_201_a (1).jpeg" alt=""><figcaption></figcaption></figure>
7. Click **Regenerate Tools**. The tool appears in the **Tool Definitions** section.&#x20;
8.  Click **Save**.\


    <figure><img src=".gitbook/assets/9FA889B6-E292-4A4D-8F19-909B768884D4_1_201_a (1).jpeg" alt=""><figcaption></figcaption></figure>
9.  Click **Deploy API**.\


    <figure><img src=".gitbook/assets/224D0D10-7DB5-4E7A-8F4C-2D234259C2E2_1_201_a.jpeg" alt=""><figcaption></figcaption></figure>
10. (Optional) In the **Deploy your API** pop-up window, add a deployment label.
11. In the **Deploy your API** pop-up window, click **Deploy**.\


    <figure><img src=".gitbook/assets/image (261).png" alt=""><figcaption></figcaption></figure>

## Verification&#x20;

The Tool Definition appears in the **Tool Definition** section of the **MCP Entrypoint** screen.

<figure><img src=".gitbook/assets/9FA889B6-E292-4A4D-8F19-909B768884D4_1_201_a (2).jpeg" alt=""><figcaption></figcaption></figure>
