# Intercepts

When intercepting a service, the Telepresence Traffic Manager ensures that a Traffic Agent has been injected into the intercepted workload. The injection is triggered by a Kubernetes Mutating Webhook and will only happen once. The Traffic Agent is responsible for redirecting intercepted traffic to the developer's workstation.

An intercept is either global or personal.

#### Global intercept

This intercept will intercept all`tcp` and/or `udp` traffic to the intercepted service and send all of that traffic down to the developer's workstation. This means that a global intercept will affect all users of the intercepted service.

#### Personal intercept

This intercept will intercept specific HTTP requests, allowing other HTTP requests through to the regular service. The selection is based on http headers or paths, and allows for intercepts which only intercept traffic tagged as belonging to a given developer.

There are two ways of configuring an intercept:

* one from the [CLI](configure-intercept-using-cli.md) directly
* one from an [Intercept Specification](configure-intercept-using-specifications.md)

### Supported workloads

Kubernetes has various [workloads](https://kubernetes.io/docs/concepts/workloads/). Currently, Telepresence supports intercepting (installing a traffic-agent on) `Deployments`, `ReplicaSets`, `StatefulSets`, and `ArgoRollouts`.

{% hint style="info" %}
While many of our examples use Deployments, they would also work on other supported workload types.
{% endhint %}

#### Enable ArgoRollouts

In order to use `ArgoRollouts`, you must pass the Helm chart value `workloads.argoRollouts.enabled=true` when installing the traffic-manager. It is recommended to set the pod template annotation `telepresence.getambassador.io/inject-traffic-agent: enabled` to avoid creation of unwanted revisions.
