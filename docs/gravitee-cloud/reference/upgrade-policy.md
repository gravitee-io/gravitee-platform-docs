# Upgrade policy

{% hint style="warning" %}
The upgrade policy applies to only Gravitee-managed Gateway installations. If you use a self-hosted profile, you must perform the upgrades. For more information about uograding a self-hosted profile, see [Broken link](broken-reference "mention").
{% endhint %}

This section describes Gravitee’s upgrade process for components in Gravitee Cloud.

* **Upgrades of new APIM Control Plane feature version**: Upgrades happen every quarter. We will communicate upgrades 14 days prior to the upgrade.&#x20;
* **Upgrades of new APIM Cloud Gateways version:** You can voluntarily upgrade the Control Plane up to 30 days after a Control Plane upgrade. After 30 days, the Control Plane automatically upgrades.
* **Upgrades of new APIM Hybrid Gateways version:** You are notified that the APIM Control Plane has been upgraded, but you are expected to upgrade your hybrid gateways yourself.
* **Upgrade of APIM maintenance and patch versions**: These upgrades happen continuously and without an announcement, which ensures that big fixes and vulnerability fixes are rolled out immediately.
* **Irregular upgrades of infrastructure and dependencies**: If there is a risk of downtime, these upgrades are announced 30 days prior to the upgrade. If there is no risk of downtime, these upgrades happen automatically.
