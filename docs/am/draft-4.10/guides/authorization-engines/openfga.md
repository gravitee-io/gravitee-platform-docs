# OpenFGA

{% hint style="warning" %}
Preview Feature: The OpenFGA Authorization Engine is currently in preview. Features and APIs may change in future releases. This functionality is not production-ready and should be used with caution.
{% endhint %}

{% hint style="info" %}
The plugin is only available in the Enterprise Edition (EE) of Gravitee.
{% endhint %}

## Overview

The OpenFGA Authorization Engine plugin integrates OpenFGA with Gravitee Access Management to provide fine-grained, relationship-based access control (ReBAC) in AM.

Once configured, the plugin establishes a connection to an OpenFGA server and allows Gravitee AM to do the following:

- Control access to MCP Servers based on user–resource relationships.
- Define complex authorization models using OpenFGA’s DSL.
- Manage permissions through relationship tuples.
- Perform manual permission checks directly in the AM Console.
- Enable runtime authorization checks via the Gateway using the AuthZen handler.

## Prerequisites

- Gravitee Access Management **4.10.0+**.
- Valid Gravitee Enterprise license with `enterprise-authorization-engine` pack.
- OpenFGA server instance with store and authorization model defined.
- Admin AM user with permissions:
  - `DOMAIN_AUTHORIZATION_ENGINE[CREATE]`
  - `DOMAIN_AUTHORIZATION_ENGINE[UPDATE]`

## Create an OpenFGA plugin instance

{% hint style="info" %}
Only one Authorization Engine plugin can be created per domain.
{% endhint %}

To create a new instance:

1. Navigate to **Authorization** in the AM Console.
2. Select **OpenFGA** and configure the connection settings. See **Configuration fields** and **Supported authentication types** for more information.
3. Click **Create** to validate the configuration and set up a new OpenFGA connection.

### Configuration fields

| Field                 | Required   | Description                                           |
| --------------------- | ---------- | ----------------------------------------------------- |
| **Name**              | Yes        | Name of the plugin instance.                         |
| **Server URL**        | Yes        | Base URL of your OpenFGA server.                     |
| **Store ID**          | Yes        | OpenFGA store identifier (must already exist).       |
| **Authorization Model ID** | No   | Specific authorization model ID to use (optional).   |
| **API Token**         | Conditional | Required when using API Token authentication.       |
| **Token Issuer**      | Conditional | OAuth2 issuer, required when using OAuth.          |
| **API Audience**      | Conditional | OAuth2 audience, required when using OAuth.        |
| **Client ID**         | Conditional | OAuth2 Client ID, required when using OAuth.       |
| **Client Secret**     | Conditional | OAuth2 Client Secret, required when using OAuth.   |

### Supported authentication types

- **No auth:** Not recommended for production environments.
- **API Token:** Uses a Bearer token for authorization.
- **OAuth2:** Uses OAuth2 client credentials to request tokens.
  - Requires: **Token Issuer**, **API Audience**, **Client ID**, **Client Secret**.

## Configure an OpenFGA plugin instance

You can configure an OpenFGA plugin instance via the AM Console after it is created. For example, you can update connection settings, authentication method, or model identifiers.

### Authorization Models

An Authorization Model uses OpenFGA's DSL to define:

- Object types.
- Relationships.
- Permission rules.

From the **Authorization Model** tab in the AM Console, you can do the following:

- Select an Authorization Model from the latest 50 models available in the OpenFGA store.
- Update the Authorization Model.
- View a dynamic visualization of the model.

#### Example configuration block

```text
type user

type tool {
  relation can_use: user
}
```

Where:

- `user`: User in the system.
- `can_use`: The permission the MCP Server or application will request.

### Relationship tuples

Tuples represent actual instances of relationships. For example, "user X is admin of server Y."

From the **Relationship Tuples** tab in the AM Console, you can perform the following actions to manage user and group permissions:

- Add new tuples.
- View all active tuples.
- Remove tuples.

#### Example configuration block

```text
user:alice can_use tool:get_weather
```

In this example, user `alice` has rights to use the MCP Server tool `get_weather`.

### Test permissions

The **Test Permissions** tab lets you manually verify authorization decisions.

To run a check, provide the following:

- **User**
- **Relation**
- **Object**

AM evaluates the request through OpenFGA and returns **allow** or **deny**.

### Configuration

The **Configuration** tab lets you update the plugin’s connection settings. For example, you can change credentials, the server URL, or the authentication type.

## Resources

- [OpenFGA documentation](https://openfga.dev/docs).