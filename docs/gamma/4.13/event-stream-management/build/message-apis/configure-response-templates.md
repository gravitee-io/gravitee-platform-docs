---
hidden: false
noIndex: false
description: Customize the errors that the gateway returns for a Message API in Event Stream Management. Follow the steps to add response templates.
---

# Configure response templates

A response template replaces the error that the gateway returns for a Message API. Each template targets an error key and an `Accept` header, and defines a status code, headers, and a body. When an error ends the request, the gateway returns them. When an error affects a single message, the entrypoint decides what reaches the client.

When an error occurs, the gateway looks for a template in this order:

1. A template for the error key.
2. A template for the `DEFAULT` key.

Among the templates of that key, the gateway picks the one whose `Accept` header matches the request. A request without an `Accept` header, or with one that matches no template of that key, gets the `*/*` template of that key. Without one, the gateway returns its standard error. The gateway doesn't fall back to `DEFAULT` once the error key has a template.

## Add a response template

1. From the Gamma console, open **Event Stream Management**.
2. In the sidebar, click **Message APIs**.
3. Click the name of the Message API.
4. In the **Design** group of the Message API sidebar, click **Response Templates**.
5. Click **Add template**.
6. Complete the following fields:

<table>
    <thead>
        <tr>
            <th width="160">Field</th>
            <th>Description</th>
        </tr>
    </thead>
    <tbody>
        <tr>
            <td><strong>Key</strong></td>
            <td>Required. The error key that the template replaces, or <code>DEFAULT</code> for every error key without a template of its own. Errors that carry no error key always return the standard error.</td>
        </tr>
        <tr>
            <td><strong>Accept header</strong></td>
            <td>Required. The media type of the requests that get this template, for example <code>application/json</code>, or <code>*/*</code>.</td>
        </tr>
        <tr>
            <td><strong>Status code</strong></td>
            <td>Optional. The status code of the error.</td>
        </tr>
        <tr>
            <td><strong>Headers</strong></td>
            <td>Optional. Click <strong>Add header</strong>, then enter a header name and value.</td>
        </tr>
        <tr>
            <td><strong>Body</strong></td>
            <td>Optional. The body of the error.</td>
        </tr>
    </tbody>
</table>

7. Click **Save template**.
8. Click **Save changes**.

The templates are saved only when you click **Save changes**. The console confirms with **API updated**. The templates reach the gateway at the next deployment, and until then the Message API shows **Out of sync**. See [Start, stop, and deploy a Message API](start-stop-and-deploy-a-message-api.md).

To change or remove a template, use the edit or delete icon of its row, then click **Save changes**.

Without permission to change the response templates of the Message API, the page is read-only.

## Verification

To verify the templates, follow these steps:

1. Reload the **Response Templates** page.
2. Check that each template shows the key, the `Accept` header, the status code, and the body you entered.
