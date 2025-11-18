# Authentication providers

{% tabs %}
{% tab title="HTTP" %}
<figure><img src="../../../../../../.gitbook/assets/resource_http (1).png" alt=""><figcaption><p>Create an HTTP Authentication Provider resource</p></figcaption></figure>

<table><thead><tr><th width="174">Config param</th><th width="227">Description</th><th>Default</th></tr></thead><tbody><tr><td>Resource name</td><td>The name of the resource</td><td>-</td></tr><tr><td>HTTP method</td><td>HTTP method to invoke the endpoint</td><td>POST</td></tr><tr><td>Use system proxy</td><td>Toggle to use the system proxy configured by your administrator</td><td>false</td></tr><tr><td>URL</td><td>Server URL</td><td>-</td></tr><tr><td>Request body</td><td>The body of the HTTP request. Supports the Gravitee Expression Language.</td><td>-</td></tr><tr><td>Authentication condition</td><td>The condition to be verified to validate that the authentication is successful. Supports the Gravitee Expression Language.</td><td>{#authResponse.status == 200}</td></tr></tbody></table>
{% endtab %}

{% tab title="Inline" %}
<figure><img src="../../../../../../.gitbook/assets/resource_inline (1).png" alt=""><figcaption><p>Create an Inline Authentication Provider resource</p></figcaption></figure>

<table><thead><tr><th width="174">Config param</th><th width="227">Description</th><th>Default</th></tr></thead><tbody><tr><td>Resource name</td><td>The name of the resource</td><td>-</td></tr><tr><td>HTTP method</td><td>HTTP method to invoke the endpoint</td><td>POST</td></tr><tr><td>Use system proxy</td><td>Toggle to use the system proxy configured by your administrator</td><td>false</td></tr><tr><td>URL</td><td>Server URL</td><td>-</td></tr><tr><td>Request body</td><td>The body of the HTTP request. Supports the Gravitee Expression Language.</td><td>-</td></tr><tr><td>Authentication condition</td><td>The condition to be verified to validate that the authentication is successful. Supports the Gravitee Expression Language.</td><td>{#authResponse.status == 200}</td></tr></tbody></table>
{% endtab %}

{% tab title="LDAP" %}
<figure><img src="../../../../../../.gitbook/assets/resource_ldap (1).png" alt=""><figcaption><p>Create an LDAP Authentication Provider resource</p></figcaption></figure>

<table><thead><tr><th width="174">Config param</th><th width="227">Description</th><th>Default</th></tr></thead><tbody><tr><td>Resource name</td><td>The name of the resource</td><td>-</td></tr><tr><td>HTTP method</td><td>HTTP method to invoke the endpoint</td><td>POST</td></tr><tr><td>Use system proxy</td><td>Toggle to use the system proxy configured by your administrator</td><td>false</td></tr><tr><td>URL</td><td>Server URL</td><td>-</td></tr><tr><td>Request body</td><td>The body of the HTTP request. Supports the Gravitee Expression Language.</td><td>-</td></tr><tr><td>Authentication condition</td><td>The condition to be verified to validate that the authentication is successful. Supports the Gravitee Expression Language.</td><td>{#authResponse.status == 200}</td></tr></tbody></table>
{% endtab %}
{% endtabs %}
