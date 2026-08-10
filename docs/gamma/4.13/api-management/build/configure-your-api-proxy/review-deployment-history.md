---
description: >-
  Compare deployed versions of an API definition and roll back to an earlier
  one.
hidden: false
noIndex: false
---

# Review deployment history

The **Deployment History** page lists all API deployments, newest first. Select two versions to diff them, or use the actions menu to inspect a single version.

To open the page, follow these steps:

1. Click **API Proxies** in the module sidebar.
2. Select your API proxy.
3. Click **Deployment** in the API proxy sidebar.
4. Click **History**.

<!-- TODO: Screenshot of the Deployment History table -->

<figure><img src="../../../.gitbook/assets/PLACEHOLDER-gamma-api-deployment-history.png" alt=""><figcaption><p>The Deployment History page</p></figcaption></figure>

The table lists each deployment's **Version**, **Date**, **User**, and **Label** columns. The most recent deployment carries the **live** badge. The label is the optional deployment label entered in the **Deploy your API** dialog. Before the first deployment, the page reads **No deployments yet**.

## Inspect a single version

To view the definition a deployment shipped, click **View definition** in the row's actions. For any version other than the live one, the actions menu also offers **Compare with live**.

## Compare two versions

Select the checkboxes of two versions. The toolbar tracks the selection, and once two versions are selected the diff view opens.

The **Comparing** dialog shows the differences between the two definitions, with **Side-by-side** and **Line-by-line** view modes. When the definitions are identical, the dialog reads **No differences found between these two versions.**

## Roll back to an earlier version

To roll back, follow these steps:

1. Compare the live version with the target version, for example with **Compare with live**.
2. In the diff dialog, click the **Rollback** button, which names the target version.
3. Confirm in the rollback dialog.

{% hint style="warning" %}
The rollback restores the API to the selected version and redeploys it to the gateway. The action can't be undone.
{% endhint %}

## Verification

To verify the deployment history is working as expected, follow these steps:

1. Deploy the API twice with different configurations, giving each deployment a label.
2. Open the **Deployment History** page. Both deployments appear with their labels, and the newest one carries the **live** badge.
3. Select both versions. The diff view shows the configuration change.

<!-- TODO: Screenshot of the diff dialog comparing two versions -->

<figure><img src="../../../.gitbook/assets/PLACEHOLDER-gamma-api-deployment-diff.png" alt=""><figcaption><p>Comparing two deployed versions</p></figcaption></figure>
