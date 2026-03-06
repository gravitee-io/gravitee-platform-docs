### Management Console UI changes

The Management Console UI includes the following changes for agent applications:

#### Application creation wizard

The application creation wizard includes a new "Agentic Application" option with a `memory` icon.

#### Grant Flows configuration page

For agent applications, the Grant Flows configuration page hides the Refresh Token section and filters forbidden grant types from the dropdown menus. The `implicit`, `password`, and `refresh_token` grant types are not available for selection. The `none` token endpoint authentication method is disabled for agent applications.

#### Agent Metadata menu item

A new "Agent Metadata" menu item appears under the "Agent" section for agent applications. This menu item is visible only when the application type is `AGENT` and requires the `application_settings_read` permission.

#### Agent Metadata page

The Agent Metadata page displays the agent card fetched from the configured `agentCardUrl`. The page includes the following states:

* **No URL configured:** Displays an informational message with a link to General settings
* **Loading:** Shows a progress spinner during the fetch operation
* **Error:** Displays an error icon, error message, and a Retry button
* **Loaded:** Renders the agent card summary (name, version, description, provider, icon) and a tabbed interface for capabilities, tools, and raw JSON

The `@a2a-js/sdk` library (version `^0.3.10`) is added as a UI dependency for rendering agent card metadata.

### OpenAPI specification changes

The OpenAPI specification version updates to `4.11.0-SNAPSHOT` and includes the following changes:

#### New enum value

The `ApplicationTypeEnum` includes a new `AGENT` value:

```yaml
ApplicationTypeEnum:
  - WEB
  - NATIVE
  - BROWSER
  - SERVICE
  - RESOURCE_SERVER
  - AGENT
```

#### New endpoint

A new `/agent-card` endpoint is available for fetching agent card metadata:

```http
GET /organizations/{organizationId}/environments/{environmentId}/domains/{domain}/applications/{application}/agent-card
```

**Responses:**

* `200`: Agent card JSON successfully fetched
* `400`: No agentCardUrl configured or invalid URL
* `404`: Application not found
* `500`: Internal server error or upstream failure

#### Schema extensions

The following schemas include a new `agentCardUrl` property:

* `ApplicationAdvancedSettings`
* `NewApplication`
* `PatchApplicationAdvancedSettings`

```yaml
ApplicationAdvancedSettings:
  properties:
    agentCardUrl:
      type: string
```
