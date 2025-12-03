# Agent Mesh

## Overview

Gravitee Agent Mesh is a suite of features that enable, govern, and protect AI use cases. Agent Mesh collectively refers to the Gravitee Agent Gateway, Gravitee Agent Catalog, and Gravitee Agent Tool Server.

Gravitee offers centralized and unified control of AI agents, even if they are running on multiple platforms. These agents can use Agent-to-Agent (A2A) protocol to interact with one another, and Model Context Protocol (MCP) to access both synchronous and asynchronous APIs. All agent communications are subject to the access control and security measures provided by the Gravitee Gateway.

## Agent Gateway

The Agent Gateway includes the Gravitee A2A Proxy and Gravitee LLM Proxy.

### A2A Proxy

The Agent-to-Agent (A2A) protocol enables dynamic and multimodal peer-to-peer communication between AI agents. By using A2A, agents can collaborate, delegate, and manage shared tasks.

An **A2A proxy** is a Gravitee v4 message API that communicates using A2A, where a client agent creates and transmits tasks that a remote agent processes to provide information or perform actions.

A2A supports the following types of interactions:

* Request/Response, with the option for stateful, long-running tasks
* Server-Sent Events (SSE) streaming for real-time or incremental updates
* Push notifications for extended tasks that render persistent connections impractical

An A2A proxy lets you apply API management principles to the interactions between AI agents. With an A2A proxy, you can add security, policies, plans, and observability to the calls agents make to one another.

When a backend agent serves the Agent Card listing its capabilities, another agent can discover it and send a task request to the A2A proxy. The Gravitee Gateway receives the task request, authenticates it, applies policies, and then forwards it to the backend agent. When the backend agent completes the task, the Gateway sends the response back to the caller.

### LLM Proxy

Gravitee's **LLM Proxy** provides a layer of abstraction between AI agents and LLMs. It sits on top of LLM models and applies governance to enforce compliance and cost control. The following are examples of LLM capabilities:

* Token-based rate limiting via Gravitee's [Prompt Token Tracking](/broken/pages/673c1a8aba3973861937417f549a203aaab96eba) policy.
* Routing to different LLMs.
* Threat protection via Gravitee's [Prompt Guard Rails](/broken/pages/7cb91c284597d976e32075d753569b509ae8b88e) policy.
* Orchestration, such as HTTP calls to obtain data to add to LLM contexts.

## Agent Catalog

The **Agent Catalog** is a centralized catalog of all the AI agents built across your organization. If an agent is compliant with the A2A protocol, Gravitee can discover its A2A agent card and add it to your APIM Console's Agent Catalog.

The Agent Catalog is used for agent discovery, governance, analytics, and cost optimization. You can browse the catalog to find information on agents, such as who owns an agent, where it runs, and what it does.

## Agent Tool Server

The Agent Tool Server integrates with the Developer Portal to discover, explore, and subscribe to Model Context Protocol (MCP) servers. MCP lets AI agents access their capabilities by connecting them to tools, APIs, and resources.

Gravitee can convert any v4 proxy API running on the Gravitee Gateway into an MCP server for easy consumption by AI agents. This includes v4 proxy APIs from 3rd-party gateways and brokers. With MCP enabled, v4 proxy APIs can communicate using a single, standardized interface.

AI agents use MCP to discover and invoke an API's available methods. MCP servers enable AI integration by exposing different capabilities:

* Tools: Specific functions that language models can control and implement on external systems. Tools are APIs, which Gravitee can discover, secure, and monitor.
* Resources: Data sources that can be accessed by language models.
* Prompts: User-defined templates that guide how language models use tools and resources.

To expose MCP to consuming AI agents, an MCP entrypoint is added to an existing v4 proxy API. Next, the MCP entrypoint is enabled, and the API's OpenAPI definition is used to generate the MCP server. Each operation in the OpenAPI spec is converted into an MCP tool definition that an agent can understand. MCP servers use SSE to push messages and events to agents in real-time over a persistent HTTP connection.
