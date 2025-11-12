# API storage and control options

## Overview

How GKO stores and controls the APIs that it manages is configurable. GKO can be configured to create API definitions and their deployment events (start/stop) either centrally in the APIM repository or locally in ConfigMaps. When ConfigMaps are used to create APIs and manage their deployment events, GKO can optionally still push APIs to the Gravitee APIM Console. This provides a central view of all APIs in the system and manage the publication of APIs to the Developer Portal.

How the Gravitee Gateway loads the APIs managed by GKO is configurable. The Gateway can load API definitions and their deployment events (start/stop) from a central repository (e.g., APIM's MongoDB database), Kubernetes ConfigMaps local to the cluster, or both.

In the most common setup, which is aligned with the proposed [Example Architecture](../../overview/example-architecture.md), the Gravitee Gateway loads APIs and detects deployment events from the APIM central repository, and GKO synchronizes the API definitions it manages with APIM, including deployment events.
