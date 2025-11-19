# Sharding Tags

## Overview

Sharding tags allow you to “tag” Gateways with a keyword and deploy specific APIs to a specific Gateway with a certain tag. You can apply _sharding tags_ on APIM Gateway instances either at the system property level, with Helm `values.yaml` or with `gravitee.yml`.

Gateways can be tagged with one or more sharding tags. Additionally, the `!` symbol can be placed before the tag name to specify exclusion rules.

To learn more about how to deploy APIs to specific Gateways based on sharding tags, refer to [Configure Deployments](../../create-and-configure-apis/configure-v2-apis/proxy-settings.md).

## Tagged Gateway/API behavior

API deployment is impacted by how tags are applied to APIs and Gateways.

### Rules

* Tagged Gateway instances never deploy tagless APIs.
* Tagless Gateway instances retrieve and deploy every API, regardless of how the APIs are tagged.
* An API defined with a specific tag is only deployed on a Gateway that has been assigned that tag.

### Examples

* A tagless API is not be deployed on a Gateway tagged with `x`.
* An API tagged with `x` is deployed on a tagless Gateway.
* A tag-less API will be deployed on a tagless Gateway.
* An API defined with tag `x` is deployed on a Gateway that has been assigned tag `x`.
* An API defined with tag `x` is deployed on a Gateway that has been assigned tag `!y`. The tag `!y` means that the Gateway has been assigned every tag but `y`.

## Configure sharding tags for your internal and external Gateways

If you have an architecture that includes both DMZ Gateways and internal corporate Gateways, you can tag these Gateways as external-only and internal-only, as shown in this diagram:

<figure><img src="../../../4.9/.gitbook/assets/Example architecture (3).png" alt="Example architecture of DMZ Gateways and internal corporate Gateways"><figcaption></figcaption></figure>

Before sharding tags can be defined in your APIM Console, you must define the configuration to assign a tag to a Gateway. For example:

```
DMZ Gateways: 
  tags: 'external'
```

```
Internal Network Gateways:
  tags: 'internal'
```

You can also exclude Gateways from tags. For example, the following sharding tag definition configures a Gateway to host APIs that are not dedicated to partners:

```
  tags: 'product,store,!partner'
```

Once Gateways have been tagged, you must define these sharding tags must within API Manager. To navigate to the **Entrypoint & Sharding Tags**, click **Organization**, and then click **Entrypoint & Sharding Tags**.

## Configure sharding tags for your APIs

To configure sharding tags, complete the following steps:

* [#create-a-tag-in-the-apim-console](sharding-tags.md#create-a-tag-in-the-apim-console "mention")
* [#add-sharding-tags-to-your-apis](sharding-tags.md#add-sharding-tags-to-your-apis "mention")
* [#add-the-tag-id-to-values.yaml-gravitee.yml-or-with-environment-variables](sharding-tags.md#add-the-tag-id-to-values.yaml-gravitee.yml-or-with-environment-variables "mention")

### Create a tag in the APIM Console

1.  In the **Dashboard**, click **Organization**.\\

    <figure><img src="../../../4.8/.gitbook/assets/apim-console-organization (1).png" alt=""><figcaption></figcaption></figure>
2.  In the **Organization** menu, click **Entrypoints & Sharding Tags**.\\

    <figure><img src="../../../4.8/.gitbook/assets/entrypoints-sharding-tags (1).png" alt=""><figcaption></figcaption></figure>
3.  Navigate to **Sharding Tags**, and then click **+ Add a tag**.\\

    <figure><img src="../../../4.8/.gitbook/assets/add-a-sharding-tag (1).png" alt=""><figcaption></figcaption></figure>
4. In the **Create a tag** pop-up window, add the following information:
   1. In the **Name** field, add the name of your tag.
   2. (Optional) In the **Description** field, add a description for the tag.
   3.  (Optional) From the **Restricted groups** drop-down menu, select the groups that you want to be able to deploy to this tag.\\

       <figure><img src="../../../4.8/.gitbook/assets/create-a-tag-pop-up (1).png" alt=""><figcaption></figcaption></figure>
5. Click **Ok**. The sharding tag now appears in the list of **Sharding Tags**.

{% hint style="info" %}
Take note of the generated 'id', as this may differ from your 'name' (due to the use of underscores or hyphens).
{% endhint %}

### Add sharding tags to your APIs

1.  From the **Dashboard**, click **APIs**.\\

    <figure><img src="../../../4.8/.gitbook/assets/click-on-apis (1).png" alt=""><figcaption></figcaption></figure>
2.  In the **APIs** screen, select the API to which you want to add a sharding tag.\\

    <figure><img src="../../../4.8/.gitbook/assets/select-sharding-tag-api (1).png" alt=""><figcaption></figcaption></figure>
3.  In the **APIs** menu, click **Deployment**.\\

    <figure><img src="../../../4.8/.gitbook/assets/select-deployment-in-api (1).png" alt=""><figcaption></figcaption></figure>
4. In the **Deployment** screen, navigate to the **Deployment configuration** section.
5.  From the **Sharding tags** drop-down menu, select the sharding tag that you want to add to the API.\\

    <figure><img src="../../../4.8/.gitbook/assets/sharding-tags-drop-down-menu (1).png" alt=""><figcaption></figcaption></figure>
6.  In the **You have unsaved changes** pop-up, click **Save**.\\

    <figure><img src="../../../4.8/.gitbook/assets/sharding-tag-popup-save-changes (1).png" alt=""><figcaption></figcaption></figure>

### Add the tag ID to `values.yaml`, `gravitee.yml` or with environment variables

1. Find the ID for your sharding tag(s). To find the ID of your sharding tag(s), complete the following substeps:
   1. From the **Dashboard**, click **Organization**.
   2. In the **Organization** menu, click **Entrypoints & Sharding Tags**.
   3. Navigate to the **Sharding Tags** section. The ID of your sharding tag is in the **ID** column.
2. Add the ID of your sharding tag or tags to either your Helm `values.yaml`, `gravitee.yml` file or as environment variables by completing the set of following steps that match your configuration:

{% tabs %}
{% tab title="Helm values.yaml" %}
In your `values.yaml` file, add the following configuration:

{% code title="values.yaml" lineNumbers="true" %}
```yaml
# Sharding tags configuration
# Allows to define inclusion/exclusion sharding tags to only deploy a part of APIs. To exclude just prefix the tag with '!'.
gateway:
  sharding_tags: <tag1>, <tag2>, !<tag3>
```
{% endcode %}

* Replace `<tag1>, <tag2>, !<tag3>` with a comma-separated list of your sharding tag IDs.
* To exclude a tag from a Gateway configuration, add an exclamation mark (!) before the tag.
{% endtab %}

{% tab title="gravitee.yml" %}
In your `gravitee.yml` file, add the following configuration:

{% code title="gravitee.yml" lineNumbers="true" %}
```yaml
# Sharding tags configuration
# Allows to define inclusion/exclusion sharding tags to only deploy a part of APIs. To exclude just prefix the tag with '!'.
#tags: <tag1>, <tag2>, !<tag3>
```
{% endcode %}

* Uncomment `#tags: <tag1>, <tag2>, !<tag3>`.
* Replace `<tag1>, <tag2>, !<tag3>` with a comma-separated list of your sharding tag IDs.
* To exclude a tag from a Gateway configuration, add an exclamation mark (!) before the tag.
{% endtab %}

{% tab title="Environment variables" %}
Add the following environment variable:

{% code lineNumbers="true" %}
```bash
gravitee_tags=<tag1>,<tag2>,!<tag3>
```
{% endcode %}

* Replace `<tag1>, <tag2>, !<tag3>` with a comma-separated list of your sharding tag IDs.
* To exclude a tag from a Gateway configuration, add an exclamation mark (!) before the tag.
{% endtab %}

{% tab title="Docker Compose" %}
In your `docker-compose.yml` file, add the following _environment variable_ configuration:

{% code title="docker-compose.yml" lineNumbers="true" %}
```yaml
# Sharding tags configuration
# Allows to define inclusion/exclusion sharding tags to only deploy a part of APIs. To exclude just prefix the tag with '!'.
gateway:
  environment:
    - gravitee_tags=<tag1>, <tag2>, !<tag3>
```
{% endcode %}

* Replace `<tag1>, <tag2>, !<tag3>` with a comma-separated list of your sharding tag IDs.
* To exclude a tag from a Gateway configuration, add an exclamation mark (!) before the tag.
{% endtab %}
{% endtabs %}

## Map entrypoints to sharding tags

You can also map different entrypoint URLs to specific sharding tags (for auto-generating the display of full URLS in the Developer Portal. The Portal displays available entrypoints based on an API's tag(s).

For example, to configure Gravitee API Manager to apply the “internal test” tag to all APIs tagged with this entrypoint:

1.  In the **Dashboard**, click **Organization**.\\

    <figure><img src="../../../4.8/.gitbook/assets/apim-console-organization (1).png" alt=""><figcaption></figcaption></figure>
2.  In the **Organization** menu, click **Entrypoints & Sharding Tags**.\\

    <figure><img src="../../../4.8/.gitbook/assets/entrypoints-sharding-tags (1).png" alt=""><figcaption></figcaption></figure>
3.  Navigate to **Entrypoint Mappings**, and then click **+ Add a mapping**. \\

    <figure><img src="../../../4.8/.gitbook/assets/entrypoint-mapping (1).png" alt=""><figcaption></figcaption></figure>
4. From the **+ Add a mapping** drop-down menu, select one of the following entrypoints:
   * HTTP
   * TCP
   * Kafka
5. In the **Create an entrypoint** pop-up window, enter the following information based your entrypoint:

{% tabs %}
{% tab title="HTTP" %}
1) From the **Sharding tags** drop-down menu, select the sharding tags that you want to map to the entrypoint.
2)  In the **Entrypoint url** field, enter your entrypoint URL. \\

    <figure><img src="../../.gitbook/assets/image (9).png" alt=""><figcaption></figcaption></figure>
3) Click **Ok.**
{% endtab %}

{% tab title="TCP" %}
1. From the **Sharding tags** drop-down menu, select the sharding tags that you want to map to this entrypoint.
2.  In the **Default TCP port** field, type the number of your TCP port. \\

    <figure><img src="../../.gitbook/assets/image (10).png" alt=""><figcaption></figcaption></figure>
3. Click **Ok**.
{% endtab %}

{% tab title="Kafka" %}
1. From the **Sharding tags** drop-down menu, select the sharding tags that you want to map to this entrypoint.
2. In the **Default Kafka domain** field, type your Default Kafka domain.
3.  In the **Default Kafka port** field, type your default Kafka port. \\

    <figure><img src="../../.gitbook/assets/image (11).png" alt=""><figcaption></figcaption></figure>
4. Click **Ok**.
{% endtab %}
{% endtabs %}

Your entrypoint mapping is displayed in **Entrypoint Mappings**.

{% hint style="success" %}
You've just learned how to configure sharding tags for your Gravitee API Gateways. To apply sharding tags to APIs to control where those APIs are deployed, refer to [this documentation](../../create-and-configure-apis/configure-v2-apis/proxy-settings.md).
{% endhint %}
