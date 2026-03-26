---
description: Overview of Visual Studio Code.
noIndex: true
---

# Visual Studio Code

Blackbird integrates with Visual Studio Code (VS Code) to enhance your development workflow by providing API, mock, and deployment management capabilities in your editor. The Hosted Dev Environment with Blackbird extension provides a streamlined experience for managing resources, interacting with APIs, and monitoring your organization’s subscription status.

Key features include:

* **Tree view** – View and manage your Blackbird APIs, mock instances, and deployments directly in VS Code using a dedicated side panel. If you're not logged in, the panel prompts you to authenticate with your Blackbird account.
* **Commands** – Use a set of built-in commands to manage your resources. You can log in or out of your account, create, update, delete, or review APIs and mocks, and refresh the tree view. You can also open resources in your browser or switch between organizations. For more information, see [Using commands with the VS Code integration](visual-studio-code.md#using-commands-with-the-vs-code-integration).
* **File watcher** – Automatically detect OpenAPI files (`.yaml`, `.yml`, `.json`) and update the extension's context so your modifications are immediately reflected.
* **Status bar** – Display your current organization and subscription details, including status, plan, and expiration. If your subscription is inactive, the extension alerts you and provides a link to renew or upgrade.
* **CLI integration** – Automatically detect the Blackbird CLI and set the extension context accordingly.
* **Chat integration** – If you installed GitHub Copilot Chat, the extension integrates with it to offer interactive assistance for API-related tasks.

## Prerequisites

Before configuring the VS Code integration, ensure you meet the following requirement:

* You're using a VS Code version that's 1.96.2 or higher.

> **Note:** The extension also requires the Blackbird CLI with a version of 1.13.0 or higher. If you haven't installed the Blackbird CLI, the extension will automatically install the latest version for you.

## Installing the VS Code extension

After you meet the prerequisites, use the following procedure to install the integration.

**To install the VS Code extension:**

1. Navigate to the Hosted Dev Environment with Blackbird in the Visual Studio Marketplace.
2. Choose **Install**. The extension detects whether you have the Blackbird CLI installed.
3.  If you don't have the Blackbird CLI installed, the extension will automatically install it:

    * **Linux (amd64 and arm64) and MacOS (amd64 and arm64)** – The extension automatically installs the Blackbird CLI and configures your environment accordingly.
    * **Windows (amd64)** – The extension automatically downloads and starts the CLI installer if you're running as an administrator. If not, it prompts you to elevate permissions. After it's installed, the extension configures your environment accordingly.

    > **Note:** The Blackbird CLI doesn't support Windows ARM64. If you have trouble installing the CLI using the extension, you can manually install it and add it to your system's PATH environment variable. For more information, see [#getting-started-with-the-blackbird-cli](../blackbird-cli/#getting-started-with-the-blackbird-cli "mention").

## Using commands with the VS Code integration

Use the following commands to manage and monitor your resources.

| **Category**   | **Command**           | **Description**                                     |
| -------------- | --------------------- | --------------------------------------------------- |
| Authentication | `Login to Blackbird`  | Log into your Blackbird account.                    |
|                | `Logout of Blackbird` | Log out of your Blackbird account.                  |
| APIs           | `Create`              | Create and upload a new API in Blackbird.           |
|                | `Update`              | Update an existing API.                             |
|                | `Delete`              | Delete an API.                                      |
|                | `Review`              | Review an API (requires GitHub Copilot Chat).       |
| Mocks          | `Create`              | Create a new mock deployment.                       |
|                | `Update`              | Update an existing mock deployment.                 |
|                | `Copy Mock URL`       | Copy the URL of a mock deployment.                  |
|                | `Delete`              | Delete a mock deployment.                           |
| General        | `Open in Browser`     | Open the selected resource in your default browser. |
|                | `Switch Organization` | Switch between organizations in Blackbird.          |
|                | `Refresh`             | Refresh the tree view to fetch the latest data.     |
