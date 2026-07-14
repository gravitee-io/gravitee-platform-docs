---
description: Overview of Enterprise Edition licensing
---

# Enterprise Edition licensing

{% hint style="warning" %}
To run a Gravitee Enterprise Edition (EE) node, you must have a valid license file.
{% endhint %}

## Get an EE license

To get an EE license, email [contact@graviteesource.com](mailto:contact@graviteesource.com) requesting a license.

## Apply an EE license

You can provide the EE license data for a Gravitee EE product in the following ways:

- Using an environment variable
- Using a file
- Using Kubernetes to provide the environment variable or file

### Apply an EE license using an environment variable

Provide the content of the license file directly in `Base64` format using an environment variable called `license.key`:

1. Create a new secret from your Gravitee license data.
2. Update your deployment description and provide a new environment variable with the license data from a Kubernetes secret, as shown in the example below:

```yaml
spec:
  containers:
  - name: ONE_OF_GRAVITEE_EE_PRODUCTS
    image: GRAVITEE_IMAGE
    env:
    - name: license.key
      valueFrom:
        secretKeyRef:
          name: graviteeio-license
          key: license.key
          optional: false # same as default; "mysecret" must exist
```

For more information, see the [Kubernetes documentation](https://kubernetes.io/docs/tasks/inject-data-application/define-environment-variable-container).

### Apply an EE license using a file

By default, Gravitee looks for the EE license file inside the `GRAVITEE_HOME/license/license.key` folder. You can override this by using a property called `gravitee.license`.

How it works:

1. Gravitee first looks for the `license.key` environment variable.
2. If it can't find it, Gravitee looks at the `gravitee.license` property.
3. If the `gravitee.license` property isn't set, Gravitee tries to retrieve the key from the `GRAVITEE_HOME` folder.

### Provide an EE license using Kubernetes

Kubernetes allows you to mount the content of a special [Secret](https://kubernetes.io/docs/concepts/configuration/secret/) inside your pod. You can use this solution to provide the EE license file to Gravitee:

1. Create a `Secret` containing the EE license data. Make sure to name the key `license.key`.
2.  Mount this content into your pod using `Volumes`. The `mountPath` isn't unique and is different for each product, as follows:

    APIM:

    * Gateway: `/opt/graviteeio-gateway/license`
    * API: `/opt/graviteeio-management-api/license`

    AM:

    * Gateway: `/opt/graviteeio-am-gateway/license`
    * API: `/opt/graviteeio-am-management-api/license`

    AE:

    * `/opt/graviteeio-alert-engine/license`

For example:

```yaml
spec:
  containers:

# ...

    volumeMounts:
    - name: graviteeio-license
      mountPath: "/opt/graviteeio-management-api/license"
      readOnly: true
  volumes:
  - name: graviteeio-license
    secret:
      secretName: graviteeio-license
      optional: false # default setting; "mysecret" must exist
```

### Provide an EE license using Helm

You can use the solutions described above to modify existing resources that have already been deployed in the cluster. Alternatively, you can provide the license information using [Helm](https://helm.sh/), when installing or updating existing installations.

The example below shows the contents of a simple `values.yaml` file that you can use to provide the EE license data using Helm:

{% code title="values.yaml" %}
```yaml
api:

# ...

    env:
    - name: gravitee_services_notifier_enabled
      value: "true"
# ...

    extraVolumeMounts: |
      - name: graviteeio-license
        mountPath: /opt/graviteeio-management-api/license
        readOnly: true
    extraVolumes: |
      - name: graviteeio-license
        secret:
          secretName: graviteeio-license

gateway:

# ...

    env:
    - name: GIO_MIN_MEM
      value: 256m

# ...

    extraVolumeMounts: |
      - name: graviteeio-license
        mountPath: /opt/graviteeio-gateway/license
        readOnly: true
    extraVolumes: |
      - name: graviteeio-license
        secret:
          secretName: graviteeio-license
```
{% endcode %}

## When your license is ending

Thirty days before the end of the license, a daily `WARN` log is printed in the log file of the node to inform you that the license is ending.

To keep the nodes running, you must provide an updated license file. This file is reloaded silently by the node.

## License support

When running an enterprise node, a license file must be supplied to bootstrap the node.

When running the node within Docker, the license file must be passed with a volume as follows:

```sh
docker run  \
        -v license.key:/opt/graviteeio-gateway/license \
        --name api-gateway  \
        --detach  \
        graviteeio/apim-gateway:4.11.0
```
