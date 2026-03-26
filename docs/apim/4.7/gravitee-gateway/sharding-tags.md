---
description: An overview about sharding tags.
---

# Sharding Tags

## Overview

Sharding tags allow you to “tag” Gateways with a keyword and deploy an API to a Gateway with a certain tag. You can apply sharding on APIM Gateway instances either at the system property level or with `gravitee.yml`.

Gateways can be tagged with one or more sharding tags. Additionally, the `!` symbol can be placed before the tag name to specify exclusion rules.

To learn more about how to deploy APIs to specific Gateways based on sharding tags, refer to [Configure Deployments](../configure-v2-apis/proxy-settings.md).

## Tagged Gateway/API behavior

API deployment is impacted by how tags are applied to APIs and Gateways.

### Rules

* Tagged Gateway instances will never deploy tagless APIs.
* Tagless Gateway instances will deploy every API, regardless of how the APIs are tagged.
* An API defined with a specific tag will only be deployed on a Gateway that has been assigned that tag.

### Examples

* A tagless API will not be deployed on a Gateway tagged with `x`.
* An API tagged with `x` will be deployed on a tagless Gateway.
* A tagless API will be deployed on a tagless Gateway.
* An API defined with tag `x` will be deployed on a Gateway that has been assigned tag `x`.
* An API defined with tag `x` will be deployed on a Gateway that has been assigned tag `!y`. The tag `!y` means that the Gateway has been assigned every tag but `y`.

## Configure sharding tags for your internal and external Gateways

If you have an architecture that includes both DMZ Gateways and internal corporate Gateways, you can tag these Gateways as external-only and internal-only, as shown in the following diagram:

<figure><img src="../.gitbook/assets/Example architecture.png" alt=""><figcaption></figcaption></figure>

Before sharding tags can be defined in your APIM Console, you must modify `gravitee.yaml` to assign a tag to a Gateway. For example:

```
DMZ Gateways: 
tags: ‘external’
```

```
Internal Network Gateways:
tags: ‘internal’
```

You can also exclude Gateways from tags. For example, the following sharding tag definition configures a Gateway to host APIs that are not dedicated to partners:

```
tags: ‘product,store,!partner’
```

Once Gateways have been tagged, these sharding tags must be defined within API Manager.

## Configure sharding tags for your APIs

To configure sharding tags, complete the following steps:

* [#create-a-tag-in-the-apim-console](sharding-tags.md#create-a-tag-in-the-apim-console "mention")
* [#add-sharding-tags-to-your-apis](sharding-tags.md#add-sharding-tags-to-your-apis "mention")
* [#add-the-tag-id-to-gravitee.yml-or-with-environment-variables](sharding-tags.md#add-the-tag-id-to-gravitee.yml-or-with-environment-variables "mention")

### Create a tag in the APIM Console

1.  In the **Dashboard**, click **Organization**.

    <figure><img src="../.gitbook/assets/CF14DEFB-4393-4DDE-917C-BB5F54374E46.jpeg" alt=""><figcaption></figcaption></figure>
2.  In the **Organization** menu, click **Entrypoints & Sharding Tags**.

    <figure><img src="../.gitbook/assets/AFBD5A82-D5A8-40E6-9818-95D0D0D2274D_1_201_a.jpeg" alt=""><figcaption></figcaption></figure>
3.  Navigate to **Sharding Tags**, and then click **+ Add a tag**.

    <figure><img src="../.gitbook/assets/82E766C4-2A59-479A-A23E-1C1C7BE7D308.jpeg" alt=""><figcaption></figcaption></figure>
4. In the **Create a tag** pop-up window, add the following information:
   1. In the **Name** field, add the name of your tag.
   2. (Optional) In the **Description** field, add a description for the tag.
   3.  (Optional) From the **Restricted groups** drop-down menu, select the groups that you want to be able to deploy to this tag.

       <figure><img src="../.gitbook/assets/image (33).png" alt=""><figcaption></figcaption></figure>
5. Click **Ok**. The sharding tag now appears in the list of **Sharding Tags**.

### Add sharding tags to your APIs

1.  From the **Dashboard**, click **APIs**.

    <figure><img src="../.gitbook/assets/A06811E0-DEFB-45E3-8ED9-E2EB2334A0AB.jpeg" alt=""><figcaption></figcaption></figure>
2.  In the **APIs** screen, select the API to which you want to add a sharding tag.

    <figure><img src="../.gitbook/assets/image (34).png" alt=""><figcaption></figcaption></figure>
3.  In the **APIs** menu, click **Deployment**.

    <figure><img src="../.gitbook/assets/88583357-60B3-4FE6-9D0D-8C8FF9FD77A6.jpeg" alt=""><figcaption></figcaption></figure>
4. In the **Deployment** screen, navigate to the **Deployment configuration** section.
5.  From the **Sharding tags** drop-down menu, select the sharding tag that you want to add to the API.

    <figure><img src="../.gitbook/assets/image (35).png" alt=""><figcaption></figcaption></figure>
6.  In the **You have unsaved changes** pop-up, click **Save**.

    <figure><img src="../.gitbook/assets/8D761E18-837A-412F-9F06-5863D7AC4C33.jpeg" alt=""><figcaption></figcaption></figure>

### Add the tag ID to `gravitee.yml` or with environment variables

1. Find the ID for your sharding tag(s). To find the ID of your sharding tag(s), complete the following substeps:
   1. From the **Dashboard**, click **Organization**.
   2. In the **Organization** menu, click **Entrypoints & Sharding Tags**.
   3. Navigate to the **Sharding Tags** section. The ID of your sharding tag is in the **ID** column.
2. Add the ID of your sharding tag(s) to either your `gravitee.yml` file or as environment variables by completing the set of following steps that matches your preference:

{% tabs %}
{% tab title="gravitee.yml" %}
In your `gravitee.yml` file, add the following configuration:

{% code title="gravitee.yml" lineNumbers="true" %}
```yaml
# Sharding tags configuration
# Allows to define inclusion/exclusion sharding tags to only deploy a part of APIs. To exclude just prefix the tag with '!'.
#tags: <tag 1>, <tag 2>, !<tag 3>
```
{% endcode %}

* Uncomment `#tags: <tag 1>, <tag 2>, !<tag 3>`.
* Replace `<tag 1>, <tag 2>, !<tag3>` with a comma-separated list of your sharding tag IDs.
* To exclude a tag from a Gateway configuration, add an exclamation mark (!) before the tag.
{% endtab %}

{% tab title="environment variables" %}
Add the following environment variable:

{% code lineNumbers="true" %}
```bash
gravitee_tags=<tag 1>,<tag 2>,!<tag3>
```
{% endcode %}

* Replace `<tag 1>, <tag 2>, !<tag3>` with a comma-separated list of your sharding tag IDs.
* To exclude a tag from a Gateway configuration, add an exclamation mark (!) before the tag.
{% endtab %}
{% endtabs %}

## Map entrypoints to sharding tags

You can also map different entrypoint URLs to specific sharding tags in the Developer Portal. The Portal displays available entrypoints based on an API's tag(s).

{% hint style="info" %}
The following process applies to both v2 and v4 APIs.
{% endhint %}

For example, to tell Gravitee API Manager to apply the “internal test” tag to all APIs tagged with this entrypoint:

1.  In the **Dashboard**, click **Organization**.

    <figure><img src="../.gitbook/assets/image (36).png" alt=""><figcaption></figcaption></figure>
2.  In the **Organization** menu, click **Entrypoints & Sharding Tags**.

    <figure><img src="../.gitbook/assets/image (37).png" alt=""><figcaption></figcaption></figure>
3.  Navigate to **Entrypoint Mappings**, and then click **+ Add a mapping**.

    <figure><img src="../.gitbook/assets/5B688A6D-71AD-4FC6-A678-B23475AA56D7_1_201_a.jpeg" alt=""><figcaption></figcaption></figure>
4. From the **+ Add a mapping** drop-down menu, select one of the following entrypoints:
   * HTTP
   * TCP
   * Kafka
5. In the **Create an entrypoint** pop-up window, enter the following information based your entrypoint:

{% tabs %}
{% tab title="HTTP" %}
1) From the **Sharding tags** drop-down menu, select the sharding tags that you want to map to the entrypoint.
2)  In the **Entrypoint url** field, enter your entrypoint URL.

    <div align="left"><figure><img src="../.gitbook/assets/image (38).png" alt="" width="375"><figcaption></figcaption></figure></div>
3) Click **Ok.**
{% endtab %}

{% tab title="TCP" %}
1. From the **Sharding tags** drop-down menu, select the sharding tags that you want to map to this entrypoint.
2.  In the **Default TCP port** field, type the number of your TCP port.

    <div align="left"><figure><img src="../.gitbook/assets/image (39) (1).png" alt="" width="375"><figcaption></figcaption></figure></div>
3. Click **Ok**.
{% endtab %}

{% tab title="Kafka" %}
1. From the **Sharding tags** drop-down menu, select the sharding tags that you want to map to this entrypoint.
2. In the **Default Kafka domain** field, type your Default Kafka domain.
3.  In the **Default Kafka port** field, type your default Kafka port.

    <div align="left"><figure><img src="../.gitbook/assets/image (40) (1).png" alt="" width="375"><figcaption></figcaption></figure></div>
4. Click **Ok**.
{% endtab %}
{% endtabs %}

Your entrypoint mapping is displayed in **Entrypoint Mappings**.

{% hint style="success" %}
You've just learned how to configure sharding tags for your Gravitee API Gateways. To apply sharding tags to APIs to control where those APIs are deployed, refer to [this documentation](../configure-v2-apis/proxy-settings.md).
{% endhint %}

nn
