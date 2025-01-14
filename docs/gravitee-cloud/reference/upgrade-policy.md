# Upgrade policy

## Upgrade policy

{% hint style="info" %}
The upgrade policy applies only to Gravitee Cloud accounts. If you are running a completely self-hosted Gravitee product, then upgrades are managed entirely by you.
{% endhint %}

* **Upgrades of new APIM Control Plane feature version (minor/major)**: Upgrades happen every quarter. Gravitee communicates upgrades 14 days prior to the upgrade.&#x20;
* **Upgrades of new APIM Cloud Gateways version:** You can choose when to upgrade the Cloud Gateways for each environment up to 30 days after a Control Plane upgrade. This choice allows you to control when the runtime of each environment is upgraded. After 30 days, Gravitee automatically upgrades your Cloud Gateways across all environments to ensure you are running the latest version.
* **Upgrades of new APIM Hybrid Gateways version:** You are notified that the APIM Control Plane has been upgraded, but you are expected to upgrade your hybrid gateways yourself.
* **Upgrade of APIM maintenance and patch versions**: These upgrades happen continuously and without an announcement, which ensures that big fixes and vulnerability fixes are rolled out immediately.
* **Irregular upgrades of infrastructure and dependencies**: If there is a risk of downtime, these upgrades are announced 30 days prior to the upgrade. If there is no risk of downtime, these upgrades happen automatically.
