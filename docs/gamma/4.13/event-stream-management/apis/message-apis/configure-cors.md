---
hidden: false
noIndex: false
description: Allow browser clients from other origins to call the HTTP entrypoints of a Message API in Event Stream Management. Follow the steps to configure CORS.
---

# Configure CORS

Cross-origin resource sharing (CORS) decides which web origins can call a Message API from a browser. It applies to the entrypoints that listen over HTTP.

## Prerequisites

* A Message API with at least one entrypoint that listens over HTTP, such as **HTTP GET**, **HTTP POST**, or **Server-Sent Events**. Without one, the **CORS** page shows **No HTTP listener**.

## Configure CORS

1. From the Gamma console, open **Event Stream Management**.
2. In the sidebar, click **Message APIs**.
3. Click the name of the Message API.
4. In the **Design** group of the Message API sidebar, click **CORS**.
5. Select **Enable CORS**.
6. Complete the following fields:

<table>
    <thead>
        <tr>
            <th width="190">Field</th>
            <th>Description</th>
        </tr>
    </thead>
    <tbody>
        <tr>
            <td><strong>Allow origin</strong></td>
            <td>The origins allowed to call the Message API. Enter <code>*</code>, or an origin of the form <code>http://host</code> or <code>https://host:port</code>, then press Enter.</td>
        </tr>
        <tr>
            <td><strong>Allow methods</strong></td>
            <td>The HTTP methods allowed. Select the checkbox of each method: <code>GET</code>, <code>POST</code>, <code>PUT</code>, <code>DELETE</code>, <code>HEAD</code>, <code>PATCH</code>, or <code>OPTIONS</code>.</td>
        </tr>
        <tr>
            <td><strong>Allow headers</strong></td>
            <td>The request headers allowed.</td>
        </tr>
        <tr>
            <td><strong>Expose headers</strong></td>
            <td>The response headers that the browser exposes to the calling script.</td>
        </tr>
        <tr>
            <td><strong>Max age (seconds)</strong></td>
            <td>Optional. How long the browser caches the result of a preflight request.</td>
        </tr>
        <tr>
            <td><strong>Allow credentials</strong></td>
            <td>Select this checkbox to allow requests with credentials, such as cookies.</td>
        </tr>
    </tbody>
</table>

7. In the save bar at the bottom of the page, click **Save changes**.

The console confirms with **API updated**. The CORS settings reach the gateway at the next deployment, and until then the Message API shows **Out of sync**. See [Start, stop, and deploy a Message API](start-stop-and-deploy-a-message-api.md).

When an origin is invalid, clicking **Save changes** doesn't save. The save bar shows **Fix the errors to save** with the invalid origins, and the focus moves to the invalid field. When the save fails, the save bar shows **Couldn't save** with the reason, and **Save changes** becomes **Try again**.

To drop your changes instead, click **Discard**. If you leave the page with unsaved changes, the **Leave without saving?** dialog asks you to confirm.

The CORS settings apply to every HTTP listener of the Message API.

## Verification

To verify the CORS settings, follow these steps:

1. Reload the **CORS** page.
2. Check that **Enable CORS** is selected and that the fields show the values you saved.
