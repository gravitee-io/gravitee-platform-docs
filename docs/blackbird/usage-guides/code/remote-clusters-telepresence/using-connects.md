# Using Connects

Blackbird cluster (powered by Telepresence) allows you to connect to a cluster from your local machine, so you can code locally and run the majority of your services within a remote Kubernetes cluster. Ultimately, this empowers you to develop services locally and still test integrations with dependent services or data stores running in the remote cluster.

After you establish a connection, you can intercept traffic from a Kubernetes service and route it to your local machine, enabling your local environment to function as if it were running in the cluster. For more information, see [using-intercepts.md](using-intercepts.md "mention").

## Prerequisites

* You downloaded the Blackbird CLI. For more information, see [#getting-started-with-the-blackbird-cli](../../../technical-reference/blackbird-cli/#getting-started-with-the-blackbird-cli "mention").
* You installed the Traffic Manager. For more information, see [using-the-traffic-manager.md](using-the-traffic-manager.md "mention").
* You can access a Kubernetes cluster using the Kubernetes CLI (kubectl) or the OpenShift CLI (oc).
* Your application is deployed in the cluster and accessible using a Kubernetes service.
* You have a local copy of the service ready to run on your local machine.

> **Note:** If you're a former Telepresence user who's now working in Blackbird, you must install the latest Blackbird CLI and Traffic Manager. Previously installed Traffic Managers from Telepresence are incompatible. For more information, see [#getting-started-with-the-blackbird-cli](../../../technical-reference/blackbird-cli/#getting-started-with-the-blackbird-cli "mention") and [using-the-traffic-manager.md](using-the-traffic-manager.md "mention").

## Connecting to a cluster

**To connect to a cluster:**

1.  Connect to your cluster.

    ```shell
    blackbird cluster connect
    ```
2.  Verify that you can reach the cluster's API or another internal service. For example, run a `curl` command to a service endpoint (e.g., `curl -vk https://kubernetes.default`). You should see the expected response or a 401 response. The 401 response is expected if you aren't providing credentials. If you can reach the endpoint, it was successful.

    > **Note:** After you set up your connection, you can create intercepts to route traffic for your cluster's service to your local machine. For more information, see [using-intercepts.md](using-intercepts.md "mention").
3.  When you're ready, end the connection and all daemons.

    ```shell
    blackbird cluster quit -s
    ```

    For detailed information about cluster commands and options, see [cluster.md](../../../technical-reference/blackbird-cli/cluster.md "mention") in the Blackbird CLI Reference.
