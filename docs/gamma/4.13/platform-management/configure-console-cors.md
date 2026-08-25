---
hidden: false
noIndex: false
description: >-
  Control which browser origins may call the organization's Management API, and
  which methods and headers a cross-origin request may use.
---

# Configure CORS for the Management API

Cross-origin resource sharing (CORS) is the browser mechanism that decides whether a page served from one origin is allowed to call an API on another. The **CORS** page sets that policy for the Management API of this organization.

An origin is a scheme, a domain, and a port together, so `https://apps.example.com` and `http://apps.example.com` are different origins.

The values on this page are stored at organization scope and take effect without restarting the Management API.

{% hint style="info" %}
This page covers the Management API only. CORS for the Developer Portal API is configured at environment scope, and CORS for an API you publish is configured on that API.
{% endhint %}

## Open the CORS page

The page sits in the **Organization** section, alongside the other settings that apply across environments.

To open it, complete the following steps:

1. From the Gamma console sidebar, select **Platform Management**.
2. Open the **Organization** section.
3. Navigate to **CORS**.

The page subtitle reads "Control which browser origins may call this organization's management API."

<!-- TODO: Screenshot of the CORS page showing Allow-Origin, methods, headers, and Max age -->
<figure><img src="../.gitbook/assets/PLACEHOLDER-gamma-platform-cors.png" alt=""><figcaption><p>The CORS page of the <strong>Organization</strong> section</p></figcaption></figure>

Whether you can edit these fields depends on your access and on your installation's configuration file, in the same way as the other organization settings pages. See [Understand which fields you can edit](configure-console-management-and-schedulers.md#understand-which-fields-you-can-edit).

The following table maps each field to the configuration setting that locks it:

<table><thead><tr><th width="330">Field</th><th>Configuration key</th></tr></thead><tbody>
<tr><td><strong>Allow-Origin</strong></td><td><code>http.api.management.cors.allow-origin</code></td></tr>
<tr><td><strong>Access-Control-Allow-Methods</strong></td><td><code>http.api.management.cors.allow-methods</code></td></tr>
<tr><td><strong>Allow-Headers</strong></td><td><code>http.api.management.cors.allow-headers</code></td></tr>
<tr><td><strong>Exposed-Headers</strong></td><td><code>http.api.management.cors.exposed-headers</code></td></tr>
<tr><td><strong>Max age</strong></td><td><code>http.api.management.cors.max-age</code></td></tr>
</tbody></table>

## Set the allowed origins

**Allow-Origin** holds the origins that may call the Management API from a browser. Each origin is a separate entry, and the field starts at `*` on a new installation.

To add an origin, type it and press Enter, or type it and click outside the field. To remove one, click the cross on its entry, or press Backspace while the input is empty. An entry that's already in the list is ignored rather than added twice.

An entry is accepted either as a literal origin or as a regular expression. An entry other than a bare `*` that contains `(`, `[`, or `*` is compiled as a regular expression. One that doesn't compile is reported under the field as `"<entry>" Regex is invalid`, and saving is blocked until you fix it. Anything else is stored as you typed it, so a value that isn't a usable origin is accepted here and never matches a request.

The following entries show the three forms:

* `https://apps.example.com` matches that one origin.
* `(http|https)://.*\.example\.com` matches every subdomain of `example.com` on either scheme.
* `*` matches every origin.

### Allow every origin

Adding `*` removes cross-origin protection from the Management API, so the page asks you to confirm it. A dialog titled **Are you sure?** asks whether you want to remove all cross-origin restrictions. Click the confirm button, labeled `Yes, I want to allow all origins.`, to add the entry. Dismiss the dialog to leave the list unchanged.

While `*` is in the list, the field carries the note "Setting `*` exposes this management API to any website. Make sure that is intended."

{% hint style="warning" %}
The Management API answers cross-origin requests with credentials allowed. An origin on this list is therefore one whose pages can send a browser's existing session along with the call. Keep the list to the origins you operate.
{% endhint %}

### Origins that are always allowed

Two addresses are added to the allowed origins on top of whatever this list holds, so tightening **Allow-Origin** doesn't lock you out of the consoles.

The first is the APIM Console address for the organization. Gravitee takes it from the console URL in your installation configuration, and falls back to the **Management URL** setting when the installation configuration doesn't set one. See [Management URL](configure-console-management-and-schedulers.md#management-url).

The second is the Gamma console address for the organization, which comes from the Gamma URL in your installation configuration. Unlike the APIM Console address, it has no fallback to a stored setting, so set it in the installation configuration if you reach the Gamma console across an origin boundary.

## Choose the allowed methods

**Access-Control-Allow-Methods** is the set of HTTP methods a cross-origin caller may use. It's a row of checkboxes, and the browser reads it from the answer to a preflight request.

The available choices are `*`, `GET`, `DELETE`, `PATCH`, `POST`, `PUT`, `OPTIONS`, `TRACE`, and `HEAD`. On a new installation, `OPTIONS`, `GET`, `POST`, `PUT`, `DELETE`, and `PATCH` are selected.

## Choose the allowed and exposed headers

Two fields deal with headers, and they point in opposite directions. Both offer the same list of common HTTP header names as you type, and both accept a name that isn't on that list.

**Allow-Headers** is the set of headers a cross-origin caller may send. On a new installation it holds `Cache-Control`, `Pragma`, `Origin`, `Authorization`, `Content-Type`, `X-Requested-With`, `If-Match`, `X-Xsrf-Token`, and `X-Recaptcha-Token`.

**Exposed-Headers** is the set of response headers the browser lets the calling page read. On a new installation it holds `ETag` and `X-Xsrf-Token`.

In both fields, press Enter or type a comma to commit an entry. A part-typed entry that you leave by clicking elsewhere is discarded rather than added, so finish an entry before you move on.

{% hint style="warning" %}
The Gamma console sends `X-Requested-With` and `X-Xsrf-Token` on every call, adds `Content-Type` when the call carries a body, and reads `X-Xsrf-Token` back from the response. Removing one of those from **Allow-Headers** or **Exposed-Headers** breaks the Gamma console for anyone reaching the Management API across an origin boundary.
{% endhint %}

## Set the preflight cache duration

**Max age** is how long, in seconds, a browser may reuse the answer to a preflight request before asking again. It defaults to `1728000`, which is 20 days.

Enter a whole number of zero or more. The field accepts values up to `2147483647`, and anything higher, or anything that isn't a whole number, blocks saving.

## Save or discard your changes

Nothing is written until you save. As soon as a value differs from what's stored, a bar appears at the bottom of the page with **Discard** and **Save changes**.

To keep your changes, click **Save changes**. The button stays disabled while an origin fails to compile as a regular expression or **Max age** holds a value the field rejects. A toast reading "Configuration successfully saved!" confirms the write.

To abandon your changes, click **Discard**. The form returns to the values last read from the Management API.

{% hint style="warning" %}
A CORS change applies as soon as it's saved. Saving a policy that excludes the origin you're browsing from ends your own session's access to the Management API on the next call.
{% endhint %}
