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

<figure><img src="../../../.gitbook/assets/gamma-api-deployment-history.png" alt="The Deployment History page, listing two deployments with Version, Date, User, and Label columns and a live badge on the newest version"><figcaption><p>The Deployment History page</p></figcaption></figure>

The table lists each deployment's **Version**, **Date**, **User**, and **Label** columns. The most recent deployment carries the **live** badge. The label is the optional deployment label entered in the **Deploy your API** dialog. Before the first deployment, the page reads **No deployments yet**.

The empty state also shows the description **Deployment records will appear here after the first publish.**

Use **Items per page** to show 10, 25, 50, or 100 entries per page. Changing the page size returns you to page 1.

## Inspect a single version

To view the definition a deployment shipped, click **View definition** in the row's actions. For any version other than the live one, the actions menu also offers **Compare with live**.

## Compare two versions

Select the checkboxes of two versions. The toolbar tracks the selection, and once two versions are selected, the diff view opens.

Until you make a selection, the toolbar hint reads **Select two rows to compare versions.** You can select at most two versions at a time. Once two are selected, the remaining checkboxes are disabled. To reset the selection, click **Clear** in the toolbar.

The **Comparing** dialog shows the differences between the two definitions, with **Side-by-side** and **Line-by-line** view modes. The panes are labeled **Before** and **After**, and **Before** holds the first of the two selected versions. When the definitions are identical, the dialog reads **No differences found between these two versions.**

## Roll back to an earlier version

To roll back, follow these steps:

1. Compare the live version with the target version, for example with **Compare with live**.
2. In the diff dialog, click the **Rollback** button, which names the target version.
3. Confirm in the rollback dialog.

In the diff dialog, the **Rollback** button targets the **After** version, and it appears only when the two versions differ. Rolling back requires the **API_DEFINITION** permission with the **UPDATE** access level. The controls stay visible without that permission, but the rollback fails.

{% hint style="warning" %}
The rollback restores the API definition to the selected version. It doesn't redeploy the API, so the API is left with undeployed changes until you deploy it. The action can't be undone.
{% endhint %}

After you confirm, the dialogs close and the selection clears. No entry is added to the history, and the API shows undeployed changes until you deploy it from **Deploy API**. If the rollback fails, a card stays on screen with the reason.

## Verification

To verify the deployment history is working as expected, follow these steps:

1. Deploy the API twice with different configurations, and give each deployment a label.
2. Open the **Deployment History** page. Both deployments appear with their labels, and the newest one carries the **live** badge.
3. Select both versions. The diff view shows the configuration change.

<figure><img src="../../../.gitbook/assets/gamma-api-deployment-diff.png" alt="The Comparing dialog in side-by-side mode, with the Before pane on the left, the After pane on the right, changed lines highlighted, and a Rollback button in the footer"><figcaption><p>Comparing two deployed versions</p></figcaption></figure>
