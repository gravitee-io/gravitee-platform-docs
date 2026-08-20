---
hidden: false
noIndex: false
description: Compare two deployed versions of an API definition and roll back to an earlier one. Follow the steps to inspect the history and restore a version.
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

The empty state also shows the description **Deployment records will appear here after the first publish.** If the history can't be loaded, the page reads **Failed to load deployment history. Please try again.**

Use the pagination control to show 10, 25, 50, or 100 entries per page. Changing the page size returns you to page 1.

## Inspect a single version

To view the definition a deployment shipped, click **View definition** in the row's actions. For any version other than the live one, the actions menu also offers **Compare with live**.

## Compare two versions

Select the checkboxes of two versions. The toolbar tracks the selection, and once two versions are selected the diff view opens.

Until you make a selection, the hint above the list reads **Select two rows to compare versions.** You can select at most two versions at a time, and selecting a third replaces the earliest selection. Optional: click **Clear** in the toolbar to reset the selection.

The **Comparing** dialog shows the differences between the two definitions, with **Side-by-side** and **Line-by-line** view modes. The left pane is labeled **Before** and the right pane is labeled **After**. When the definitions are identical, the dialog reads **No differences found between these two versions.**

## Roll back to an earlier version

To roll back, follow these steps:

1. Compare the live version with the target version, for example with **Compare with live**.
2. In the diff dialog, click the **Rollback** button, which names the target version.
3. Confirm in the rollback dialog.

In the diff dialog, the **Rollback** button targets the right-hand **After** version, and it appears only when the two versions differ. The rollback controls are hidden unless you have the **API_DEFINITION** permission with the **UPDATE** access level.

{% hint style="warning" %}
The rollback restores the API to the selected version and redeploys it to the gateway. The action can't be undone.
{% endhint %}

After you confirm, a notification reports that the API was rolled back and redeployed, and the history list refreshes with the new deployment at the top. If the rollback fails, a card stays on screen with the reason.

## Verification

To verify the deployment history is working as expected, follow these steps:

1. Deploy the API twice with different configurations, giving each deployment a label.
2. Open the **Deployment History** page. Both deployments appear with their labels, and the newest one carries the **live** badge.
3. Select both versions. The diff view shows the configuration change.

<!-- TODO: Screenshot of the diff dialog comparing two versions -->

<figure><img src="../../../.gitbook/assets/PLACEHOLDER-gamma-api-deployment-diff.png" alt=""><figcaption><p>Comparing two deployed versions</p></figcaption></figure>
