---
hidden: false
noIndex: false
description: Define the key-value properties that the policies of a Message API read at runtime in Event Stream Management, encrypt sensitive values, and sync properties from an HTTP source. Follow the steps to manage them.
---

# Configure API properties

API properties are key-value pairs that the policies of a Message API read at runtime with the expression `{#api.properties['key']}`. Properties keep configuration values, such as timeouts or feature flags, out of the policies themselves.

## Open the properties

1. From the Gamma console, open **Event Stream Management**.
2. In the sidebar, click **Message APIs**.
3. Click the name of the Message API.
4. In the **Design** group of the Message API sidebar, click **API Properties**.

The page counts the total, encrypted, and dynamic properties, and lists them with their key, their value, and a badge for their characteristic, for example **Dynamic** or **Encrypted**. An encrypted value shows as dots.

Without permission to change the Message API's definition, the page is read-only.

## Add a property

1. Click **Add property**.
2. In **Key**, enter a key that the Message API doesn't use yet.
3. In **Value**, enter the value.
4. Optional: Turn on **Encrypt value** to store the value encrypted. Once saved, an encrypted value can't be read back.
5. Click **Add property**.

The console saves the property and confirms with **Message API updated**. The property reaches the gateway at the next deployment, and until then the Message API shows **Out of sync**. See [Start, stop, and deploy a Message API](start-stop-and-deploy-a-message-api.md).

## Change a property

Open the actions menu of the property's row:

* **Edit value** changes the value of an unencrypted property.
* **Encrypt value** encrypts an unencrypted property and saves it at once.
* **Renew encryption** replaces the value of an encrypted property. Leave the value empty to keep the current one.
* **Delete** removes the property.

Dynamic properties show **Managed** instead of an actions menu, because their source sets their values.

## Import properties

1. Click **Import**.
2. Enter one property per line, in the form `KEY=value`. A line that starts with `#` is a comment, and a quoted value can span several lines.
3. Click **Import properties**.

An imported key that already exists replaces the existing property, unless that property is encrypted. Encrypted properties are skipped. The panel lists the keys that it replaces and the keys that it skips before you import.

## Sync properties from an HTTP source

Dynamic properties are fetched on a schedule from an HTTP endpoint that you choose. The Management API polls the endpoint, so it needs network access to it.

1. Click **Manage dynamically**.
2. Turn on **Enable dynamic properties**.
3. In **Schedule (cron)**, enter a cron expression of six fields, `sec min hr dom mon dow`, or select a preset in **Quick select:**. The default, `0 */5 * * * *`, polls every five minutes.
4. Under **Request**, select the HTTP method, then enter the URL of the endpoint. Optional: Add **Request headers** and a **Request body**.
5. In **JOLT transformation specification**, enter a JOLT specification that turns the response into a list of objects with a `key` and a `value` field.
6. Optional: Expand **HTTP client options**, **Proxy**, or **SSL / TLS** to tune the HTTP client, route the calls through a proxy, or set the trust store and key store of the connection.
7. Click **Save changes**.
8. Deploy the Message API. See [Start, stop, and deploy a Message API](start-stop-and-deploy-a-message-api.md).

The Management API starts polling the source once the Message API is deployed while it's started. After a poll that returns the status code 200, the properties that the source returns appear as **Dynamic** properties, except for keys that you defined yourself. The policies read them like any other property. When the Message API has no other undeployed changes, the Management API redeploys it with the new values. Otherwise, they reach the gateway at your next deployment.

## Verification

To verify the properties, follow these steps:

1. Reload the **API Properties** page.
2. Check that each property shows the characteristic you expect.
3. When dynamic properties are on, deploy the Message API, wait for the first scheduled poll, then check that the counter of dynamic properties shows the keys that the source returns.
