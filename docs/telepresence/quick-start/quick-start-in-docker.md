---
noIndex: true
---

# Quick Start in Docker

## Telepresence in Docker Quick Start <a href="#telepresence-in-docker-quick-start" id="telepresence-in-docker-quick-start"></a>

This quickstart provides the fastest way to get an understanding of how [Telepresence](https://www.getambassador.io/products/telepresence) can speed up your development in Kubernetes within docker. It should take you about 5-10 minutes. You'll create a local cluster using Kind with a sample app installed, and use Telepresence to redirect traffic from a workload in your cluster to a local docker image.

{% hint style="info" %}
If you have already completed the standard Telepresence Quickstart and have a Kind demo cluster running, skip to step 3.
{% endhint %}

### Prerequisites

* You installed the Telepresence CLI.
* You installed and set up [`kubectl`](https://kubernetes.io/docs/tasks/tools/install-kubectl/) ([Linux](https://kubernetes.io/docs/tasks/tools/install-kubectl-linux/#verify-kubectl-configuration) / [macOS](https://kubernetes.io/docs/tasks/tools/install-kubectl-macos/#verify-kubectl-configuration) / [Windows](https://kubernetes.io/docs/tasks/tools/install-kubectl-windows/#verify-kubectl-configuration)).
* You installed [Docker](https://docs.docker.com/get-docker/).

### 1. Set up a local cluster with sample app

We provide [a repo](https://github.com/ambassadorlabs/telepresence-local-quickstart) that sets up a local cluster for you with the in-cluster Telepresence components and a sample app already installed. It does not need `sudo` or `Run as Administrator` privileges.

{% tabs %}
{% tab title="GNU/Linux" %}
```
# Clone the repo with submodules
git clone https://github.com/ambassadorlabs/telepresence-local-quickstart.git --recurse-submodules

# Change to the repo directory
cd telepresence-local-quickstart

# Run the Linux setup script
./linux-setup.sh
```
{% endtab %}

{% tab title="macOS" %}
```
# Clone the repo with submodules
git clone https://github.com/ambassadorlabs/telepresence-local-quickstart.git --recurse-submodules

# Change to the repo directory
cd telepresence-local-quickstart

# Run the macOS setup script
./macos-setup.sh
```
{% endtab %}

{% tab title="Windows" %}
```
# Clone the repo with submodules
git clone https://github.com/ambassadorlabs/telepresence-local-quickstart.git --recurse-submodules

# Change to the repo directory
cd .\telepresence-local-quickstart

# Run the Windows setup script
.\windows-setup.ps1
```
{% endtab %}
{% endtabs %}

### 2. Use Telepresence to connect your laptop to the cluster

1.  Connect to the cluster: `telepresence connect --docker --namespace <namespace>`

    ```
    $ telepresence connect --docker --namespace default

    Launching Telepresence User Daemon
    ...
    Connected to context default, namespace default (https://<cluster-public-IP>)
    ```
2.  Normally, Telepresence would provide cluster dns for your browser, but, in docker mode, the telepresence daemons are running inside docker; Telepresence is only providing cluster dns to that docker network. To open our app in a browser, we will need to use kubectl to connect to it. Port-forward a connection to the ingress in the demo cluster: `kubectl port-forward service/verylargejavaservice 8080:8080`

    ```
    $ kubectl port-forward service/verylargejavaservice 8080:8080

    Forwarding from 127.0.0.1:8080 -> 8080
    Forwarding from [::1]:8080 -> 8080
    ```
3. Open the app in your browser by typing `http://localhost:8080/` into the search bar.

You are connected to the VeryLargeJavaService, which talks to the DataProcessingService as an upstream dependency. The DataProcessingService in turn has a dependency on VeryLargeDatastore.

### 3. Route traffic from the cluster to your local application

Historically, when developing microservices with Kubernetes, your choices have been to run an entire set of services in a cluster or namespace just for you, and spend 15 minutes on every one-line change, pushing the code, waiting for it to build, waiting for it to deploy, etc. Or, you could run all 50 services in your environment on your laptop, and be deafened by the fans.

With Telepresence, you can _intercept_ traffic from a service in the cluster and route it to your laptop, effectively replacing the cluster version with your local development environment. This gives you back the fast feedback loop of local development, and access to your preferred tools like your favorite IDE or debugger. And you still have access to all the cluster resources via `telepresence connect`. Now you'll see this in action.

Next, we’ll create an intercept. An intercept is a rule that tells Telepresence where to send traffic. In this example, we will send all traffic destined for the DataProcessingService to the version of the DataProcessingService running locally instead:

1.  Start the intercept with the `intercept` command, setting the service name and port: `telepresence intercept --port <local port>:<service port> <workload name> --docker-run -- <docker run flags> <image name> <image flags>`

    ```
    $ telepresence intercept --port 3000:3000 dataprocessingservice --docker-run -- --rm datawire/dataprocessingservice:golang -c blue

    Using Deployment dataprocessingservice
     Intercept name    : dataprocessingservice
     State             : ACTIVE
     Workload kind     : Deployment
     Destination       : 127.0.0.1:3000
     Volume Mount Point: /var/folders/...
     Intercepting      : all TCP requests
    Welcome to the DataProcessingGoService!
    Color set to:  blue
    ```
2. Go to the frontend service again in your browser and refresh (if you closed the `port-forward` from step 3, you will have to re-start it). You will now see the <mark style="color:blue;">**blue**</mark> elements in the app.

{% hint style="success" %}
The frontend’s request to DataProcessingService is being **intercepted and rerouted** to the server on your laptop!&#x20;
{% endhint %}

{% hint style="info" %}
If you want to build an image and intercept to it, in one command, you can use the \`--docker-build\` flag instead of \`--docker-run\`.
{% endhint %}
