---
hidden: false
noIndex: false
description: >-
  Override the AI Gateway's default error payloads on an A2A Proxy. Learn how a
  response template matches a request, what each field sets, and when the page
  is read-only.
---

# Configure A2A Proxy response templates

When the AI Gateway refuses or fails a request, it answers with a default error payload. A response template replaces that payload for one error and one kind of client. You match on a template key and an Accept header, and then return the status code, headers, and body of your choice.

Templates are stored on the A2A Proxy and matched per request, so one proxy can answer a browser with HTML and a service with JSON for the same error.

Among the proxy types in Agent Management, response templates are offered on A2A Proxies only. The **Response Templates** item isn't in the sidebar of an LLM Proxy or an MCP Proxy. A request that targets another proxy type is refused with the message **Response templates are not available for this proxy type.**

## Before you start

* You need an A2A Proxy.
* You need permission to read the definition of the proxy and to update its response templates. Without both, the page opens read-only and offers no way to add, edit, or delete a template.

## Open the Response Templates page

1. Open **Agent Management** in the Gamma console.
2. In the **Secure** section of the sidebar, select **A2A Proxies**.
3. Select your A2A Proxy.
4. In the **Design** group of the proxy sidebar, select **Response Templates**.

The page opens on the templates the proxy already carries. Each row shows its **Key**, its **Content-Type**, and its **Status Code**.

Type in **Search key, content-type, or status…** to narrow the list. When nothing matches, the table reads **No response templates found**, with **No templates match your search.** underneath and a **Clear search** button.

A proxy that carries no templates opens on an empty state titled **No Response Templates**, with an **Add new Response Template** button in the middle of it.

<!-- TODO: Screenshot of the Response Templates page of an A2A Proxy -->
<figure><img src="../../.gitbook/assets/PLACEHOLDER-gamma-a2a-response-templates-list.png" alt="The Response Templates page of an A2A Proxy, listing templates by Key, Content-Type, and Status Code"><figcaption><p>The Response Templates page of an A2A Proxy</p></figcaption></figure>

## Add a response template

1. Select **Add new Response Template**.
2. Set **Template key** to the error you're overriding. The field suggests **DEFAULT** and the gateway's own error keys, and it accepts a key you type yourself. When your text matches no suggestion, the list reads **No matching keys — your custom value will be used.**
3. Set **Accept header to match** to the Accept header of the requests this template answers, for example `application/json`. The field starts at `*/*`, which answers any Accept header.
4. Set **Status code** to the status the consumer receives. The field starts at `400`, and the name of the status appears beside the field once the value matches a known code. Select the browse button to pick from the known status codes.
5. Optional: under **HTTP Headers**, fill in the **Header name** and **Value**. The form always shows one empty row, and **Add header** adds another. A row left without a name isn't saved.
6. Optional: enter the payload in **Body**.
7. Optional: turn on **Add template key to logs** to record the template key alongside the request. It starts off.
8. Select **Create**.

The console reports **Configuration successfully saved!** and returns to the list.

Saving a template changes the API definition, so the proxy is left out of sync until you deploy it. The banner at the top reads **This API is out of sync**, with **Your latest changes are not live yet. Deploy to push them to the gateway.** Select **Deploy** on the banner, and then confirm in the **Deploy your API** dialog.

<!-- TODO: Screenshot of the Create a new Response Template form -->
<figure><img src="../../.gitbook/assets/PLACEHOLDER-gamma-a2a-response-template-form.png" alt="The Create a new Response Template form, with the Template key selector, the Accept header to match field, the Status code field beside the status name, the HTTP Headers rows, the Body field, and the Add template key to logs switch"><figcaption><p>Creating a response template on an A2A Proxy</p></figcaption></figure>

### What the form refuses

**Template key**, **Accept header to match**, and **Status code** are all required. The form reports each problem against its own field:

<table>
    <thead>
        <tr>
            <th width="320">What you did</th>
            <th>What the form says</th>
        </tr>
    </thead>
    <tbody>
        <tr>
            <td>Left <strong>Template key</strong> empty</td>
            <td><strong>Template key is required.</strong></td>
        </tr>
        <tr>
            <td>Left <strong>Accept header to match</strong> empty</td>
            <td><strong>Accept header is required.</strong></td>
        </tr>
        <tr>
            <td>Used a template key and Accept header another template already uses</td>
            <td><strong>Response template with key '&lt;key&gt;' and accept header '&lt;accept&gt;' already exists.</strong></td>
        </tr>
        <tr>
            <td>Left <strong>Status code</strong> empty</td>
            <td><strong>Status code is required.</strong></td>
        </tr>
        <tr>
            <td>Entered a value that isn't one of the known status codes</td>
            <td><strong>Invalid status code: &lt;value&gt;.</strong></td>
        </tr>
    </tbody>
</table>

The pair of a template key and an Accept header identifies a template, which is why the two together have to be unique on the proxy.

## Edit a response template

1. Open the actions menu at the end of the template's row.
2. Select **Edit**.
3. Change the fields you need.
4. Select **Save**.

Deploy the proxy to push the change to the gateway.

## Delete a response template

1. Open the actions menu at the end of the template's row.
2. Select **Delete**.
3. In the **Delete a Response Template** dialog, check the template named in the question, and then select **Delete**.

The console confirms that the template was deleted.

## When the page is read-only

The page opens without its editing controls in these cases:

* **The proxy is managed by the Kubernetes operator.** A banner reads **This API is managed by the Kubernetes operator. It can only be changed from its source definition.** Change the templates in the resource the operator applies.
* **Gamma can't confirm whether the proxy can be edited here.** The page reads **Could not confirm whether this API can be edited here**, with **Actions are hidden until this is confirmed. Refresh the page to try again.** underneath.
* **Your role can't update the proxy.** The add, edit, and delete controls aren't offered, and the actions menu offers **View** in place of **Edit**. Opening a template shows it under the title **View Response Template**.

A reader whose role can't see templates at all gets the page title and **You don't have permission to view response templates.** in place of the list.

## What an import does to response templates

Response templates travel with an A2A Proxy definition file:

* **Creating a proxy by importing a definition** applies the response templates the file carries. The create wizard has no response templates step, so a proxy created through the wizard starts with none.
* **Updating a proxy by importing a definition** replaces the proxy's response templates with the ones in the file. A file that carries none removes the templates the proxy had.

For the rest of what an import carries, see [Export and import an A2A Proxy](../export-and-import-an-a2a-proxy.md).

## Next steps

* [Add policies to your A2A Proxy](add-policies-to-a2a-proxy.md). The policies that produce many of the errors a template answers.
* [Configure logging and tracing](configure-logging-and-tracing.md). What the proxy records about each request.
