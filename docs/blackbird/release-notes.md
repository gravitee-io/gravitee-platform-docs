---
description: Release notes for Release Notes.
noIndex: true
---

# Release Notes

## July 02, 2025

* **New release note tracking method**\
  Blackbird release notes are now organized by release date rather than version number. We'll continue to include the latest CLI version in our release notes for your reference.
* **Streamline your Blackbird workflow with the Blackbird MCP server**\
  You can now add the Blackbird MCP server to your IDE. This allows you to query Blackbird instances, upload new API specifications, create mock instances, and complete other tasks directly from your preferred AI chatbot.
* **View progress when generating a new API specification**\
  When you generate API specifications based on your code, a progress bar now appears in the lower-right corner of the Blackbird UI. The bar shows both the percentage complete and the current step in the process.
* **Access your project from notification messages**\
  When you generate API specifications based on your code, you can access the related project from the notification bell in the top-right corner by hovering over the “Completed indexing repository” message.
* **Blackbird CLI version 1.14.2 is now available**\
  This Blackbird CLI release includes internal changes that don't affect the functionality for end users.

***

## Version 1.14.1 (June 25, 2025)

* **Define additional GitHub details for API discovery and generation**\
  You can now specify the GitHub owner/organization, repository, and branch when discovering or generating API specifications with Blackbird.
* **View additional project details**\
  The Projects page now includes a job event log that displays real-time updates from the streaming service for in-progress jobs.
* **Access your Blackbird notifications**\
  The Blackbird UI now includes a notification bell in the top-right corner to display real-time status updates across all jobs and system activity.

***

## Version 1.14.0 (June 18, 2025)

* **Manage your MCP deployments using the Blackbird CLI**\
  You can now host and manage third-party MCP servers directly from the Blackbird CLI.
* **Host a third-party MCP server using VS Code**\
  You can now browse the MCP catalog and host a third-party MCP server in Blackbird using Visual Studio Code (VS Code).
* **View your MCP deployments in Blackbird**\
  You can now view your MCP deployments in the Blackbird UI to make it easier to track and manage your servers.
* **Receive notifications when a new version of the VS Code extension is available**\
  The extension now automatically detects the installed CLI version and prompts you to update when a new version is available.

***

## Version 1.13.7 (June 17, 2025)

* **Create projects from your GitHub repositories**\
  You can now create projects based on your GitHub repositories. A project is built from a specific repository and includes one or more API definitions that you choose. Blackbird keeps the imported definitions up to date with changes made in the repository, so your definitions stay current as your APIs evolve. The sync only works one way, so changes made in Blackbird won’t update your GitHub repository.
* **Generate API specifications from your code**\
  You can now scan a GitHub repository for code related to API definitions and generate an OpenAPI specification from it.
* **Explore tutorials using the new Blackbird Demo Center**\
  You can now browse tutorials directly in the Blackbird UI to help you learn about key features and workflows.

***

## Version 1.13.4 (June 05, 2025)

* **Specify a protocol during deployments**\
  You can now specify either TCP or HTTP during deployments to provide more control over service accessibility.

***

## Version 1.13.2 (May 21, 2025)

* **Automatically install the Blackbird CLI with the VS Code extension**\
  The Hosted Dev Environment with Blackbird extension now automatically installs the latest version of the Blackbird CLI if it's not detected on your system.
* **Specify a custom Docker image name during deployments**\
  You can now specify a custom Docker image name when creating a deployment.
* **Specify a port during deployments**\
  You can now specify a port for the container to listen on when creating or updating a deployment.

***

## Version 1.13.1 (May 07, 2025)

* **Enhance your Blackbird workflow with VS Code**\
  You can now manage Blackbird APIs, mock deployments, and subscriptions directly in Visual Studio Code (VS Code) using the new Hosted Dev Environment with Blackbird extension. The extension integrates with the Blackbird CLI and GitHub Copilot Chat.
* **Persistent connections to deployments**\
  You can now maintain persistent connections to Blackbird instance deployments to improve performance.

***

## Version 1.13.0 (May 01, 2025)

* **Connect your Blackbird workflow with Git**\
  You can now analyze your GitHub repositories and automatically import OpenAPI and Swagger definitions into your Blackbird catalog. This integration simplifies how you discover and onboard your APIs.
* **Improved output formatting and resource management**\
  The `--output` flag now supports multiple formats, including JSON, YAML, and table, to provide more control over how command responses are displayed. The `--force` flag now allows you to delete related resources where applicable to streamline cleanup operations.
* **Resolved an issue that caused failed commands on Windows**\
  Fixed an issue where `blackbird cluster` commands would fail on Windows due to a missing dependency. The command now runs reliably across platforms.

***

## Version 1.12.2 (April 15, 2025)

* **Resolved cluster connection stalling issue**\
  Fixed an issue where `blackbird cluster connect` would stall when the current Kubernetes context used `ExecConfig` to fetch credentials.

***

## Version 1.12.1 (March 31, 2025)

* **Resolved daemon crash issue**\
  Fixed an issue where the Blackbird daemon would crash when reconnecting after leaving an intercept.

***

## Version 1.12.0 (March 27, 2025)

* **Blackbird cluster (powered by Telepresence) is now widely available**\
  Non-airgapped customers with the appropriate subscription can now access Blackbird cluster functionality. For information on subscriptions, see [Blackbird Pricing](https://www.getambassador.io/blackbird-pricing).

***

## Version 1.11.1 (March 18, 2025)

* **Connect your Blackbird workflow with Slack**\
  You can now integrate with Slack to streamline your workflow and foster a collaborative environment where everyone is immediately aware of changes to your mocks and deployments in Blackbird. This release also introduces `genyaml` commands for Blackbird cluster (powered by Telepresence) so you can generate YAML configurations for the Traffic Agent.

***

## Version 1.11.x (March 03, 2025)

* **Single sign-on is now available for enterprise customers**\
  Enterprise customers can now integrate SSO to streamline authentication, enhance their user experience, and reduce the risk of unauthorized access.

***

## Version 1.11.0 (February 26, 2025)

* **Blackbird cluster (powered by Telepresence) is now available**\
  Blackbird cluster allows you to locally run and debug your services while seamlessly interacting with the rest of your Kubernetes cluster.

***

## Version 1.0.0 (August 19, 2024)

* **Create and manage mock API instances**\
  You can now create and manage mock API instances in the Blackbird UI and CLI. Simulated API behavior allows for faster testing, parallel development, and improved application quality without relying on live services.
* **Generate server and client code from API specs**\
  You can now generate server and client code directly from your API specifications using OpenAPI Generator. This streamlines development and testing workflows for both frontend and backend teams.
* **Debug API specs and mock instances**\
  You can now debug your API specification or mock instance to test the behavior of your API, analyze request and response data, and troubleshoot issues.
* **Deploy APIs to non-production environments**\
  Blackbird now supports deploying APIs to a dedicated non-production environment. You can test and validate applications without impacting production systems.
