---
description: An overview about shared policy groups overview.
---

# Shared policy groups overview

With shared policy groups, you can define a collection of policies in a central location and use them across multiple APIs. Also, you can complete the following actions:

* Define a standard set of policies to shape traffic
* Enforce security standards
* Transform messages.

The deployment of a shared policy group to the gateway is independent of the deployment lifecycle of the APIs the shared policy group is used in. If you make a change to the shared policy group, and then deploy it to the gateway, all APIs will pick up the changes when the next connection begins, without requiring the APIs to be restarted. When using this feature at scale, inform your team of any changes you make, and test your changes before deploying to a higher environment.

{% hint style="info" %}
* Shared policy groups only work on the Gravitee v4 API definition.
{% endhint %}
