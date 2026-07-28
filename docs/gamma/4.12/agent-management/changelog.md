---
description: >-
  Track incremental Agent Management updates as they ship, independent of the
  quarterly Gamma Release Notes.
---

# Changelog

This page lists Agent Management updates as they ship every two weeks. For the quarterly, cross-module summary, see [Gamma Release Notes](../platform-management/gamma-release-notes.md).

***

## 1.1.0 — July 17, 2026

<details>

<summary>Bug Fixes</summary>

* Per-verb API permissions now replace the manage-only access guard, so readers can view resources without manage rights.
* MCP: users with read access can now view proxies without manage rights.
* MCP discovery transport no longer follows redirects.
* LLM Proxy: secret fields now accept Expression Language–compatible values.
* LLM Studio: the save button resets and a deploy banner appears after you save.

</details>

<details>

<summary>Improvements</summary>

* Added Claude Sonnet 5 and Fable 5 to the LLM providers bundle.
* Added Google Vertex AI as an LLM provider, available in the LLM Proxy creation wizard with an editable target field.
* Added upstream credential profiles for MCP and LLM proxies.
* Added a visual workflow builder, a workflow tool wizard and detail pages, and unified the tools catalog with workflow tools.
* Agent identity now resolves Access Management by the connection's organization and environment.

</details>

## 1.0.1 — July 14, 2026

<details>

<summary>Bug Fixes</summary>

* The agent identity wizard now lists all domain identity providers, not only user-store providers.

</details>

## 1.0.0 — June 26, 2026

<details>

<summary>Improvements</summary>

* Initial release of Agent Management: LLM Proxy, MCP servers and proxies, A2A, agent identity, and the tools catalog.

</details>

***
