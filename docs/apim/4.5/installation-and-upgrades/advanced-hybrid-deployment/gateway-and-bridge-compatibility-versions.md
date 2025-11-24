---
description: Conceptual explanation of gateway and bridge compatibility versions.
---

# Gateway and Bridge compatibility versions

The Gateway version that you use for your Hybrid deployment and the Bridge version that you use for your Hybrid deployment must be compatible. The control plane signifies the Bridge and the data-plane signifies the Gateway.

The following tables explain which versions of the Gateway and the Bridge are compatible for a Hybrid deployment:

| Control-Plane version | Supported Data-Plane versions |
| --------------------- | ----------------------------- |
| 4.2.x                 | 4.2.x                         |
| 4.3.x                 | 4.2.x to 4.3.x                |
| 4.4.x                 | 4.2.x to 4.4.x                |
| 4.5.x                 | 4.2.x to 4.5.x                |

The following table lists the Control-Plane (Bridge) versions supported by each Data-Plane (Gateway) version.

| Data-Plane version | Supported Control-Plane versions |
| ------------------ | -------------------------------- |
| 4.2.x              | 4.2.x to 4.5.x                   |
| 4.3.x              | 4.3.x to 4.5.x                   |
| 4.4.x              | 4.4.x to 4.5.x                   |
| 4.5.x              | 4.5.x                            |
