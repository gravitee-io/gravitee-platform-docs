---
description: >-
  Track incremental Edge Management updates as they ship, independent of the
  quarterly Gamma Release Notes.
---

# Changelog

This page lists Edge Management updates as they ship every two weeks. For the quarterly, cross-module summary, see [Gamma Release Notes](../platform-management/gamma-release-notes.md).

***

## 1.0.0 — June 26, 2026

<details>

<summary>Bug Fixes</summary>

* Guarded metric values against nulls to prevent reporter errors.
* Set the remote and local address on reported metrics.
* Edge now survives a reactor update through a dedicated acceptor that removes only its own registration.
* Corrected the licensing feature name.

</details>

<details>

<summary>Improvements</summary>

* Initial release of Edge Management: heartbeat, metrics, and shadow-AI reporting endpoints with v4-metrics reporting.
* Serves deployed Edge API configuration from `GET /config`.
* Added a provider field to metrics payloads and to route configuration.
* Added an OS field to the heartbeat payload.

</details>

***
