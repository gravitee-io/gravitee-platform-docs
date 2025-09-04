---
noIndex: true
---

# Server Name Indication (SNI)

Ambassador Edge Stack supports serving multiple `Host`s behind a single IP address, each with their own certificate.

This is as easy to do as creating a `Host` for each domain or subdomain you want Ambassador Edge Stack to serve, getting a certificate for each, and telling Ambassador Edge Stack which `Host` the route should be created for.

The example below configures two `Host`s and assigns routes to them.

## Configuring a `Host`

The `Host` resources lets you separate configuration for each distinct domain and subdomain you plan on serving behind Ambassador Edge Stack.

Let's start by creating a simple `Host` and providing our own certificate in the `host-cert` secret.

```yaml
---
apiVersion: getambassador.io/v3alpha1
kind: Host
metadata:
  name: example-host
spec:
  hostname: host.example.com
  tlsSecret:
    name: host-cert
```

Now let's create a second `Host` for a different domain we want to serve behind Ambassador Edge Stack. This second `Host` uses Ambassador Edge Stack's automatic TLS to get a certificate from Let's Encrypt.

```yaml
---
apiVersion: getambassador.io/v3alpha1
kind: Host
metadata:
  name: foo-host
spec:
  hostname: host.foo.com
  acmeProvider:
    email: julian@example.com
```

We now have two `Host`s with two different certificates.

{% hint style="info" %}
A minimum version of TLS 1.1 is required to properly use SNI. When setting up your TLS configuration, be sure you are not using TLS 1.0 or older.
{% endhint %}

## Configuring routes

Now that we have two domains behind Ambassador Edge Stack, we can create routes for either or both of them.

We do this by setting the `hostname` attribute of a `Mapping` to the domain the `Mapping` should be created for.

```yaml
---
apiVersion: getambassador.io/v3alpha1
kind:  Mapping
metadata:
  name:  httpbin
spec:
  prefix: /httpbin/
  service: httpbin.org:80
  host_rewrite: httpbin.org
  hostname: host.example.com
```

The above creates a `/httpbin/` endpoint for `host.example.com`.

```yaml
---
apiVersion: getambassador.io/v3alpha1
kind:  Mapping
metadata:
  name:  mockbin
spec:
  prefix: /foo/
  service: foo-service
  hostname: host.foo.com
```

The above creates a `/foo/` endpoint for `host.foo.com`.

```yaml
---
apiVersion: getambassador.io/v3alpha1
kind: Mapping
metadata:
  name: frontend
spec:
  hostname: "*"
  prefix: /bar/
  service: bar-endpoint
```

The above creates a `/bar/` endpoint for all `Host`s.
