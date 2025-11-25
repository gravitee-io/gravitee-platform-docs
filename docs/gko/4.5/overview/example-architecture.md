---
description: Examples and code samples for Example.
---

# Example architecture

The Gravitee Kubernetes Operator (GKO) is commonly used as one piece of a broader API platform that includes components such as a central Gravitee control plane, one or more Gravitee data planes, a GitOps tool like ArgoCD, and a version control system.

The purpose of this platform as a whole is:

* to facilitate onboarding of new users by allowing them to start creating APIs in the GraviteeConsole GUI
* to allow a transition from GUI-based design in development stages, to "as-code" APIs for staging and production environments
* to allow for a central control plane to drive APIs and gateways on multiple distributed data planes, that could be running on different clouds / platforms / vendors
* to facilitate the task of giving individual API publisher teams autonomy to self-serve from the API platform, while API governance teams establish guardrails.

Below is an illustration of one such platform:

<figure><img src="../.gitbook/assets/image (9) (1).png" alt=""><figcaption></figcaption></figure>

In the approach illustrated above, GKO is used to enable GitOps-style API management by storing API definitions and other resources in version control, and using tools like ArgoCD to continuously synchronize the state of what is running on the cluster with the state of APIs in version control.

This Git-centric workflow allows for changes to APIs to be carefully traced and governed, and also allows for reverting state to a previous version quite easily.

GKO is also used to synchronize the state of resources with the Gravitee API Management Console, Developer Portal, and Gateway. This allows governance teams to have a central control plane to view all of their APIs, regardless of where and how they are deployed.

GKO can be deployed in different places depending on your needs. The simplest approach is to have a single GKO running alongside the control plane (or on its own dedicated cluster). In some cases, you may prefer to have one instance of GKO running on each data pane.
