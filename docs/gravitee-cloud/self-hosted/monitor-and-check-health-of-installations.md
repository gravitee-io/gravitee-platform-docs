---
description: Overview of Monitor.
---

# Monitor and check health of installations

## Introduction

Installations that are registered with Gravitee Cloud (GC) will report valuable information, including configuration of the installation, list of nodes, plugins, and also some regular updates regarding their health status.

### Nodes

Installations are monitored at node level. The first REST API node connected when you registered the installation acts as the **primary node**. The role of the primary node is to gather, consolidate, and share the information from the other registered nodes, including:

* status
* name
* version
* sharding tags
* JDK version
* list of plugins
* health checks

If the primary node goes down, another REST API node takes over as primary node. If no REST API nodes are left, after 5 minutes all nodes are considered unhealthy, since GC is no longer able to retrieve health information from the installation.

Nodes can be in a `STARTED` or `STOPPED` state.

You can view all the nodes of an installation which are in a `STARTED` state in the Dashboard, with a color indicating the state of their health. You can click on a node to access more details about that node, including general details about the node (for example, name and version), the list of plugins.

### Health checks

Health check data is gathered every 5 seconds. A node is considered unhealthy if its last health check was unhealthy, or if the last health check was more than five minutes ago.
