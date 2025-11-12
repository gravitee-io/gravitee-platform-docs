---
noIndex: true
---

# Rewrites

Once Ambassador Edge Stack uses a prefix to identify the service to which a given request should be passed, it can rewrite the URL before handing it off to the service.

There are two approaches for rewriting: `rewrite` for simpler scenarios and `regex_rewrite` for more advanced rewriting.

**Please note that** only one of these two can be configured for a mapping **at the same time**. As a result Ambassador Edge Stack ignores `rewrite` when `regex_rewrite` is provided.

## `rewrite`

By default, the `prefix` is rewritten to `/`, so e.g., if we map `/backend-api/` to the service `service1`, then

`http://ambassador.example.com/backend-api/foo/bar`

* `prefix`: /backend-api/ which rewrites to / by default.
* `rewrite`: /
* `remainder`: foo/bar

would effectively be written to

`http://service1/foo/bar`

* `prefix`: was /backend-api/
* `rewrite`: / (by default)

You can change the rewriting: for example, if you choose to rewrite the prefix as /v1/ in this example, the final target would be:

`http://service1/v1/foo/bar`

* `prefix`: was /backend-api/
* `rewrite`: /v1/

And, of course, you can choose to rewrite the prefix to the prefix itself, so that

`http://ambassador.example.com/backend-api/foo/bar`

* `prefix`: /backend-api/
* `rewrite`: /backend-api/

would be "rewritten" as:

`http://service1/backend-api/foo/bar`

To prevent Ambassador Edge Stack rewrite the matched prefix to `/` by default, it can be configured to not change the prefix as it forwards a request to the upstream service. To do that, specify an empty `rewrite` directive:

* `rewrite: ""`

In this case requests that match the prefix /backend-api/ will be forwarded to the service without any rewriting:

`http://ambassador.example.com/backend-api/foo/bar`

would be forwarded to:

`http://service1/backend-api/foo/bar`

## `regex_rewrite`

In some cases, a portion of URL needs to be extracted before making the upstream service URL. For example, suppose that when a request is made to `foo/12345/list`, the target URL must be rewritten as `/bar/12345`. We can do this as follows:

```
prefix: /foo/
regex_rewrite:
    pattern: '/foo/([0-9]*)/list'
    substitution: '/bar/\1'
```

`([0-9]*)` can be replaced with `(\d)` for simplicity.

`http://ambassador.example.com/foo/12345/list`

* `prefix`: /foo/
* `pattern`: /foo/12345/list where `12345` captured by `([0-9]*)`
* `substitution`: /bar/12345 where `12345` substituted by `\1`

would be forwarded to:

`http://service1/bar/12345`

More than one group can be captured in the `pattern` to be referenced by `\2`, `\3` and `\n` in the `substitution` section.

For more information on how `Mapping` can be configured, see [advanced-mapping-configuration.md](docs/edge-stack/technical-reference/using-custom-resources/advanced-mapping-configuration.md "mention").
