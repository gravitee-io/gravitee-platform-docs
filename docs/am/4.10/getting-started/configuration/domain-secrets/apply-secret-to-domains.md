---
description: An overview about reference secrets in domains.
---

# Apply Secret to Domains

### Overview <a href="#overview" id="overview"></a>

You can configure secret managers to work with your Domains. You can use secrets to hide information in any plugin field that supports secrets using Expression Language.&#x20;

This article explains the syntax that you can use to resolve secrets in Domains and configure secret managers.

### Reference a secret with specialized syntax <a href="#reference-a-secret-with-specialized-syntax" id="reference-a-secret-with-specialized-syntax"></a>

Secrets can be resolved in plugin fields that are marked as sensitive data. Fields supporting secrets are listed in the [Plugin support](plugins-support.md) section.

#### General syntax <a href="#general-syntax" id="general-syntax"></a>

`{#secrets.get('<path to secret>')}`

Arguments can have the following formats:

* Static strings, surrounded by simple quotes: `'`
* The syntax must start with `{#secrets.get(`. No spaces are allowed anywhere between `{` and `(`.
* The syntax must end with `)}` . There must be no space between `)` and `}`.

Arguments can be embedded in a larger string, like in the following example:

`"My password is {#secrets.get('<path to secret>')} and should remain a secret"`

#### Secret URI syntax <a href="#secret-uri-syntax" id="secret-uri-syntax"></a>

Secret URI syntax is a subset of URL syntax that you can use to [apply secrets to configurations](../secret-providers.md) (`secret://...`). Secret URI syntax allows you to specify the secret you want to resolve.

A URI is composed of the following components:

`/<provider>/<path>:<key>`&#x20;

* `provider`: The **id** or **plugin id** used to resolve secrets. It cannot contain `'/'`.
* `path`: The location of the secret in the secret manager. It can be a path, a name, or an ID. It is specific to each secret manager. It cannot contain `':'`.
* `key`: Secrets are returned as maps (key/value pairs). The key allows you to get one value of that map and is expected to be provided either as part of the URI, with `':'` separator, or as a separate argument.

A secret reference points directly to a secret value.&#x20;

The basic syntax specify the key after the path using the `':'` separator :

`{#secrets.get('/provider/path:key')}`

The key can also be provided as separate argument:

`{#secrets.get('/provider/path', 'key')}`

### Secret resolution  <a href="#secret-resolution-and-evaluation" id="secret-resolution-and-evaluation"></a>

Secret references are discovered when a domain is deployed or when a plugin is reloaded. When the EL is parsed, not evaluated, the URI is extracted, and then the secret can be resolved.

When the first resolution occurs, it blocks the deployment process for a short while.

Once a secret is resolved,  other Domains using the same URI will not attempt to resolve it again, since it will be cached.

