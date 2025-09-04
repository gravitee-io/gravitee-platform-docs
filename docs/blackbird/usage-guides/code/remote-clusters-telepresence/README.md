---
noIndex: true
---

# Remote Clusters (Telepresence)

Using Blackbird clusters (powered by Telepresence), you can locally run and debug your service while seamlessly interacting with the rest of your Kubernetes cluster. It also allows you to intercept traffic to your service, routing requests from the cluster to your local machine as if were running remotely. This allows you and your team to test in real time, iterate quickly, and debug your service without full deployments.

This guide provides information about:

* Features related to clusters, including the Traffic Manager, connect command, and intercept command.
* Advanced configuration options, such as cluster-side and local configurations, how to work with VPNs, and how to configure volume mounts.
* Integrations, such as Prometheus, which you can use for monitoring capabilities.

For detailed information about cluster commands, see _Cluster_ in the [blackbird-cli](../../../technical-reference/blackbird-cli/ "mention") reference.

> **Tip:** If you're a former Telepresence user who's now working in Blackbird, you don't need to immediately update your existing scripts that rely on `telepresence` commands. To maintain compatibility, you can run `alias telepresence='blackbird cluster'` in your terminal. This allows your existing scripts to continue working as expected while you transition to Blackbird.
