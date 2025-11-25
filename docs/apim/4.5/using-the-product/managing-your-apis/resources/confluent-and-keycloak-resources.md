---
description: Configuration and usage guide for confluent and keycloak resources.
---

# Confluent and Keycloak resources

{% tabs %}
{% tab title="Confluent Schema Registry" %}
{% hint style="warning" %}
**Enterprise only**

As of Gravitee 4.0, the ability to use Confluent Schema Registry as a resource is an Enterprise Edition capability. To learn more about Gravitee Enterprise, and what's included in various enterprise packages, please:

* [Refer to the EE vs OSS documentation](../../../overview/gravitee-apim-enterprise-edition/)
* [Book a demo](https://app.gitbook.com/o/8qli0UVuPJ39JJdq9ebZ/s/rYZ7tzkLjFVST6ex6Jid/)
* [Check out the pricing page](https://www.gravitee.io/pricing)
{% endhint %}

<figure><img src="../../../.gitbook/assets/resource_confluent.png" alt=""><figcaption><p>Create a Confluent Schema Registry resource</p></figcaption></figure>

<table><thead><tr><th width="199">Config param</th><th width="316">Description</th><th>Default</th></tr></thead><tbody><tr><td>Resource name</td><td>Name of the resource</td><td>-</td></tr><tr><td>Registry URL</td><td>URL of the schema registry</td><td>-</td></tr><tr><td>Use proxy</td><td>Toggle to use proxy to fetch schema</td><td>false</td></tr><tr><td>Proxy type</td><td>The type of the proxy</td><td>HTTP CONNECT proxy</td></tr><tr><td>Use system proxy</td><td>Toggle to use proxy configured at system level</td><td>false</td></tr><tr><td>Proxy host</td><td>Proxy host to connect to</td><td>-</td></tr><tr><td>Proxy port</td><td>Proxy port to connect to</td><td>-</td></tr><tr><td>Proxy username</td><td>Optional proxy username</td><td>-</td></tr><tr><td>Proxy password</td><td>Optional proxy password</td><td>-</td></tr><tr><td>Authentication mode</td><td>The authentication mode used to connect to Schema Registry</td><td>Basic</td></tr><tr><td>Authentication username</td><td>Authentication username</td><td>-</td></tr><tr><td>Authentication password</td><td>Authentication password</td><td>-</td></tr><tr><td>Verify host</td><td>Toggle to enable host name verification</td><td>true</td></tr><tr><td>Trust all</td><td>Toggle to force the Gateway to trust any origin certificates. Use with caution over the Internet. The connection will be encrypted but this mode is vulnerable to 'man in the middle' attacks.</td><td>false</td></tr><tr><td>Trust store type</td><td>The type of the trust store</td><td>None</td></tr><tr><td>Key store type</td><td>The type of the key store</td><td>None</td></tr></tbody></table>
{% endtab %}

{% tab title="Keycloak Adapter" %}
<figure><img src="../../../.gitbook/assets/resource_keycloak.png" alt=""><figcaption><p>Create a Keycloak Adapter resource</p></figcaption></figure>

| Config param                  | Description                                           | Default |
| ----------------------------- | ----------------------------------------------------- | ------- |
| Resource name                 | The name of the resource                              | -       |
| Keycloak client configuration | The configuration of the Keycloak client              | -       |
| Local token validation        | Toggle to use local token validation                  | true    |
| User claim                    | User claim field to store end user in log analytics   | sub     |
| Verify host                   | Verify certificate on SSL connection to Keycloak host | false   |
| Trust all                     | Trust all certificates, including self-signed         | true    |
{% endtab %}
{% endtabs %}
