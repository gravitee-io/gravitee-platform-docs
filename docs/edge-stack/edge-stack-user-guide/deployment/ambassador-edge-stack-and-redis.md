---
description: Overview of Ambassador Edge Stack.
noIndex: true
---

# Ambassador Edge Stack and Redis

The Ambassador Edge Stack make use of Redis for several purposes. By default, all components of the Ambassador Edge Stack share a Redis connection pool.

### Redis password in the Helm chart

Redis holds OAuth2 sessions and rate limit counters, so only Ambassador Edge Stack should be able to read and change it. Starting with Helm chart v8.15.0 (Ambassador Edge Stack 3.15.0), the Redis instance that the chart creates requires a password by default.

{% hint style="warning" %}
**If you deploy with Argo CD, Flux, or another tool that renders the chart with `helm template`, set the password yourself before you upgrade to chart v8.15.0.** The chart generates the password once and then reads it back from the cluster on later upgrades, which isn't possible when the chart is rendered offline. Each offline render generates a new random password: the application never stops showing a difference, every sync rewrites the Secret, and the next Ambassador Edge Stack or Redis pod to start can no longer authenticate, which breaks OAuth2 logins and rate limiting. Before you upgrade, do one of the following:

* Set `redis.auth.password`, for example from your secret store.
* Create the `<release-fullname>-redis-auth` Secret yourself with a non-empty `password` key, and set `redis.auth.createSecret=false`.
{% endhint %}

* On the first install, the chart generates a random 32-character password and stores it in a Secret named `<release-fullname>-redis-auth`, under the key `password`, in the release namespace. For a release named `edge-stack`, the Secret is `edge-stack-redis-auth`.
* The chart starts Redis with `--requirepass`, and gives the password to Ambassador Edge Stack in the `REDIS_PASSWORD` and `REDIS_AUTH` environment variables, both read from the Secret. The password isn't written to a ConfigMap, the pod spec, or the notes that Helm prints after an install or upgrade.
* On each `helm upgrade`, the chart reads the password back from the existing Secret, so it doesn't change.
* With the password on, Redis refuses to start if the `password` key of the Secret is empty, for example a Secret that you manage with `redis.auth.createSecret=false` and left empty. Its `check-redis-password` init container exits with an error instead of letting Redis start without a password. Put a non-empty password in the Secret, or set `redis.auth.enabled=false`.
* The Secret has the `helm.sh/resource-policy: keep` annotation, so `helm uninstall` leaves it in place, and reinstalling a release with the same name and namespace reuses the same password. To rotate the password, or to remove it after you uninstall for good, delete the Secret: `kubectl delete secret -n <namespace> <release-fullname>-redis-auth`. With the password on, the next `helm upgrade` or install generates a new one. Run that upgrade right away, because until the Secret exists again a restarted Redis pod can't start, and then restart Redis and Ambassador Edge Stack as described below.
* While the chart manages the Secret (`redis.auth.createSecret=true`, the default), it always creates it, with an empty password when Redis has none. This way, a Secret left over from an earlier revision never gives Ambassador Edge Stack an old password for a Redis instance that has none. If a Secret named `<release-fullname>-redis-auth` already exists that the release didn't create, for example one that you created for a YAML installation, `helm install` and `helm upgrade` fail with an ownership error. Set `redis.auth.createSecret=false`, delete the Secret, or adopt it into the release.

The following Helm values control this behavior:

| Value | Default | Description |
| ----- | ------- | ----------- |
| `redis.auth.enabled` | `true` | Require a password on the Redis instance that the chart creates. Applies only when `redis.create` is `true` and no external Redis URL is set. Set to `false` to run it without a password, as in chart versions before v8.15.0. |
| `redis.auth.password` | `""` | Use this password instead of a generated one. Ignored when `redis.auth.createSecret` is `false`. |
| `redis.auth.createSecret` | `true` | Set to `false` to create and manage the `<release-fullname>-redis-auth` Secret yourself, for example with an external secrets operator. The Secret must contain a non-empty `password` key and exist before the Redis pod starts. |

{% hint style="warning" %}
Before you upgrade to chart v8.15.0, check the following:

* If you deploy with a tool that renders the chart with `helm template`, follow the instructions at the top of this section.
* Use `helm upgrade --reset-then-reuse-values` (Helm 3.14 and later) instead of `--reuse-values`. With `--reuse-values`, Helm keeps the previous chart's `emissary-ingress.envRaw`, which doesn't pass the password to Ambassador Edge Stack, so the chart leaves Redis without a password and prints a warning.

The first upgrade restarts Redis with a password and restarts the Ambassador Edge Stack pods. Redis keeps its data in memory, so existing OAuth2 sessions and rate limit counters are lost, as with any Redis restart. An Ambassador Edge Stack pod that starts while the old Redis pod is still running can fail to set up rate limiting, so after the upgrade finishes, restart Ambassador Edge Stack: `kubectl rollout restart -n <namespace> deployment/<release-fullname>`.
{% endhint %}

The chart leaves Redis without a password, as in earlier versions, in the following cases:

* **You use an external Redis.** If you set `emissary-ingress.redisURL` or `redis.create=false`, the chart doesn't send a password. To authenticate to your own Redis, set `REDIS_PASSWORD` and `REDIS_AUTH` yourself, as shown in [Redis authentication](#redis-authentication-auth). The top-level `redisURL` value isn't passed to Ambassador Edge Stack, so use `emissary-ingress.redisURL`. If you set only the top-level `redisURL`, Ambassador Edge Stack still uses the chart's Redis instance.
* **You already protect Redis yourself**, with `--requirepass` in `redis.containerArgs`, or with `REDIS_PASSWORD` or `REDIS_AUTH` in `emissary-ingress.env`. The chart leaves your configuration as it is.
* **You override `emissary-ingress.envRaw`** without the `REDIS_PASSWORD` and `REDIS_AUTH` entries from the chart's default value. The chart prints a warning. To turn on the password, add both entries to your `envRaw`: the rate limit service reads `REDIS_AUTH`, and rate limiting fails without it. The chart turns on the password only when `envRaw` refers to the chart's own `<release-fullname>-redis-auth` Secret.
* **You turn it off.** Set `redis.auth.enabled=false` to keep the previous behavior. The chart still creates an empty `<release-fullname>-redis-auth` Secret; also set `redis.auth.createSecret=false` to avoid it. This isn't recommended, because anyone who can reach Redis on the network can then read and change OAuth2 sessions and rate limit state.

Keep the following in mind:

* **If you enable `REDIS_PERSECOND`** and point `REDIS_PERSECOND_URL` at the Redis instance that the chart creates, also set `REDIS_PERSECOND_PASSWORD` and `REDIS_PERSECOND_AUTH` from the same Secret.
* **Ambassador Edge Stack reads the password only when its pods start.** After you change the password, turn `redis.auth.enabled` on or off (including by adding your own `REDIS_PASSWORD`, `REDIS_AUTH`, or `--requirepass`), or run `helm rollback` between revisions that use chart v8.15.0 or later, restart both deployments: `kubectl rollout restart -n <namespace> deployment/<release-fullname>-redis deployment/<release-fullname>`.
* **Switching an existing release from `redis.auth.createSecret=true` to `false`** leaves the chart's Secret in place, because of `helm.sh/resource-policy: keep`, and the chart stops managing it. Replace its `password` with your own or adopt it into the tool that now manages it, then restart Redis and Ambassador Edge Stack. With `createSecret=false`, the chart never changes the Secret, so if you later turn the password off, empty or delete the Secret yourself.
* **The password is stored in the Helm release record**, like any Secret that Helm manages. With Helm's default storage driver, the release record is itself a Secret, so only users who can read Secrets in the release namespace can see it.

{% hint style="warning" %}
The YAML manifests can't include a password that's unique to each installation, so the Redis instance that they create still runs without a password. Until you add one, anyone who can reach the Redis Service can read and change OAuth2 sessions and rate limit state. This includes any workload in the cluster, and anyone who can create a `Mapping` or `TCPMapping` that points at the Redis Service. If you install from the YAML manifests, add a password as described below, or move to the Helm chart.
{% endhint %}

In the 3.15.0 and later manifests, the Ambassador Edge Stack deployment reads `REDIS_PASSWORD` and `REDIS_AUTH` from an optional `edge-stack-redis-auth` Secret. To add a password to a YAML installation, first upgrade to the 3.15.0 or later manifests, then create the Secret, start Redis with it, and restart Ambassador Edge Stack:

```bash
kubectl create secret generic -n ambassador edge-stack-redis-auth --from-literal=password="$(openssl rand -hex 24)"
kubectl patch deployment -n ambassador edge-stack-redis --type=json -p '[
  {"op":"add","path":"/spec/template/spec/containers/0/env","value":[{"name":"REDIS_PASSWORD","valueFrom":{"secretKeyRef":{"name":"edge-stack-redis-auth","key":"password"}}}]},
  {"op":"add","path":"/spec/template/spec/containers/0/args","value":["--requirepass","$(REDIS_PASSWORD)"]}]'
kubectl rollout restart -n ambassador deployment/edge-stack
```

These commands use the `ambassador` namespace. Use the namespace that you installed into, such as `default` or `emissary` for those manifest variants. In the `-migration` manifests, the Ambassador Edge Stack deployment is named `aes`.

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
