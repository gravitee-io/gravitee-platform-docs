---
noIndex: true
---

# Install/Uninstall the Traffic Manager

Telepresence uses a traffic manager to send/receive cloud traffic to the user. Telepresence uses [Helm](https://helm.sh) under the hood to install the traffic manager in your cluster. The `telepresence` binary embeds both `helm` and a helm-chart for a traffic-manager that is of the same version as the binary.

You can also use `helm` command directly, provided that you have it installed, see [Installing With Helm](install-uninstall-the-traffic-manager.md#install-the-traffic-manager-with-helm) for more details.

## Prerequisites

Before you begin, you need to have [Telepresence installed](install.md). In addition, you may need certain prerequisites depending on your cloud provider and platform. See the [cloud provider installation notes](cloud-provider-prerequisites.md) for more.

## Install the Traffic Manager

The telepresence cli can install the traffic manager for you. The basic install will install the same version as the client used.

1.  Install the Telepresence Traffic Manager with the following command:

    ```shell
    telepresence helm install
    ```

### Customizing the Traffic Manager.

For details on what the Helm chart installs and what can be configured, see the Helm chart [configuration on artifacthub](https://artifacthub.io/packages/helm/datawire/telepresence).

1. Create a values.yaml file with your config values.
2.  Run the `install` command with the `--values` flag set to the path to your values file:

    ```shell
    telepresence helm install --values values.yaml
    ```

    alternatively, provide values using the `--set` flag:

    ```shell
    telepresence helm install --set logLevel=debug
    ```

### Install into custom namespace

The Helm chart supports being installed into any namespace, not necessarily `ambassador`. Simply pass a different `namespace` argument to `telepresence helm install`. For example, if you wanted to deploy the traffic manager to the `staging` namespace:

```shell
telepresence helm install --namespace staging
```

This will create the namespace if it does not already exist. If you want to prevent that, you can pass `--create-namespace=false`.

Note that users of Telepresence will need to configure their kubeconfig to find this installation of the Traffic Manager:

```yaml
apiVersion: v1
clusters:
- cluster:
    server: https://127.0.0.1
    extensions:
    - name: telepresence.io
      extension:
        manager:
          namespace: staging
  name: example-cluster
```

See the [kubeconfig documentation](../technical-reference/laptop-side-configuration.md#manager) for more information.

## Upgrading/Downgrading the Traffic Manager.

1. Download the cli of the version of Telepresence you wish to use.
2.  Run the `upgrade` command. Optionally with `--values` and/or `--set` flags

    ```shell
    telepresence helm upgrade
    ```

    You can also use the `--reuse-values` or `--reset-values` to specify if previously installed values should be reused or reset.

## Uninstall

The telepresence cli can uninstall the traffic manager for you using the `telepresence helm uninstall`.

1.  Uninstall the Telepresence Traffic Manager and all the agents installed by it using the following command:

    ```shell
    telepresence helm uninstall
    ```

## RBAC

### Installing a namespace-scoped traffic manager

You might not want the Traffic Manager to have permissions across the entire kubernetes cluster, or you might want to be able to install multiple traffic managers per cluster (for example, to separate them by environment). In these cases, the traffic manager supports being installed with a namespace scope, allowing cluster administrators to limit the reach of a traffic manager's permissions.

For example, suppose you want a Traffic Manager that only works on namespaces `dev` and `staging`. To do this, create a `values.yaml` like the following:

```yaml
managerRbac:
  create: true
  namespaced: true
  namespaces:
  - dev
  - staging
```

This can then be installed via:

```shell
telepresence helm install --namespace staging -f ./values.yaml
```

**NOTE** Do not install namespace-scoped Traffic Managers and a global Traffic Manager in the same cluster, as it could have unexpected effects.

#### Namespace collision detection

The Telepresence Helm chart will try to prevent namespace-scoped Traffic Managers from managing the same namespaces. It will do this by creating a ConfigMap, called `traffic-manager-claim`, in each namespace that a given install manages.

So, for example, suppose you install one Traffic Manager to manage namespaces `dev` and `staging`, as:

```bash
telepresence helm install --namespace dev --set 'managerRbac.namespaced=true' --set 'managerRbac.namespaces={dev,staging}'
```

You might then attempt to install another Traffic Manager to manage namespaces `staging` and `prod`:

```bash
telepresence helm install --namespace prod --set 'managerRbac.namespaced=true' --set 'managerRbac.namespaces={staging,prod}'
```

This would fail with an error:

```
Error: rendered manifests contain a resource that already exists. Unable to continue with install: ConfigMap "traffic-manager-claim" in namespace "staging" exists and cannot be imported into the current release: invalid ownership metadata; annotation validation error: key "meta.helm.sh/release-namespace" must equal "prod": current value is "dev"
```

To fix this error, fix the overlap either by removing `staging` from the first install, or from the second.

#### Namespace scoped user permissions

Optionally, you can also configure user rbac to be scoped to the same namespaces as the manager itself. You might want to do this if you don't give your users permissions throughout the cluster, and want to make sure they only have the minimum set required to perform telepresence commands on certain namespaces.

Continuing with the `dev` and `staging` example from the previous section, simply add the following to `values.yaml` (make sure you set the `subjects`!):

```yaml
clientRbac:
  create: true

  # These are the users or groups to which the user rbac will be bound.
  # This MUST be set.
  subjects: {}
  # - kind: User
  #   name: jane
  #   apiGroup: rbac.authorization.k8s.io

  namespaced: true

  namespaces:
  - dev
  - staging
```

### Installing RBAC only

Telepresence Traffic Manager does require some [RBAC](../technical-reference/rbac.md) for the traffic-manager deployment itself, as well as for users. To make it easier for operators to introspect / manage RBAC separately, you can use `rbac.only=true` to only create the rbac-related objects. Additionally, you can use `clientRbac.create=true` and `managerRbac.create=true` to toggle which subset(s) of RBAC objects you wish to create.

## Ambassador Agent

The Ambassador Agent is installed alongside the Traffic Manager to report your services to Ambassador Cloud and give you the ability to trigger intercepts from the Cloud UI.

If you are already using the Emissary-Ingress or Edge-Stack you do not need to install the Ambassador Agent. When installing the `traffic-manager` you can add the flag `--set ambassador-agent.enabled=false`, to not include the ambassador-agent. Emissary and Edge-Stack both already include this agent within their deployments.

If your namespace runs with tight security parameters you may need to set a few additional parameters. These parameters are `securityContext`, `tolerations`, and `resources`. You can set these parameters in a `values.yaml` file under the `ambassador-agent` prefix to fit your namespace requirements.

### Adding an API Key to your Ambassador Agent

While installing the traffic-manager you can pass your cloud-token directly to the helm chart using the flag, `--set ambassador-agent.cloudConnectToken=<API_KEY>`. The [API Key](../technical-reference/client-reference/telepresence-login.md) will be created as a secret and your agent will use it upon start-up. Telepresence will not override the API key given via Helm.

### Creating a secret manually

The Ambassador agent watches for secrets with a name ending in `agent-cloud-token`. You can create this secret yourself. This API key will always be used.

```shell
kubectl apply -f - <<EOF
---
apiVersion: v1
kind: Secret
metadata:
  name: agent-cloud-token
  namespace: <agent namespace>
  labels:
    app.kubernetes.io/name: agent-cloud-token
data:
  CLOUD_CONNECT_TOKEN: <your api key>
EOF
```

## Running air-gapped

If your cluster is on an isolated network such that it cannot communicate with Ambassador Cloud, then some additional configuration is required. Check the technical reference on[ Air-gapped cluster](../technical-reference/cluster-side-configuration.md#air-gapped-cluster) for details.

## Install the Traffic Manager with Helm

The Telepresence Helm chart is hosted by Ambassador Labs and published at `https://app.getambassador.io`.

Start by adding this repo to your Helm client with the following command:

```shell
helm repo add datawire  https://app.getambassador.io
helm repo update
```

### Installing.

When you run the Helm chart, it installs all the components required for the Telepresence Traffic Manager.

1.  If you are installing the Telepresence Traffic Manager **for the first time on your cluster**, create the `ambassador` namespace in your cluster:

    ```shell
    kubectl create namespace ambassador
    ```
2.  Install the Telepresence Traffic Manager with the following command:

    ```shell
    helm install traffic-manager --namespace ambassador datawire/telepresence
    ```

### Upgrading/Downgrading.

Versions of the Traffic Manager Helm chart are coupled to the versions of the Telepresence CLI that they are intended for. Thus, for example, if you wish to use Telepresence `v2.18.1`, you'll need to install version `v2.18.1` of the Traffic Manager Helm chart.

Upgrading the Traffic Manager is the same as upgrading any other Helm chart; for example, if you installed the release into the `ambassador` namespace, and you just wished to upgrade it to the latest version without changing any configuration values:

```shell
helm repo up
helm upgrade traffic-manager datawire/telepresence --reuse-values --namespace ambassador
```

If you want to upgrade the Traffic-Manager to a specific version, add a `--version` flag with the version number to the upgrade command. For example: `--version v2.18.1`
