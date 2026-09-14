---
hidden: false
noIndex: false
description: Manage the metadata of an LLM, MCP, or A2A Proxy from its Metadata page. Follow the steps to add an entry, override an environment default, and reset it.
---

# Manage metadata for your proxies

Each LLM Proxy, MCP Proxy, and A2A Proxy detail view includes a **Metadata** page. A metadata entry describes the API rather than changing how it routes traffic, and it carries a key, a name, a format, and a value.

The page lists the entries in effect for one proxy: the entries the proxy holds a value for, together with the entries it inherits from its environment.

An environment entry arrives as a default value on every proxy in that environment. Giving the proxy its own value for the same key overrides that default for this proxy alone. For the environment side of the same data, see [Manage environment metadata](../../platform-management/manage-environment-metadata.md).

Metadata isn't part of the proxy definition, so an entry you add, change, or remove takes effect without a deployment. Each of those changes is recorded in the audit log of the proxy. See [Review audit logs](../observe/review-audit-logs.md).

## Open the Metadata page

To open the page, follow these steps:

1. Under **Secure** in the module sidebar, select **LLM Proxies**, **MCP Proxies**, or **A2A Proxies**.
2. Select the proxy you want to configure.
3. Under **General**, select **Metadata**.

The **Metadata** item is hidden when your role can't read the metadata of an API.

<!-- TODO: Screenshot of the Metadata page of an LLM Proxy, showing the blended list with a Global badge on an inherited row and the source filter -->

<figure><img src="../.gitbook/assets/PLACEHOLDER-gamma-aim-proxy-metadata-list.png" alt=""><figcaption><p>The Metadata page lists the entries in effect for the proxy</p></figcaption></figure>

## Read the metadata list

The table holds the following columns:

| Column       | Description                                                                                                                                      |
| ------------ | ------------------------------------------------------------------------------------------------------------------------------------------------ |
| **Key**      | The identifier generated from the name when the entry was created. A **Global** badge follows the key when the environment defines the same key. |
| **Name**     | The label the console displays.                                                                                                                  |
| **Format**   | **String**, **Numeric**, **Boolean**, **Date**, **Mail**, or **URL**.                                                                             |
| **Value**    | The value in effect: the proxy's own value, or the environment default when the proxy doesn't hold one. An entry with an empty value reads **&#x2014;**. |

The **Global** badge tracks the environment, not ownership. An entry the proxy has overridden keeps the badge as long as the environment still defines the key.

Each row ends with an actions menu. The column appears only when your role can change or remove metadata, and the menu lists only the actions that apply to the row.

The list arrives sorted by key, in ascending order. Select **Key**, **Name**, **Format**, or **Value** in the header to sort by that column instead. The table shows 10 entries per page by default.

The list above the table filters the entries by source. It offers the following options:

* **All sources**. Every entry in effect for the proxy.
* **Global**. The entries whose key the environment defines, including the ones the proxy has overridden.
* **API**. The entries the environment doesn't define, which the proxy holds on its own.

When the proxy has no entry at all, the table reads **No metadata defined for this API yet.** When the selected source matches nothing, it reads **No metadata matches the selected source.**

## Add an entry

To add an entry, follow these steps:

1. Click **Add metadata**.
2. In the **Add metadata** panel, enter a **Name**. The key is generated from it.
3. Select a **Format**. Changing the format clears the value.
4. Enter a **Value**. For **Boolean**, select `true` or `false`. Selecting the **Boolean** format sets the value to `false`.
5. Click **Add**.

<!-- TODO: Screenshot of the Add metadata panel of a proxy, showing the Name field, the Format list, and the Value field -->

<figure><img src="../.gitbook/assets/PLACEHOLDER-gamma-aim-proxy-metadata-add.png" alt=""><figcaption><p>The Add metadata panel</p></figcaption></figure>

The page confirms with **Metadata added**.

**Add** stays disabled until the name and the value are filled in and the value honors the selected format.

The following table describes what each format accepts:

| Format      | Value                                                                                                         |
| ----------- | --------------------------------------------------------------------------------------------------------------- |
| **String**  | Any text.                                                                                                     |
| **Numeric** | A number. The panel reads **Value must be a number.** while the value isn't one.                              |
| **Boolean** | `true` or `false`, selected from a list.                                                                      |
| **Date**    | A date in `YYYY-MM-DD` form, entered in a date field. A date that doesn't exist is refused.                   |
| **Mail**    | An email address. The panel reads **Value must be a valid email address.** while the value isn't one.         |
| **URL**     | A URL entered in full, including `http://` or `https://`. The panel reads **Value must be a valid URL, including the scheme (for example https://gravitee.io).** while the value isn't one. |

A name is at most 64 characters, and a value is at most 1,024 characters.

**Add metadata** refuses a name that another entry the proxy already owns uses, matched without regard to case.

It also refuses a name that generates the key of an entry already listed while differing from that entry's name. Choose a name that differs by more than punctuation or case.

A name that holds no letter or digit generates no key, and it's refused as well.

### Use an expression as a value

A value that starts with `${` is stored as a template and resolved against the API where the metadata is consumed. One entry then follows the API it belongs to, instead of repeating a fixed value. The **Value** column shows the stored template, not the resolved value.

The panel checks that the expression closes with a matching `}` and holds something between the braces. While it doesn't, the panel reads `Value must be a well-formed expression: "${" needs a matching closing "}" with something in between.`

An expression that resolves to something its format refuses is only caught when the entry is saved. The console then reports that the value doesn't honor its format, or that it couldn't be resolved.

The **Date** format takes a literal date alone. Entering an expression reads **A Date value must be a literal, not an expression.**

## Override an entry inherited from the environment

An entry the proxy doesn't hold a value for offers **Override** in its actions menu. Overriding writes the proxy's own value for that key and leaves the environment entry untouched.

To override an entry, follow these steps:

1. Open the actions menu of the entry, and then click **Override**.
2. In the **Override global metadata** panel, change the **Name**, the **Value**, or both. **Key** and **Format** are read-only, and **Global value** shows the environment's value for reference.
3. Click **Save**.

<!-- TODO: Screenshot of the Override global metadata panel, showing the read-only Key and Format fields and the Global value field above Value -->

<figure><img src="../.gitbook/assets/PLACEHOLDER-gamma-aim-proxy-metadata-override.png" alt=""><figcaption><p>The Override global metadata panel shows the environment's value above the proxy's own</p></figcaption></figure>

The page confirms with **Metadata updated**.

## Edit an entry the proxy owns

An entry the proxy holds a value for offers **Edit** in its actions menu.

To edit an entry, follow these steps:

1. Open the actions menu of the entry, and then click **Edit**.
2. In the **Edit metadata** panel, change the **Name**, the **Value**, or both.
3. Click **Save**.

The format of an entry is fixed once the entry exists. The panel notes **Format cannot be changed after creation.** under the read-only **Format** field.

**Save** refuses a name that any other entry in the list already uses, inherited entries included, matched without regard to case. The same check applies when you override an inherited entry.

## Reset an override or delete an entry

The last item of the actions menu depends on what the environment defines, and it appears only on an entry the proxy holds a value for.

* **Reset**, when the environment defines the same key. Removing the proxy's value restores the environment default, and the environment entry is untouched. The **Reset global metadata?** dialog names the value the entry goes back to. The page confirms with **Metadata reset to its global value**.
* **Delete**, when the environment doesn't define the key. The entry is removed from the proxy, and the **Delete metadata?** dialog warns that Markdown templates referencing it stop resolving and that the removal can't be undone. The page confirms with **Metadata deleted**.

An entry the proxy only inherits offers neither action, because the proxy holds nothing of its own to remove.

## Metadata of a proxy the Kubernetes operator manages

A proxy synced from the Kubernetes operator owns its metadata in its source definition, so the page lists the entries and offers no way to change them. The page reads **This API is managed by the Kubernetes operator. It can only be changed from its source definition.**

The actions are also hidden while the console can't tell where the proxy's definition comes from. When that read fails, the page reads **Could not confirm whether this API can be edited here** and asks you to refresh.

## Verification

To verify a metadata entry is in effect, follow these steps:

1. Add an entry to the proxy, for example a **Mail** entry named `Support contact`.
2. Reload the **Metadata** page. The entry is listed with the key generated from the name, and without a **Global** badge.
3. Select **API** in the source list. The entry is still listed, because the environment doesn't define its key.

<!-- TODO: Screenshot of the Metadata page filtered to API, showing the entry added in step 1 -->

<figure><img src="../.gitbook/assets/PLACEHOLDER-gamma-aim-proxy-metadata-api-filter.png" alt=""><figcaption><p>The entry the proxy owns, listed under the API source</p></figcaption></figure>
