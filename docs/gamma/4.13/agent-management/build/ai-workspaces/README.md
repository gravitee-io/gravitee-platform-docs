---
hidden: false
noIndex: false
description: Give a team governed access to a chosen set of AI models, with a per-member spending budget and a separate API key for every member. Choose the AI Workspace task you want to start with.
---

# AI Workspaces

An AI Workspace gives a team governed access to a chosen set of AI models. You pick the models the workspace exposes, set the budget its members spend against, and add the users who consume it. Every member gets their own API key for the workspace and is metered individually against the budget you assign them. Gravitee creates an application for a member when it needs one, and reuses one they already hold for workspace access.

The workspace owns one Default LLM Proxy. Gravitee creates it when you add the first model, exposes it on the gateway path of the workspace, and routes it only to the models the workspace holds. The credentials for the upstream providers are held on the workspace, and members authenticate with their own API key instead.

* [**Create an AI workspace**](../create-an-ai-workspace.md). Name the workspace, derive its gateway path, and set the default budget its members start on.
* [**Add models to an AI workspace**](../add-models-to-an-ai-workspace.md). Add catalog models to the workspace, and control which models its members can call.
* [**Manage AI workspace budgets**](../manage-ai-workspace-budgets.md). Cap what each member spends per period, and optionally cap how fast they send requests.
* [**Assign users to an AI workspace**](../assign-users-to-an-ai-workspace.md). Add members, give each one an API key, change the budget they're metered against, and review their usage.

## Set up a workspace

The **Overview** page of a workspace carries a checklist that follows the order these guides use:

1. **Add a model.** Until the workspace holds a model, it has no Default LLM Proxy and no gateway path to call.
2. **Create a budget.** Budgets define the spend ceiling and the rate limits members are metered against. Every workspace already has one budget named `Default`, created with the workspace, so the checklist counts this step as done as soon as the workspace exists. Add more budgets when different members need different ceilings.
3. **Add a user.** Members get their own API key and are metered against the budget you assign them.

The same page shows a **Workspace snapshot** with the member, budget, and asset counts, and a **Details** card carrying the version, owner, context path, creation date, and last update. Once the workspace has a gateway path, a **Connection** card carries the entrypoint URL to give members.
