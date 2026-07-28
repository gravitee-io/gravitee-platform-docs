---
description: >-
  Track incremental Authorization Management updates as they ship,
  independent of the quarterly Gamma Release Notes.
---

# Changelog

This page lists Authorization Management updates as they ship every two weeks. For the quarterly, cross-module summary, see [Gamma Release Notes](../platform-management/gamma-release-notes.md).

***

## 1.7.0 — July 20, 2026

<details>

<summary>Bug Fixes</summary>

* The Target gateways picker now filters correctly and clears stale queries.
* The schema outline is now a flat entity list.

</details>

## 1.6.1 — July 17, 2026

<details>

<summary>Bug Fixes</summary>

* The parent picker search now filters results.

</details>

## 1.6.0 — July 9, 2026

<details>

<summary>Bug Fixes</summary>

* Access Explorer: principal pickers now use a searchable dropdown; mismatches with no visible row are flagged; runs wait for policies to load and results are sorted; stale runs are ignored and rebuild when inputs change; missing-context engine errors now appear in plain language.
* MCP: whole-server grants stay editable when a server has no tool entities, and no longer unwrap into per-tool permits on edit.
* Policy Simulator: stale runs are ignored, and the full tool id is sent and shown as the verified action.

</details>

<details>

<summary>Improvements</summary>

* Access Explorer now shows everything a principal is permitted to do, with a toggle for raw entity IDs in the decision drawer.

</details>

## 1.4.0 — July 3, 2026

<details>

<summary>Bug Fixes</summary>

* MCP policy authoring: the Visual editor stays reachable while creating policies, bulk create handles duplicates and partial failures, and code-view edits are no longer dropped.

</details>

<details>

<summary>Improvements</summary>

* Bulk-delete policies with search-scoped select-all.
* All-tools MCP policies now collapse to server membership.

</details>

***
