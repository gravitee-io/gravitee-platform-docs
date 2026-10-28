---
description: Overview of Ambassador Edge Stack.
noIndex: true
---

# Ambassador Edge Stack and Redis

The Ambassador Edge Stack make use of Redis for several purposes. By default, all components of the Ambassador Edge Stack share a Redis connection pool.

### Redis password in the Helm chart

Redis holds OAuth2 sessions and rate limit counters, so only Ambassador Edge Stack should be able to read and change it. Starting with Helm chart v8.15.0 (Ambassador Edge Stack 3.15.0), the Redis instance that the chart creates requires a password by default:

* On the first install, the chart generates a random 32-character password and stores it in a Secret named `<release-fullname>-redis-auth`, under the key `password`, in the release namespace. For a release named `edge-stack`, the Secret is `edge-stack-redis-auth`.
* The chart starts Redis with `--requirepass`, and gives the password to Ambassador Edge Stack in the `REDIS_PASSWORD` and `REDIS_AUTH` environment variables, both read from the Secret. The password isn't written to a ConfigMap, the pod spec, or the notes that Helm prints after an install or upgrade.
* On each `helm upgrade`, the chart reads the password back from the existing Secret, so it doesn't change.

The following Helm values control this behavior:

| Value | Default | Description |
| ----- | ------- | ----------- |
| `redis.auth.enabled` | `true` | Require a password on the Redis instance that the chart creates. Set to `false` to run it without a password, as in chart versions before v8.15.0. |
| `redis.auth.password` | `""` | Use this password instead of a generated one. Ignored when `redis.auth.createSecret` is `false`. |
| `redis.auth.createSecret` | `true` | Set to `false` to create and manage the `<release-fullname>-redis-auth` Secret yourself, for example with an external secrets operator. The Secret must contain the key `password` and exist before the Redis pod starts. Switching an existing release from `true` to `false` deletes the chart's Secret, so create yours right after that upgrade. |

{% hint style="warning" %}
Before you upgrade to chart v8.15.0, check the following:

* If you deploy with a tool that renders the chart with `helm template`, such as Argo CD, set `redis.auth.password` from your secret store or set `redis.auth.createSecret=false`. These tools can't read the existing Secret, so the chart would generate a new password on every render.
* Use `helm upgrade --reset-then-reuse-values` (Helm 3.14 and later) instead of `--reuse-values`. With `--reuse-values`, Helm keeps the previous chart's `emissary-ingress.envRaw`, which doesn't pass the password to Ambassador Edge Stack, so the chart leaves Redis without a password and prints a warning.

The first upgrade restarts Redis with a password and restarts the Ambassador Edge Stack pods. Redis keeps its data in memory, so existing OAuth2 sessions and rate limit counters are lost, as with any Redis restart. An Ambassador Edge Stack pod that starts while the old Redis pod is still running can fail to set up rate limiting, so after the upgrade finishes, restart Ambassador Edge Stack: `kubectl rollout restart -n <namespace> deployment/<release-fullname>`.
{% endhint %}

The chart leaves Redis without a password, as in earlier versions, in the following cases:

* **You use an external Redis.** If you set `emissary-ingress.redisURL` or `redis.create=false`, the chart doesn't create the Secret or send a password. To authenticate to your own Redis, set `REDIS_PASSWORD` and `REDIS_AUTH` yourself, as shown in [Redis authentication](#redis-authentication-auth). The top-level `redisURL` value isn't passed to Ambassador Edge Stack, so use `emissary-ingress.redisURL`. If you set only the top-level `redisURL`, Ambassador Edge Stack still uses the chart's Redis instance, and the chart leaves it without a password.
* **You already protect Redis yourself**, with `--requirepass` in `redis.containerArgs`, or with `REDIS_PASSWORD` or `REDIS_AUTH` in `emissary-ingress.env`.
* **You override `emissary-ingress.envRaw`** without the `REDIS_PASSWORD` and `REDIS_AUTH` entries from the chart's default value. The chart prints a warning. To turn on the password, add those entries to your `envRaw`.

Keep the following in mind:

* **If you enable `REDIS_PERSECOND`** and point `REDIS_PERSECOND_URL` at the Redis instance that the chart creates, also set `REDIS_PERSECOND_PASSWORD` and `REDIS_PERSECOND_AUTH` from the same Secret.
* **Ambassador Edge Stack reads the password only when its pods start.** After you change the password, turn `redis.auth.enabled` on or off (including by adding your own `REDIS_PASSWORD`, `REDIS_AUTH`, or `--requirepass`), or run `helm rollback` between revisions that use chart v8.15.0 or later, restart both deployments: `kubectl rollout restart -n <namespace> deployment/<release-fullname>-redis deployment/<release-fullname>`.
* **The password is stored in the Helm release record**, like any Secret that Helm manages. With Helm's default storage driver, the release record is itself a Secret, so only users who can read Secrets in the release namespace can see it.

The YAML manifests can't include a password that's unique to each installation, so the Redis instance that they create still runs without a password. In the 3.15.0 and later manifests, the Ambassador Edge Stack deployment reads `REDIS_PASSWORD` and `REDIS_AUTH` from an optional `edge-stack-redis-auth` Secret. To add a password to a YAML installation, first upgrade to the 3.15.0 or later manifests, then create the Secret, start Redis with it, and restart Ambassador Edge Stack:

```bash
kubectl create secret generic -n ambassador edge-stack-redis-auth --from-literal=password="$(openssl rand -hex 24)"
kubectl patch deployment -n ambassador edge-stack-redis --type=json -p '[
  {"op":"add","path":"/spec/template/spec/containers/0/env","value":[{"name":"REDIS_PASSWORD","valueFrom":{"secretKeyRef":{"name":"edge-stack-redis-auth","key":"password"}}}]},
  {"op":"add","path":"/spec/template/spec/containers/0/args","value":["--requirepass","$(REDIS_PASSWORD)"]}]'
kubectl rollout restart -n ambassador deployment/edge-stack
```

These commands use the `ambassador` namespace. Use the namespace that you installed into. In the `-migration` manifests, the Ambassador Edge Stack deployment is named `aes`.

{% hint style="info" %}
Don't create the Secret without also changing Redis. If the Secret exists but Redis has no password, Ambassador Edge Stack fails to authenticate to Redis after its next restart.
{% endhint %}

A password protects Redis from clients that can reach it on the network. It doesn't protect Redis from users who can create Ambassador Edge Stack resources, because those users can act with Ambassador Edge Stack's own access. For more information, see [Controlling Who Can Configure Ambassador Edge Stack](controlling-who-can-configure-ambassador-edge-stack.md).

### Rate Limit Service

The rate limiting service, can be configured to use different connection pools for handling per-second rate limits or connecting to Redis clusters.

#### AES\_RATELIMIT\_PREVIEW

Set `AES_RATELIMIT_PREVIEW` to `true` to access support for redis clustering, local caching, and an upgraded redis client with improved scalability in preview mode.

#### REDIS\_PERSECOND

If `REDIS_PERSECOND` is true, a second Redis connection pool is created (to a potentially different Redis instance) that is only used for per-second RateLimits; this second connection pool is configured by the `REDIS_PERSECOND_*` variables rather than the usual `REDIS_*` variables.

### Redis layer 4 connectivity (L4)

**`SOCKET_TYPE`**

The Go network to use to talk to Redis. see [Go net.Dial](https://golang.org/src/net/dial.go)

Most users will leave this as the default of `tcp`.

**`URL`**

The URL to dial to talk to Redis

This will be either a hostname:port pair or a comma separated list of hostname:port pairs depending on the [TYPE](ambassador-edge-stack-and-redis.md#redis-type) you are using.

For `REDIS_URL` (but not `REDIS_PERSECOND_URL`), not setting a value disables Ambassador Edge Stack features that require Redis.

**`TLS_ENABLED`**

Specifies whether to use TLS when talking to Redis.

**`TLS_INSECURE`**

Specifies whether to skip certificate verification when using TLS to talk to Redis.

Consider installing the self-signed certificate for your Redis in to the Ambassador Edge Stack container in order to leave certificate verification on. For more information, see [using-filters-and-filterpolicies.md](../../technical-reference/filters/using-filters-and-filterpolicies.md "mention").

### Redis authentication (auth)

**Default**

Configure authentication to a redis pool using the default implementation.

**`PASSWORD`**

If set, it is used to [AUTH](https://redis.io/commands/auth) to Redis immediately after the connection is established.

**`USERNAME`**

If set, then that username is used with the password to log in as that user in the [Redis 6 ACL](https://redis.io/docs/latest/operate/oss_and_stack/management/security/acl/). It is invalid to set a username without setting a password. It is invalid to set a username with Redis 5 or lower.

The following YAML snippet is an example of configuring Redis authentication in the Ambassador deployment's environment variables.

```yaml
env:
- name: REDIS_USERNAME:
  value: "default"
- name: REDIS_PASSWORD:
  valueFrom:
    secretKeyRef:
      key: password
      name: ambassador-redis-password
```

{% hint style="info" %}
This example demonstrates getting the redis password from a secret called `ambassador-redis-password` instead of providing the value directly.
{% endhint %}

**Rate Limit Preview**

Configure authentication to a redis pool using the preview rate limiting implementation

**`AUTH`**

Required for authentication with Rate Limit Preview. You must also configure `REDIS_USERNAME` and `REDIS_PASSWORD` for the rest of Ambassador's Redis usage.

If you configure `REDIS_AUTH`, then `REDIS_USERNAME` cannot be changed from the value `default`, and `REDIS_PASSWORD` should contain the same value as `REDIS_AUTH`.

`REDIS_USERNAME` and `REDIS_PASSWORD` handle all Redis authentication that is separate from Rate Limit Preview so failing to set them when using `REDIS_AUTH` will result in Ambassador not being able to authenticate with Redis for all of its other functionality.

Adding `AUTH` to the example above for rate limit preview would look like the following snippet.

```yaml
env:
- name: REDIS_USERNAME:
  value: "default"
- name: REDIS_PASSWORD:
  valueFrom:
    secretKeyRef:
      key: password
      name: ambassador-redis-password
- name: REDIS_AUTH
  valueFrom:
    secretKeyRef:
      key: password
      name: ambassador-redis-password
```

{% hint style="warning" %}
Setting `AUTH` without `USERNAME` and `PASSWORD` can result in various problems since `AUTH` does not overwrite the basic Redis authentication behavior for systems outside of rate limit preview.
{% endhint %}

### Redis performance tuning (tune)

**`POOL_SIZE`**

The number of connections to keep around when idle.

The total number of connections may go lower than this if there are errors.

The total number of connections may go higher than this during a load surge.

**`PING_INTERVAL`**

The rate at which Ambassador will ping the idle connections in the normal pool (not extra connections created for a load surge).

Ambassador will `PING` one of them every `PING_INTERVAL÷POOL_SIZE` so that each connection will on average be `PING`ed every `PING_INTERVAL`.

**`TIMEOUT`**

Sets 4 different timeouts:

1. `(*net.Dialer).Timeout` for establishing connections
2. `(*redis.Client).ReadTimeout` for reading a single complete response
3. `(*redis.Client).WriteTimeout` for writing a single complete request
4. The timeout when waiting for a connection to become available from the pool (not including the dial time, which is timed out separately)

A value of "0" means "no timeout".

**`SURGE_LIMIT_INTERVAL`**

During a load surge, if the pool is depleted, then Ambassador may create new connections to Redis in order to fulfill demand, at a maximum rate of one new connection per `SURGE_LIMIT_INTERVAL`.

A value of "0" (the default) means "allow new connections to be created as fast as necessary.

The total number of connections that Ambassador can surge to is unbounded.

**`SURGE_LIMIT_AFTER`**

The number of connections that can be created _after_ the normal pool is depleted before `SURGE_LIMIT_INTERVAL` kicks in.

The first `POOL_SIZE+SURGE_LIMIT_AFTER` connections are allowed to be created as fast as necessary.

This setting has no effect if `SURGE_LIMIT_INTERVAL` is 0.

**`SURGE_POOL_SIZE`**

Normally during a surge, excess connections beyond `POOL_SIZE` are closed immediately after they are done being used, instead of being returned to a pool.

`SURGE_POOL_SIZE` configures a "reserve" pool for excess connections created during a surge.

Excess connections beyond `POOL_SIZE+SURGE_POOL_SIZE` will still be closed immediately after use.

**`SURGE_POOL_DRAIN_INTERVAL`**

How quickly to drain connections from the surge pool after a surge is over.

Connections are closed at a rate of one connection per `SURGE_POOL_DRAIN_INTERVAL`.

This setting has no effect if `SURGE_POOL_SIZE` is 0.

### Redis type

Redis currently support three different deployment methods. Ambassador Edge Stack can now support using a Redis deployed in any of these ways for rate limiting when `AES_RATELIMIT_PREVIEW=true`.

**`TYPE`**

*   `SINGLE`: Talk to a single instance of redis, or a redis proxy.

    Requires the redis `REDIS_URL` or `REDIS_PERSECOND_URL` to be either a single hostname:port pair or a unix domain socket reference.
*   `SENTINEL`: Talk to a redis deployment with sentinel instances (see https://redis.io/topics/sentinel).

    Requires the redis `REDIS_URL` or `REDIS_PERSECOND_URL` to be a comma separated list with the first string as the master name of the sentinel cluster followed by hostname:port pairs. The list size should be >= 2. The first item is the name of the master and the rest are the sentinels.
*   `CLUSTER`: Talk to a redis in cluster mode (see https://redis.io/topics/cluster-spec)

    Requires the redis `REDIS_URL` or `REDIS_PERSECOND_URL` to be either a single hostname:port pair of the read/write endpoint or a comma separated list of hostname:port pairs with all the nodes in the cluster.

    `PIPELINE_WINDOW` must be set when `TYPE: CLUSTER`.

**`PIPELINE_WINDOW`**

The duration after which internal pipelines will be flushed.

If window is zero then implicit pipelining will be disabled.

> `150us` is recommended when using implicit pipelining in production.

**`PIPELINE_LIMIT`**

The maximum number of commands that can be pipelined before flushing.

If limit is zero then no limit will be used and pipelines will only be limited by the specified time window.
