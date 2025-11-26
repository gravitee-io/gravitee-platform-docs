---
description: Examples and code samples for Example Architecture.
---

# Example Architecture

The Gravitee Kubernetes Operator (GKO) is commonly used as one piece of a broader API platform that includes components such as a central Gravitee control plane, one or more Gravitee data planes, a GitOps tool like ArgoCD, and a version control system.

The purpose of this platform as a whole is to:

* Onboard new users by allowing them to start creating APIs in the Gravitee Console GUI
* Allow a transition from GUI-based design in development stages to "as-code" APIs for staging and production environments
* Allow a central control plane to drive APIs and Gateways on multiple distributed data planes that could be running on different clouds/platforms/vendors
* Give individual API publisher teams the autonomy to self-serve from the API platform while API governance teams establish guardrails

Below is an illustration of one such platform:

<figure><img src="../.gitbook/assets/image (9).png" alt=""><figcaption></figcaption></figure>

In the approach illustrated above, GKO enables GitOps-style API management by:

* Storing API definitions and other resources in version control
* Using tools like ArgoCD to continuously synchronize the state of what is running on the cluster with the state of APIs in version control

This Git-centric workflow allows changes to APIs to be carefully traced and governed. It also allows you to easily revert the state to a previous version.

GKO can synchronize the states of resources between the Gravitee API Management Console, Developer Portal, and Gateway. This allows governance teams to have a central control plane to view all of their APIs, regardless of where and how they are deployed.

GKO can be deployed in different places depending on your needs. The simplest approach is to have a single GKO running alongside the control plane (or on its own dedicated cluster). In some cases, you may prefer to have one instance of GKO running on each data plane.
