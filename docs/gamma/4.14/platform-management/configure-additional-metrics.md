---
hidden: false
noIndex: false
description: Label, describe, and hide the additional metrics of an environment, and declare one before any request carries it, from the Metrics configuration page.
---

# Configure additional metrics

Additional metrics are values that a policy or the gateway attaches to a request. They show in the log detail as soon as requests carry them.

The **Metrics configuration** page lists the additional metrics of an environment. For each one, it sets the label, the description, and the unit that the Observability pages of the environment show, and whether their filter, column, and widget-editor lists offer it.

## Open the Metrics configuration page

To open the page, complete the following steps:

1. At the top of the page, click **Home**, or the name of the product you're working in.
2. Select **Platform Management**.
3. Open the **Environment** section. The section names show when you hover over the icons on the left.
4. Under **System & Security**, click **Metrics configuration**.

<!-- TODO: Screenshot of the Metrics configuration page, with built-in, declared, and discovered metrics in the table -->
<figure><img src=".gitbook/assets/PLACEHOLDER-gamma-platform-metrics-configuration.png" alt=""><figcaption><p>The Metrics configuration page</p></figcaption></figure>

The page appears only for a role that can read the environment's settings. Without permission to update them, the table is read-only, and the **Information** panel above it reads **You do not have permission to modify these settings. Contact your administrator for access.**

## Read the list

The **Additional metrics** table has one row per metric:

| Column | What it shows |
| ------ | ------------- |
| **Metric** | The label, with the key below it. |
| **Type** | The type of the values, such as **number** or **keyword**. **log detail only** follows the type of a metric that only the log detail shows, such as a **string** or **json** value. |
| **Origin** | **Built-in** for a metric that comes with Gravitee, **Declared** for a metric that has a record in this environment, and **Discovered** for a metric that requests of the last 30 days carried. |
| **Last seen** | When a request last carried the metric. **Not in 30 days** when no request of the last 30 days did. |
| **Unit** | The unit of the values, when the metric has one. |
| **Exposed** | **Exposed**, or **Hidden** for a metric that the filter, column, and widget-editor lists don't offer. |

Discovered metrics and **Last seen** times come from the environment's traffic, so they show only for a user who can read that traffic, such as the logs of one of its APIs.

To narrow the table, type in **Search by label or key**, or pick values under **Origin**, **Type**, and **Exposed**. **Clear filters** removes them.

Built-in metrics can't be edited.

## Declare a metric

Declaring a metric gives it a label, a description, and a unit before any request carries it. To declare a metric, complete the following steps:

1. Click **Declare a metric**.
2. Keep **Additional** selected, for a value that a policy or the gateway attaches to requests. **Custom** is for a value that the Assign metrics policy writes.
3. Under **Type**, select the type of the values. The type is part of the key and can't change later.
4. Under **Key**, enter the name of the metric, such as `checkout_basket-value`. **Full key** shows the key it makes, such as `additional-metrics.double_checkout_basket-value`.
5. Optional: Enter a **Label** and a **Description**.
6. Optional: Under **Unit**, select a unit, or select **Custom suffix** and enter the suffix, such as `€`.
7. Optional: Turn off **Exposed**. See [Hide a metric from the lists](#hide-a-metric-from-the-lists).
8. Click **Declare**.

<!-- TODO: Screenshot of the Declare a metric panel, with Additional selected and the Type, Key, Label, Description, Unit, and Exposed fields filled in -->
<figure><img src=".gitbook/assets/PLACEHOLDER-gamma-platform-declare-a-metric.png" alt=""><figcaption><p>The Declare a metric panel</p></figcaption></figure>

**Metric declared** confirms the save, and the metric shows as **Declared**. Until a request carries it, its **Last seen** reads **Not in 30 days**.

The **Type** list offers the following types:

| Type | Values |
| ---- | ------ |
| `long` and `int` | Whole numbers |
| `double` | Decimal numbers |
| `bool` | True or false |
| `keyword` | Short text, which the filters offer |
| `string` | Free text, shown in the log detail only |
| `json` | Structured values, shown in the log detail only |

The **Unit** list offers **No unit**, **Custom suffix**, and the following units, each followed in the list by its suffix when it has one:

| Unit | Suffix |
| ---- | ------ |
| **Percent** | `%` |
| **Milliseconds** | `ms` |
| **Seconds** | `s` |
| **Bytes** | `B` |
| **Kilobytes** | `KB` |
| **Megabytes** | `MB` |
| **Gigabytes** | `GB` |
| **Count** | None |
| **Count per second** | `/s` |
| **Tokens** | None |
| **Currency** | None |

The form refuses a value that breaks one of the following rules, and shows the message under the field:

| Rule | Message |
| ---- | ------- |
| The key holds letters, digits, `-`, `_`, `.`, and `/` only. | **Letters, digits, -, \_, . and / only** |
| The full key is 256 characters at most. | **The key is longer than 256 characters** |
| The key doesn't start with `custom_`. | **Keys starting with `custom_` are reserved** |
| No built-in metric reads the key. | **A built-in metric already uses this key** |
| The environment doesn't have a record on the key yet. | **Already declared in this environment** |
| The label is 64 characters at most. | **Label is longer than 64 characters** |
| The description is 512 characters at most. | **Description is longer than 512 characters** |
| The custom suffix is 16 characters at most. | **Unit is longer than 16 characters** |

## Edit a metric

You can edit a declared or a discovered metric. To edit a metric, complete the following steps:

1. Click its row.
2. Change the **Label**, the **Description**, the **Unit**, or **Exposed**. The key and the type can't change.
3. Click **Save**.

Saving a discovered metric creates its record, so it becomes a declared metric. **Record created** confirms it, and **Metric saved** confirms the save of a declared metric.

## Hide a metric from the lists

When **Exposed** is off, the metric shows as **Hidden**, and the filter, column, and widget-editor lists of the Observability pages don't offer it. The log detail still shows it, you can still use it by its key, and saved widgets keep working.

To hide a metric, open it, turn off **Exposed**, and then click **Save** or **Declare**.

## Delete a record

Deleting the record of a declared metric removes its label, its description, its unit, and its visibility setting. The metric is listed as **Discovered** while requests carry it, and disappears otherwise. Saved widgets keep working. To delete a record, complete the following steps:

1. Click the row of the declared metric.
2. Click **Delete record**.
3. In the **Delete this record?** dialog, click **Delete record**.

**Record deleted** confirms the deletion.

## See the metrics from API Management and Agent Management

API Management and Agent Management show the same table, read-only, on the **Settings** page of their **Observability** group. Each module leaves out the metrics that belong only to API types it doesn't manage. To change a metric, come back to the **Metrics configuration** page.

## Verification

To verify a declared metric, complete the following steps:

1. At the top of the page, click **Platform Management**.
2. Select **API Management**.
3. Under **Observability**, click **Settings**.
4. In **Search by label or key**, enter the label of the metric.

The table lists the metric with its label, unit, and **Declared** origin, with no edit action.
