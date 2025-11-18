---
noIndex: true
---

# Quick Start

## Telepresence Quick Start

### Overview

This quickstart provides the fastest way to get an understanding of how [Telepresence](https://www.getambassador.io/products/telepresence) can speed up your development in Kubernetes. It should take you about 5-10 minutes. You'll create a local cluster using Kind with a sample app installed, and use Telepresence to

* access services in the cluster directly from your laptop
* make changes locally and see those changes immediately in the cluster

Then we'll point you to some next steps you can take, including trying out collaboration features and trying it in your own infrastructure.

### Prerequisites

* You installed the Telepresence CLI.
* You installed and set up [`kubectl`](https://kubernetes.io/docs/tasks/tools/install-kubectl/) ([Linux](https://kubernetes.io/docs/tasks/tools/install-kubectl-linux/#verify-kubectl-configuration) / [macOS](https://kubernetes.io/docs/tasks/tools/install-kubectl-macos/#verify-kubectl-configuration) / [Windows](https://kubernetes.io/docs/tasks/tools/install-kubectl-windows/#verify-kubectl-configuration)).
* You installed [Docker](https://docs.docker.com/get-docker/).
* The sample application instructions default to Python, which is pre-installed on MacOS and Linux. If you're using Windows and don't have Python installed, you can install it from the [official Python site](https://www.python.org/downloads/). There are also instructions for NodeJS, Java and Go if you already have those installed and prefer to work in them.

### Set up a local cluster with sample app

We provide [a repo](https://github.com/ambassadorlabs/telepresence-local-quickstart) that sets up a local cluster for you with the in-cluster Telepresence components and a sample app already installed. It does not need `sudo` or `Run as Administrator` privileges.

{% tabs %}
{% tab title="GNU/Linux" %}
```shell
# Clone the repo with submodules
git clone https://github.com/ambassadorlabs/telepresence-local-quickstart.git --recurse-submodules

# Change to the repo directory
cd telepresence-local-quickstart

# Run the Linux setup script
./linux-setup.sh
```
{% endtab %}

{% tab title="macOS" %}
```shell
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
cd .\telepresence-local-quickstart\

# Run the Windows setup script
.\windows-setup.ps1
```
{% endtab %}
{% endtabs %}

### Use Telepresence to connect your laptop to the cluster

Telepresence connects your local workstation to a namespace in your remote Kubernetes cluster, allowing you to talk to cluster resources like your laptop is in the selected namespace of the cluster. Intercepts can only be created in the selected namespace.

{% hint style="info" %}
The first time you run a Telepresence command you will be prompted to create an [Ambassador Labs](https://getambassador.io) account. Creating an account is completely free, takes a few seconds and can be done through accounts you already have, like GitHub and Google.
{% endhint %}

1.  Connect to the cluster: `telepresence connect --namespace default`

    ```
    $ telepresence connect --namespace default

    Launching Telepresence User Daemon
    Launching Telepresence Root Daemon
    ...
    Connected to context default, namespace default (https://<cluster-public-IP>)
    ```



    {% hint style="info" %}
    macOS users: If you receive an error when running Telepresence that the developer cannot be verified, open\
    **System Preferences → Security & Privacy → General**.\
    Click **Open Anyway** at the bottom to bypass the security block. Then retry the `telepresence connect` command.
    {% endhint %}


2.  Now we'll test that Telepresence is working properly by accessing a service running in the cluster. Telepresence has merged your local IP routing tables and DNS resolution with the clusters, so you can talk to the cluster in its DNS language and to services on their cluster IP address.\
    Open up a browser and go to `http://verylargejavaservice.default:8080`. As you can see you've loaded up a dashboard showing the architecture of the sample app.\


    <figure><img src=".gitbook/assets/00 tp 1.png" alt=""><figcaption></figcaption></figure>

You are connected to the VeryLargeJavaService, which talks to the DataProcessingService as an upstream dependency. The DataProcessingService in turn has a dependency on VeryLargeDatastore. You were able to connect to it using the cluster DNS name thanks to Telepresence.

### Run the sample application locally

We'll take on the role of a DataProcessingService developer. We want to be able to connect to that big test database that everyone has that dates back to the founding of the company and has all the critical test scenarios and is too big to run locally. In the other direction, VeryLargeJavaService is developed by another team and we need to make sure with each change that we are being good upstream citizens and maintaining valid contracts with that service.

{% hint style="info" %}
Confirm first that nothing is running locally on port 3000! If `curl localhost:3000` returns `Connection refused` then you should be good to go.
{% endhint %}

{% tabs %}
{% tab title="Python" %}
To run the DataProcessingService locally:

1. Change into the repo directory, then into DataProcessingService: `cd edgey-corp-python/DataProcessingService/`
2. Install the dependencies and start the Python server: `pip install flask requests && python app.py`
3. In a **new terminal window**, curl the service running locally to confirm it’s set to **blue**: `curl localhost:3000/color`

```
$ pip install flask requests && python app.py

Collecting flask
...
Welcome to the DataServiceProcessingPythonService!
...


$ curl localhost:3000/color

"blue"
```
{% endtab %}

{% tab title="NodeJS" %}
To run the DataProcessingService locally:

1. Change into the repo directory, then into DataProcessingService: `cd edgey-corp-nodejs/DataProcessingService/`
2. Install the dependencies and start the NodeJS server: `npm install && npm start`
3. In a **new terminal window**, curl the service running locally to confirm it’s set to **blue**: `curl localhost:3000/color`

```
$ npm install && npm start

added 170 packages, and audited 171 packages in 597ms
...
Welcome to the DataServiceProcessingNodeService!
...


$ curl localhost:3000/color

"blue"
```
{% endtab %}

{% tab title="Java" %}
To run the DataProcessingService locally:

1. Change into the repo directory, then into DataProcessingService: `cd edgey-corp-java/DataProcessingService/`
2. Install the dependencies and start the Java server: `mvn spring-boot:run`
3. In a **new terminal window**, curl the service running locally to confirm it’s set to **blue**: `curl localhost:3000/color`

```
$ mvn spring-boot:run

[INFO] Scanning for projects...
...
INFO 49318 --- [  restartedMain] g.d.DataProcessingServiceJavaApplication : Starting DataProcessingServiceJavaApplication using Java
...


$ curl localhost:3000/color

"blue"
```
{% endtab %}

{% tab title="Go" %}
To run the DataProcessingService locally:

1. Change into the repo directory, then into DataProcessingService: `cd edgey-corp-go/DataProcessingService/`
2. Install the dependencies and start the Go server: `go get github.com/pilu/fresh && go install github.com/pilu/fresh && fresh`
3. In a **new terminal window**, curl the service running locally to confirm it’s set to **blue**: `curl localhost:3000/color`

```
$ go get github.com/pilu/fresh && go install github.com/pilu/fresh && fresh

12:24:13 runner      | InitFolders
...
12:24:14 app         | Welcome to the DataProcessingGoService!
...


$ curl localhost:3000/color

"blue"
```
{% endtab %}
{% endtabs %}

{% hint style="success" %}
**Victory**, your local server is running a-ok!
{% endhint %}

### 5. Route traffic from the cluster to your local application

Historically, when developing microservices with Kubernetes, your choices have been to run an entire set of services in a cluster or namespace just for you, and spend 15 minutes on every one-line change, pushing the code, waiting for it to build, waiting for it to deploy, etc. Or, you could run all 50 services in your environment on your laptop, and be deafened by the fans.

With Telepresence, you can _intercept_ traffic from a service in the cluster and route it to your laptop, effectively replacing the cluster version with your local development environment. This gives you back the fast feedback loop of local development, and access to your preferred tools like your favorite IDE or debugger. And you still have access to all the cluster resources via `telepresence connect`. Now you'll see this in action.

Look back at your browser tab looking at the app dashboard. You see the EdgyCorp WebApp with a <mark style="color:green;">**green**</mark> title and <mark style="color:green;">**green**</mark> pod in the diagram. The local version of the code has the UI color set to <mark style="color:blue;">**blue**</mark> instead of <mark style="color:green;">**green**</mark>.

Next, we’ll create an intercept. An intercept is a rule that tells Telepresence where to send traffic. In this example, we will send all traffic destined for the DataProcessingService to the version of the DataProcessingService running locally instead:

1.  Start the intercept with the `intercept` command, setting the service name and port: `telepresence intercept dataprocessingservice --port 3000`

    ```
    $ telepresence intercept dataprocessingservice --port 3000

    Using Deployment dataprocessingservice
      Intercept name    : dataprocessingservice
      State             : ACTIVE
      Workload kind     : Deployment
      Destination       : 127.0.0.1:3000
      Intercepting      : all TCP requests
    ```
2. Go to the frontend service again in your browser and refresh. You will now see the <mark style="color:blue;">**blue**</mark> elements in the app.

{% hint style="success" %}
The frontend’s request to DataProcessingService is being **intercepted and rerouted** to the Python server on your laptop!
{% endhint %}

### 6. Make a code change

We’ve now set up a local development environment for the DataProcessingService, and we’ve created an intercept that sends traffic in the cluster to our local environment. We can now combine these two concepts to show how we can quickly make and test changes.

{% tabs %}
{% tab title="Python" %}
To update the color:

1. Open `edgey-corp-python/DataProcessingService/app.py` in your editor and change `DEFAULT_COLOR` on line 15 from `blue` to `orange`. Save the file and the python server will auto reload.
2. Now, visit `http://verylargejavaservice:8080` again in your browser and refresh. You will now see the <mark style="color:orange;">**orange**</mark> elements in the application.
{% endtab %}

{% tab title="NodeJS" %}
To update the color:

1. Open `edgey-corp-nodejs/DataProcessingService/app.js` in your editor and change line 6 from `blue` to `orange`. Save the file and the Node server will auto reload.
2. Now, visit `http://verylargejavaservice:8080` again in your browser. You will now see the <mark style="color:orange;">**orange**</mark> elements in the application.
{% endtab %}

{% tab title="Java" %}
To update the color:

1. Open `edgey-corp-java/DataProcessingService/src/main/resources/application.properties` in your editor and change `app.default.color` on line 2 from `blue` to `orange`. Save the file then stop and restart your Java server.
2. Now, visit `http://verylargejavaservice:8080` again in your browser. You will now see the <mark style="color:orange;">**orange**</mark> elements in the application.
{% endtab %}

{% tab title="Go" %}
To update the color:

1. Open `edgey-corp-go/DataProcessingService/main.go` in your editor and change `var color string` from `blue` to `orange`. Save the file and the Go server will auto reload.
2. Now, visit `http://verylargejavaservice:8080` again in your browser. You will now see the <mark style="color:orange;">**orange**</mark> elements in the application.
{% endtab %}
{% endtabs %}

{% hint style="success" %}
We’ve just shown how we can edit code locally, and **immediately** see these changes in the cluster.\
Normally, this process would require a container build, push to registry, and deploy.\
With Telepresence, these changes happen instantly.
{% endhint %}
