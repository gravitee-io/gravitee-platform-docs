# Promote APIs

Overview

The following sections describe how to promote an API from one environment to another. This feature requires that your installation is linked to Gravitee Cloud.

{% hint style="warning" %}
**Limitations**

* APIs can only be promoted to environments belonging to the same organization.
* **One process at a time:** Only one promotion request can be active for an API on an environment. The request must be accepted or rejected before initiating another promotion.
* **Same organization only:** APIs can only be promoted between environments in the same organization.
{% endhint %}

## Prerequisites&#x20;

Before promoting an API, ensure the following requirements are met:

* The installation is linked to a Gravitee Cloud account. For more information about Gravitee Cloud, see [Getting Started with Gravitee Cloud. ](https://documentation.gravitee.io/gravitee-cloud/getting-started/getting-started-with-gravitee-cloud)
* (Dev, QA, Prod) Multiple environments are configured in your organization. For more information about environments, see [Add Environments.](https://documentation.gravitee.io/gravitee-cloud/guides/add-environments)&#x20;
* An API in the source environment you want to promote
* You have the following required permissions:
  * To request promotion: `API DEFINITION` permission with `UPDATE` action, which is an API-level permission from an API role, on the source environment where the API currently exists.
  * To accept or reject promotion: `ENVIRONMENT API` permission with `CREATE` and `UPDATE` actions, which is an Organisation role, on the target environment where you want to promote the API.

## Promote an API

The following diagram shows an example organization (UK) with multiple environments (Dev, QA, Demo, Prod). Each environment is connected to an APIM installation, which communicates with Gravitee Cloud:

![Map of installations in Cockpit](https://docs.gravitee.io/images/apim/3.x/api-publisher-guide/promote-apis/graviteeio-promote-api-cockpit-graph.png)

### Request a promotion for an API

To request a promotion, you need to have API `DEFINITION` [permissions](https://documentation.gravitee.io/apim/configure-and-manage-the-platform/manage-organizations-and-environments/user-management#permissions). Promotion requests are logged in the [Audit trail](https://documentation.gravitee.io/apim/guides/api-measurement-tracking-and-analytics#the-audit-trail).

1.  From the dashboard, click APIs.&#x20;

    <figure><img src="../../.gitbook/assets/click-apis-promotion.png" alt=""><figcaption></figcaption></figure>
2.  Navigate to the API you want to promote in the APIM Console, and then click the API.

    <figure><img src="../../.gitbook/assets/api-entity-to-promote.png" alt=""><figcaption></figcaption></figure>
3.  From the APIs menu, click **General.**&#x20;

    <figure><img src="../../.gitbook/assets/click-general-from-configuration-tab (1).png" alt=""><figcaption></figcaption></figure>
4.  Click **Promote**.

    <figure><img src="../../.gitbook/assets/click-promote.png" alt=""><figcaption></figcaption></figure>
5.  From the **Promote the API** pop-up menu, select the target environment from the **Environment** dropdown menu.

    <figure><img src="../../.gitbook/assets/target-environment-list.png" alt=""><figcaption></figcaption></figure>
6.  Click **Promote** to submit the request.&#x20;

    <div data-gb-custom-block data-tag="hint" data-style="info" class="hint hint-info"><p>Promoting an API does not transfer member and group information. Accepting the promotion updates the API on the target environment. </p></div>

    <figure><img src="../../.gitbook/assets/click-promote-api.png" alt=""><figcaption></figcaption></figure>

### Verification&#x20;

The promotion request is logged in the Audit trail and sent to administrators of the target environment.

<figure><img src="../../.gitbook/assets/audit-trail-promote-api.png" alt=""><figcaption></figcaption></figure>

### Accept or reject a promotion

Users with environment `API` [permissions](https://documentation.gravitee.io/apim/configure-and-manage-the-platform/manage-organizations-and-environments/user-management#permissions) in the target environment can accept or reject promotion requests.

1.  Log in to the APIM Console in the **target environment.**&#x20;

    <figure><img src="../../.gitbook/assets/apim-development.png" alt=""><figcaption></figcaption></figure>
2.  Navigate to Tasks.

    <figure><img src="../../.gitbook/assets/navigate-to-tasks.png" alt=""><figcaption></figcaption></figure>
3.  View the pending promotion requests.

    <figure><img src="../../.gitbook/assets/review-pending-promotion-request.png" alt=""><figcaption></figcaption></figure>
4. Accept or reject the promotion by completing the following steps:&#x20;

{% tabs %}
{% tab title="Accept the Promotion" %}
1)  Click **Accept** to approve the promotion<br>

    <figure><img src="../../.gitbook/assets/image (172).png" alt=""><figcaption></figcaption></figure>
2)  The API is created in the target environment, and the task is removed from the list.<br>

    <figure><img src="../../.gitbook/assets/image (173).png" alt=""><figcaption></figcaption></figure>


{% endtab %}

{% tab title="Reject the Promotion" %}
1.  Click Reject to discard the promotion request.

    <figure><img src="../../.gitbook/assets/image (174).png" alt=""><figcaption></figcaption></figure>
2.  The task is removed from the list.<br>

    <figure><img src="../../.gitbook/assets/no-task-to-display.png" alt=""><figcaption></figcaption></figure>
{% endtab %}
{% endtabs %}

## Verification&#x20;

{% tabs %}
{% tab title="Accepted Promotions" %}
The API appears in the target environment's API list.

<figure><img src="../../.gitbook/assets/api-in-target-environment (1).png" alt=""><figcaption></figcaption></figure>
{% endtab %}

{% tab title="Rejected Promotions" %}
The promotion request is removed from the Tasks list.

<figure><img src="../../.gitbook/assets/complete-removed-from-task-list.png" alt=""><figcaption></figcaption></figure>
{% endtab %}
{% endtabs %}

