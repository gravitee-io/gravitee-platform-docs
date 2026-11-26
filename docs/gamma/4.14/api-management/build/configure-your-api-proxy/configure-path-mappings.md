---
hidden: false
noIndex: false
description: Group the analytics of an API proxy by path, with path mappings such as /orders/:orderId. Follow the steps to add, import, edit, or delete them.
---

# Configure path mappings

Path mappings group the analytics of an API proxy by path. A path mapping such as `/orders/:orderId` groups every request that matches it, such as `/orders/42`, instead of listing each URL. A segment that starts with `:` matches any value in that segment, or none, so `/orders/:orderId` also matches `/orders`. When several path mappings match a request, the one with the fewest `:` segments groups it, so add `/orders` too to keep those requests apart.

The list applies the next time you deploy the API proxy. **Path Mappings** appears in the sidebar of an API proxy with an HTTP listener. It doesn't appear for a TCP proxy.

## Open the Path Mappings page

To open the page, follow these steps:

1. Click **API Proxies** in the module sidebar.
2. Select your API proxy.
3. Click **Path Mappings** in the **Monitoring** group of the API proxy sidebar.

The page lists each path mapping under **Path**. Until the API proxy has a path mapping, the page shows a **Why add a path mapping?** card. The card has an **Add path mapping** button unless the page is read-only.

The page is read-only when the API proxy is managed by the Gravitee Kubernetes Operator, or when you can't update the API proxy.

## Add a path mapping

To add a path mapping, follow these steps:

1. Click **Add path mapping**.
2. Select **Type a path**.
3. In **Path mapping**, enter a path, such as `/orders/:orderId`.
4. Click **Add**.

A path mapping is `/` followed by one or more unaccented letters, digits, or the characters `:`, `/`, `.`, `_`, and `-`. Two path mappings of an API proxy can't be the same.

## Import path mappings from an OpenAPI page

**Import from Swagger** adds the paths of an OpenAPI page of the API proxy's documentation in the next-gen Developer Portal. To add one, see [Manage API documentation](manage-api-documentation.md). Unpublished pages are listed when you can manage the API proxy's documentation. When the API proxy has no OpenAPI page, the panel shows `No swagger documentation in the next-gen Developer Portal.`

To import path mappings, follow these steps:

1. Click **Add path mapping**.
2. Select **Import from Swagger**.
3. Under **Choose a document**, select a page. Under its name, the page shows the first path that the import can add, followed by the number of other paths it can add.

    <figure><img src="../../.gitbook/assets/gamma-api-path-mappings-import.png" alt="The Add path mapping panel with Import from Swagger selected, an OpenAPI page chosen under Choose a document, and the Replace existing path mappings checkbox"><figcaption><p>Import path mappings from an OpenAPI page</p></figcaption></figure>
4. Optional: Select **Replace existing path mappings** to replace the list with the page's paths. Otherwise, the import adds the page's paths and keeps the existing path mappings. With **Replace existing path mappings** selected, a page with no valid path removes every path mapping.
5. Click **Import**.

The import writes each path parameter, such as `{orderId}`, as `:orderId`, adds each path once, and skips a path that isn't a valid path mapping.

## Edit or delete a path mapping

To edit a path mapping, follow these steps:

1. In the row of the path mapping, click the actions menu, then click **Edit**.
2. Change the **Path mapping**.
3. Click **Save**.

To delete a path mapping, follow these steps:

1. In the row of the path mapping, click the actions menu, then click **Delete**.
2. In the **Delete path mapping** dialog, click **Delete**.

## Deploy the changes

A change to the path mappings takes effect after you deploy the API proxy. After a change, the API proxy shows **This API is out of sync**, unless API review is enabled and the API proxy hasn't passed its review.

To deploy the API proxy, follow these steps:

1. Click **Deploy API**.
2. In the **Deploy your API** dialog, click **Deploy**.

## Verification

To verify the path mappings are in place, follow these steps:

1. Open the **Path Mappings** page of the API proxy.
2. Confirm that each path mapping shows under **Path**.

    <figure><img src="../../.gitbook/assets/gamma-api-path-mappings-page.png" alt="The Path Mappings page of an API proxy listing /orders, /orders/:orderId, and /orders/:orderId/items under Path, below the This API is out of sync banner"><figcaption><p>The Path Mappings page of an API proxy</p></figcaption></figure>

## Next steps

* [Import an API proxy](../import-an-api-proxy.md#import-options). Create the path mappings of an API proxy from an OpenAPI specification when you import it.
* [Manage API documentation](manage-api-documentation.md). Add the OpenAPI pages that **Import from Swagger** lists.
