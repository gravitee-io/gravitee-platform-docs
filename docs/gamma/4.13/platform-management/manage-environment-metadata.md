---
hidden: false
noIndex: false
description: The Metadata page in the Gamma console holds the key-value entries that every API in the selected environment inherits. Add, edit, search, and delete them.
---

# Manage environment metadata

Environment metadata is a set of key-value entries defined once for an environment. Every API in that environment inherits each entry as a default value, and an API that defines the same key overrides the environment value for that API. Defining an entry once at the environment level saves repeating the same value on every API, and keeps the value consistent when it changes.

Each entry carries four parts:

* **Key**. The identifier that APIs and Developer Portal pages use to reference the entry. Gravitee generates it from the name when the entry is created.
* **Name**. The label the console displays.
* **Format**. The kind of value the entry holds: String, Numeric, Boolean, Date, Mail, or URL.
* **Value**. The value APIs inherit.

The Metadata page in the Gamma console lets you view, add, edit, and delete the entries of the selected environment.

## View environment metadata

From the Gamma console sidebar, select **Platform Management**, open the **Environment** section, and then navigate to **Metadata**.

The metadata table displays the following columns:

* **Key**. The entry's generated identifier.
* **Name**. The entry's name.
* **Format**. A badge that reads String, Numeric, Boolean, Date, Mail, or URL.
* **Value**. The value, or **&#x2014;** when the entry has no value.
* **Actions**. A row menu that holds the **Edit** and **Delete** actions. The column appears only when you can edit or delete entries, and the menu lists only the actions you can run.

The list is scoped to the environment selected in the console, and it arrives sorted by name, ignoring case. Select any of the four column headers to sort the table by that column instead. Use the search bar to filter the table by key or name, ignoring case. The table paginates 10 rows at a time by default, and offers 25, 50, and 100.

When the environment has no entries, the table reads **No global metadata defined for this environment.** When a search matches nothing, it reads **No metadata matches your search.**

A new environment starts with one entry: name `email-support`, format Mail, and value `support@change.me`.

<!-- TODO: Screenshot of the Metadata page listing the entries of an environment -->

<figure><img src="../.gitbook/assets/PLACEHOLDER-gamma-platform-metadata-list.png" alt=""><figcaption><p>The Metadata page lists the key-value entries that APIs in the selected environment inherit.</p></figcaption></figure>

## Add a metadata entry

To add an entry, complete the following steps:

1. Select **Add Global Metadata**.
2. Enter the entry details described in the following table:

    | Field      | Description                                                                                                    | Required |
    | ---------- | -------------------------------------------------------------------------------------------------------------- | -------- |
    | **Name**   | The entry's name. Gravitee generates the key from it, so a name that produces a key an entry in the environment already uses is rejected. | Yes      |
    | **Format** | **String**, **Numeric**, **Boolean**, **Date**, **Mail**, or **URL**. **String** is preselected, and the format is fixed after creation. | Yes      |
    | **Value**  | The value APIs inherit. The field matches the format you selected, and changing the format resets it.           | Yes      |

3. Select **Add**.

**Add** stays disabled until the name and the value are filled in and the value matches the selected format.

The following table describes what each format accepts:

| Format      | Value                                                                                                                    |
| ----------- | -------------------------------------------------------------------------------------------------------------------------- |
| **String**  | Any text.                                                                                                                  |
| **Numeric** | A number, entered in a number field.                                                                                       |
| **Boolean** | `true` or `false`, selected from a dropdown. Selecting the format sets the value to `false`.                                |
| **Date**    | A date, entered in a date field. The platform stores the date part alone, in `yyyy-MM-dd` form, and rejects a date that doesn't exist. |
| **Mail**    | An email address. The console reads **Invalid email** under the field while the value isn't one.                            |
| **URL**     | A URL. Enter it in full, including `http://` or `https://`. The console reads **Invalid URL** under the field while the value isn't one. |

An empty **Value** field shows no format error, and **Add** stays disabled until you fill it in.

## Edit a metadata entry

Editing an entry changes the value every API in the environment inherits, unless the API overrides the key with a value of its own. To edit an entry, complete the following steps:

1. In the entry's row, open the actions menu.
2. Select **Edit**.
3. Update the **Name**, the **Value**, or both. **Key** and **Format** are read-only.
4. Select **Update**.

**Update** stays disabled until you change the name or the value. Renaming an entry leaves its key unchanged, so the APIs and Developer Portal pages that reference the key keep working. A name that another entry in the environment already uses is rejected, matched without regard to case.

## Delete a metadata entry

To delete an entry, complete the following steps:

1. In the entry's row, open the actions menu.
2. Select **Delete**.
3. In the confirmation dialog, select **Delete**.

Deleting an entry removes it from the environment, and APIs that inherited it lose the default value. The platform also deletes every API-level metadata entry that uses the same key, including entries on APIs in other environments.

## How APIs and the Developer Portal use environment metadata

The entries of an environment are consumed in three places:

* **API metadata**. Each entry is a default value on every API in the environment. An API that defines the same key replaces the environment value with its own for that API.
* **Support requests**. A Developer Portal support request that isn't tied to an API is sent to the address held in the `email-support` entry. The platform refuses to send the request while that entry still holds its `support@change.me` default.
* **Developer Portal pages**. A Developer Portal page that isn't attached to an API can reference environment metadata values by key in its content.

## Next steps

* [Manage dictionaries](manage-dictionaries.md). Maintain the environment-scoped lookup data that API policies read at runtime.
