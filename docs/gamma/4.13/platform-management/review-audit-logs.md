---
hidden: false
noIndex: false
description: The Audit pages trace who changed what, and when, across the organization or within one environment. Read the trail, filter it, inspect a change, and export it.
---

# Review organization and environment audit logs

An audit event records a configuration change made through the platform, together with the account that made it, the object it applied to, and the change itself. Platform Management carries two Audit pages: one under **Organization**, which covers the whole organization, and one under **Environment**, which covers the environment selected in the console.

Both pages are read-only. Use them to trace a configuration change during an incident investigation, to answer a compliance question about who changed what, and to export a filtered trail for a compliance archive.

{% hint style="info" %}
The Audit pages require an enterprise license that includes the audit trail feature. Without it, either page opens an upgrade dialog instead of the trail, and closing the dialog returns you to the **Applications** page.
{% endhint %}

## Open an Audit page

The Audit page you open decides the scope of the trail. Both pages carry the heading **Audit**, so the section you opened it from is what tells them apart.

To review changes across the whole organization, complete the following steps:

1. From the Gamma console sidebar, select **Platform Management**.
2. Open the **Organization** section.
3. Navigate to **Audit**.

The page subtitle reads "Search configuration changes across the organization."

To review changes in a single environment, complete the following steps:

1. From the Gamma console sidebar, select **Platform Management**.
2. Open the **Environment** section.
3. Navigate to **Audit**.

The page subtitle reads "Search configuration changes for this environment."

<!-- TODO: Screenshot of the Organization Audit page with the filter toolbar and the results table -->

<figure><img src="../.gitbook/assets/PLACEHOLDER-gamma-platform-audit-organization.png" alt=""><figcaption><p>The Audit page of the Organization section, with the filter toolbar above the results table.</p></figcaption></figure>

Each page has its own access control, so a role that reaches one doesn't necessarily reach the other.

### What each page covers

The scope of each page is fixed, and no filter widens it.

The **Organization** page covers every audited change in the organization, across all its environments. The **Environment** page covers only the environment selected in the console, and it follows that selection when you switch environment.

Changes recorded against the organization itself don't belong to any environment, so they appear on the Organization page only. Both pages list the newest event first.

## Read the audit trail

The table lists one row per audit event, with the following columns:

| Column        | Description                                                                                                                           |
| ------------- | ------------------------------------------------------------------------------------------------------------------------------------- |
| **Date**      | When the event was recorded, as an absolute date and time rather than a relative one. Select it to open the event's detail panel.      |
| **User**      | The account that made the change. Select it to open the event's detail panel.                                                          |
| **Type**      | What kind of object the change applied to: `ORGANIZATION`, `ENVIRONMENT`, `APPLICATION`, or `API`.                                     |
| **Reference** | The name of that object, or its identifier when the name isn't available.                                                              |
| **Event**     | The identifier of the event type, such as `APPLICATION_UPDATED`.                                                                       |
| **Target**    | The properties of the object the event applied to, one `key: value` pair per line, or **&#x2014;** when the event carries none.        |

The last column holds a **View patch** button, which appears on the events that carry a patch.

The table paginates 10 rows at a time by default, and offers 25, 50, and 100.

The **User** column takes three forms:

* A display name is the account that signed in and made the change.
* `system` marks a change the platform made without a signed-in user.
* A display name followed by the name of a personal access token marks a change made with that token.

When the table has no rows and no filter is active, it shows **No audit logs** and explains that configuration changes will appear there. When a filter is active and nothing matches, it shows **No audit logs found** instead, and suggests adjusting or clearing the filters. When the trail can't be loaded, the page shows **Failed to load audit logs. Please try again.**

## Filter the audit trail

The toolbar above the table narrows the trail. Every filter change returns the table to the first page, and the filters apply to an export too, not only to the table.

To filter by event type, select an entry in the event type filter. It defaults to **All events** and lists every audit event type the platform defines, sorted by name, rather than only the types already recorded.

To filter by the kind of object that changed, select an entry in the type filter. It defaults to **All types**. The Organization page offers `ORGANIZATION`, `ENVIRONMENT`, `APPLICATION`, and `API`. The Environment page offers `APPLICATION` and `API` only.

Selecting a type other than `ORGANIZATION` reveals a second filter that narrows the results to one object:

* `ENVIRONMENT` reveals an environment picker. This filter is on the Organization page only.
* `APPLICATION` reveals an application picker.
* `API` reveals an API picker.

On the Organization page, the application and API pickers cover every environment, and each entry is labeled with its environment name followed by the object name. Changing the type clears whichever object you had picked.

<!-- TODO: Screenshot of the filter toolbar with the type filter open -->

<figure><img src="../.gitbook/assets/PLACEHOLDER-gamma-platform-audit-filters.png" alt=""><figcaption><p>The filter toolbar, with the type filter open.</p></figcaption></figure>

To bound the trail in time, use either of the following controls:

* The time period filter, which offers **Any time**, **Last 24 hours**, **Last 7 days**, **Last 30 days**, **Last 90 days**, and **Custom**.
* The **Date range** picker, which takes a start and an end date. The end date is inclusive to the end of that day, and picking a range switches the time period filter to **Custom**.

A relative period resolves against the moment you selected it, and it doesn't move forward on its own. To bring a relative period up to the current time, select it again.

To clear the active filters, select **Reset**. The button appears only while a filter is active.

## Inspect a change

Selecting the **Date** or **User** cell of a row, or its **View patch** button, opens the **Audit event** panel for that event.

The panel repeats the event's **User**, **Type**, **Reference**, **Event**, and **Target**, and adds a **JSON Patch** section when the event carries a patch. The patch is the difference between the object before and after the change, so it names each field that changed and the value it took.

Two details of the patch are worth knowing:

* The `createdAt` and `updatedAt` fields of the object are excluded, because they change on every write and say nothing about what the user changed.
* Values that the platform treats as sensitive are replaced with `*****`.

<!-- TODO: Screenshot of the Audit event panel showing the JSON Patch section -->

<figure><img src="../.gitbook/assets/PLACEHOLDER-gamma-platform-audit-event-panel.png" alt=""><figcaption><p>The Audit event panel, with the JSON Patch of the change.</p></figcaption></figure>

## Export the audit trail

An export writes the trail to a file for a compliance archive or an offline review. It covers everything the current filters match, not only the rows on screen.

To export the trail, complete the following steps:

1. Select **Export**.
2. In the **Export audit logs** dialog, select **CSV** or **JSON**.

The browser downloads a file named `audit-logs-YYYY-MM-DD.csv` or `audit-logs-YYYY-MM-DD.json`, dated the day you ran the export, and the console confirms with **Audit logs exported.**

The file carries seven values for each event: the date, the user, the type, the reference, the event, the target, and the patch. Dates are written in ISO 8601 UTC rather than in the console's own format. In a CSV export, a value that starts with `=`, `+`, `-`, `@`, a tab, or a carriage return is written with a leading apostrophe, so that a spreadsheet reads it as text instead of running it as a formula.

An export covers at most 10,000 events. Above that, it stops and reports how many events matched, so narrow the date range or the filters and run it again.

## Verification

To confirm that the trail records your changes, complete the following steps:

1. Change a setting of an object the audit trail covers, for example the description of an application, and save it.
2. Open the Audit page of the environment that holds the object.
3. Confirm that the change appears at the top of the table, with your account in the **User** column.
4. Select **View patch** on that row, and confirm that the **JSON Patch** section names the field you changed.
