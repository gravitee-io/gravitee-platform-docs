---
description: This article walks through how to upgrade your Alert engine instance(s)
---

# Upgrade guide

## Upgrade to 2.0.0

Moving from 1.6.x to 2.0.0 should run smoothly, as only internals have changed.

Major changes:

* Rework of Alert Engine internals for better performance
* **Rolling updates are not supported by this version,** even if Hazelcast v5 (previously v4) ensures a rolling upgrade of its cluster nodes. **Blue/Green deployment** is recommended.

## Upgrade to 1.3.0

{% hint style="info" %}
**Please be aware**

AE v1.3.0 cannot run alongside a v1.2.x version. **Rolling updates are not supported by this version**.
{% endhint %}

Major changes:

* Upgrade to Hazelcast v4 (previously v3). Hazelcast V4 brings a lot of improvements and better stability when running on Kubernetes cluster.

## Deployment strategy

Since the upgrade to Hazelcast v4, AE v1.3.0 can no longer communicate with previous versions. Therefore it is not possible to upgrade AE using a rolling update strategy.

For version 1.3.0, we recommend opting for a **Blue/Green deployment** instead of a rolling update strategy, so you can switch all of your traffic when ready.

Be aware that you may lose some alerts during the upgrade, as all counters will be reset. This mostly depends on the duration of aggregated periods configured on the alerts (the longer the period, the more likely the loss of alerts is).

\
