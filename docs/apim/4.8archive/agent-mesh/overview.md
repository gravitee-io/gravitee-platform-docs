# Overview

Gravitee Agent Mesh is a suite of features to enable, govern, and protect AI use cases. Agent Mesh collectively refers to the Gravitee Agent Gateway, Gravitee Agent Catalog, and Gravitee Agent Tool Server.

## Agent Gateway

The Agent Gateway includes the Gravitee A2A Proxy and Gravitee LLM Proxy.&#x20;

### A2A Proxy

An **A2A proxy** is a Gravitee v4 Message API that communicates using the Agent-to-Agent (A2A) protocol. An A2A proxy lets you apply API management principles to the interactions between AI agents. With an A2A proxy, you can add security, policies, plans, and observability to the calls agents make to one another.

When a backend agent serves the Agent Card listing its capabilities, another agent can discover it and send a task request to the A2A proxy. The Gravitee Gateway receives the task request, authenticates it, applies policies, and then forwards it to the backend agent. When the backend agent completes the task, the Gateway sends the response back to the caller.

### LLM Proxy

Gravitee's **LLM Proxy** provides a layer of abstraction between AI agents and LLMs. It sits on top of LLM models and applies policies that enforce compliance and cost control. For example, Prompt Guard Rails and Token Tracking.

## Agent Catalog

The **Agent Catalog** is a centralized catalog of all the AI agents built across your organization. If an agent is compliant with the A2A protocol, Gravitee can discover its A2A agent card and add it to your APIM Console's Agent Catalog. You can browse the catalog to find information on agents, such as who owns an agent, where it runs, and what it does.

## Agent Tool Server

With Gravitee Agent Tool Server, you can convert v4 proxy APIs to MCP Tools and expose them.

Gravitee can convert any v4 proxy API running on the Gravitee Gateway into an MCP (Model Context Protocol) server for easy consumption by AI agents. With MCP enabled, v4 proxy APIs can communicate using a single standardized interface.

AI agents use the MCP protocol to discover and invoke an API's available methods, or tools. To expose the MCP protocol to consuming AI agents, an MCP entrypoint is added to an existing v4 proxy API. Next, the MCP entrypoint is enabled, and the API's OpenAPI definition is used to generate the MCP server. Each operation in the OpenAPI spec is converted into an MCP tool definition that an agent can understand.
