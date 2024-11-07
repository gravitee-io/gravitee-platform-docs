# API storage and control options

## Overview

GKO provides a number of configuration options that determine how GKO stores and controls the APIs that it manage it. Also, the Gravitee Gateway provides an option to configure how the gateway loads those APIs.

* The Gravitee Gateway can load API definitions and their deployment events (start/stop) either from a central repository (e.g. APIM's MongoDB database) or from Kubernetes ConfigMaps local to the cluster, or both.
* GKO can be configured to create API definitions and their deployment events (start/stop) either centrally in the APIM repository, or locally in ConfigMaps.
  * When ConfigMaps are used to create APIs and manage their deployment events, GKO can still optionally push APIs to the Gravitee API Management Console, in order provide a central view of all APIs in the system, and to manage publication of APIs to the developer portal

The most common setup, which is aligned with the proposed [Example Architecture](../../overview/example-architecture.md), uses the following configuration:

* The Gravitee Gateway loads APIs and detects deployment events from the APIM central repository
* GKO synchronizes API definitions it manages with APIM, including deployment events
