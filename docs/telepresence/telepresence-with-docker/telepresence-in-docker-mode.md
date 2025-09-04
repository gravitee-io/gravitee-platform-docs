---
noIndex: true
---

# Telepresence in Docker Mode

Welcome to the quickstart guide for Telepresence Docker mode! In this hands-on tutorial, we will explore the powerful features of Telepresence and learn how to leverage Telepresence Docker mode to enhance local development and debugging workflows.

### What is Telepresence Docker Mode?

Telepresence Docker Mode enables you to run a single service locally while seamlessly connecting it to a remote Kubernetes cluster. This mode enables developers to accelerate their development cycles by providing a fast and efficient way to iterate on code changes without requiring admin access on their machines.

### Key Benefits

When using Telepresence in Docker mode, you can enjoy the following benefits:

1. **Simplified Development Setup**: Eliminate the need for admin access on your local machine, making it easier to set up and configure your development environment.
2. **Efficient Networking**: Address common networking challenges by seamlessly connecting your locally running service to a remote Kubernetes cluster. This enables you to leverage the cluster's resources and dependencies while maintaining a productive local development experience.
3. **Enhanced Debugging**: Gain the ability to debug your service in its natural environment, directly from your local development environment. This eliminates the need for complex workarounds or third-party applications to enable volume mounts or access remote resources.

### Prerequisites

1. [Kubectl](https://kubernetes.io/docs/tasks/tools/install-kubectl/). Kubectl is the official Kubernetes command-line tool. You will use it regularly to interact with your cluster, whether deploying applications, inspecting resources, or debugging issues.
2. [Telepresence 2.13 or latest](../install-telepresence/install.md). Telepresence is a command-line tool that lets you run a single service locally, while connecting that service to a remote Kubernetes cluster. You can use Telepresence to speed up local development and debugging.
3. [Docker Desktop](https://www.docker.com/get-started). Docker Desktop is a tool for building and sharing containerized applications and microservices. You'll use Docker Desktop to run a local development environment.

Now that we have a clear understanding of Telepresence Docker mode and its benefits, let's dive into the hands-on tutorial!

### 1. Get a free remote cluster

Telepresence connects your local workstation with a remote Kubernetes cluster. In this tutorial, we'll start with a pre-configured, remote cluster.

1. Get a free remote cluster. Sign in to [Ambassador Cloud](https://app.getambassador.io/cloud) to activate your demo cluster.
2. Go to the [Service Catalog](https://app.getambassador.io/cloud/services?_gl=1*1kujpqy*_gcl_au*MTQwMzk1MTk4Mi4xNzUyMDc1OTE5LjE2MTYxNTE4MjMuMTc1NjI2NTcyMC4xNzU2MjY1NzE5*_ga*MTYwNzAzMDY1NS4xNzUyMDc1OTE5*_ga_DJXYY7HYXH*czE3NTY0MDEyNDAkbzMzJGcxJHQxNzU2NDA1MzQ1JGo2MCRsMCRoMTY1MTI5MjUxNQ..) to see all the services deployed on your cluster. The Service Catalog gives you a consolidated view of all your services across development, staging, and production. After exploring the Service Catalog, continue with this tutorial to test the application in your demo cluster.

<figure><img src="../.gitbook/assets/00 tp 28.png" alt=""><figcaption></figcaption></figure>

### 2. Try the Emojivoto application

The remote cluster is running the Emojivoto application, which consists of four services. Test out the application:

1.  Go to the and vote for some emojis.

    \{% hint style="info" %\} If the link to the remote demo cluster doesn't work, make sure you don't have an **ad blocker** preventing it from opening. \{% endhint %\}
2. Now, click on the 🍩 emoji. You'll see that a bug is present, and voting 🍩 doesn't work. We're going to use Telepresence shortly to fix this bug, as everyone should be able to vote for 🍩!

{% hint style="success" %}
**Congratulations!** You've successfully accessed the Emojivoto application on your remote cluster.
{% endhint %}

### 3. Testing the fix in your local environment

We'll set up a development environment locally on your workstation. We'll then use [Telepresence](../technical-reference/running-telepresence-inside-a-container.md) to connect this local development environment to the remote Kubernetes cluster. To save time, the development environment we'll use is pre-packaged as a Docker container.

1.  Download and run the image for the service locally:

    ```bash
    docker run -d --name ambassador-demo --pull always -p 8083:8083 -p 8080:8080 --rm -it datawire/demoemojivoto
    ```

    \{% hint style="info" %\} If you're using Docker Desktop on Windows, you may need to [enable virtualization](https://docs.docker.com/desktop/troubleshoot-and-support/troubleshoot/topics/#virtualization) to run the container.\
    \> Make sure that ports **8080** and **8083** are free. If the Docker engine is not running, the command will fail and you will see **docker: unknown server OS** in your terminal. \{% endhint %\}

    The Docker container includes a copy of the Emojivoto application that fixes the bug. Visit the [leaderboard](http://localhost:8083/leaderboard) and notice how it is different from the leaderboard in your Kubernetes cluster.
2.  Now, stop the container by running the following command in your terminal:

    ```bash
    docker stop ambassador-demo
    ```

In this section of the quickstart, you ran the Emojivoto application locally. In the next section, you'll use Telepresence to connect your local development environment to the remote Kubernetes cluster.

### 4. Download the demo cluster config file

1. Download your demo cluster config file. This file contains the credentials you need to access your demo cluster.
2. Export the file's location to KUBECONFIG by running this command in your terminal:



\`\`\`\` \`\`\`bash export KUBECONFIG=/path/to/kubeconfig.yaml \`\`\` \`\`\`\` \{% endtab %\}

\{% tab title="macOS" %\}

````
```bash
export KUBECONFIG=/path/to/kubeconfig.yaml
```
````

\{% endtab %\}

\{% tab title="Windows" %\}

````
```bash
SET KUBECONFIG=/path/to/kubeconfig.yaml
```
````

\{% endtab %\} \{% endtabs %\}

You should now be able to run `kubectl` commands against your demo cluster.

3.  Verify that you can access the cluster by listing the app's services:

    ```
    $ kubectl get services -n emojivoto
    NAME            TYPE           CLUSTER-IP      EXTERNAL-IP     PORT(S)        AGE
    emoji-svc        ClusterIP   10.43.131.84    <none>        8080/TCP,8801/TCP   3h12m
    voting-svc       ClusterIP   10.43.32.184    <none>        8080/TCP,8801/TCP   3h12m
    web-svc          ClusterIP   10.43.105.110   <none>        8080/TCP            3h12m
    web-app          ClusterIP   10.43.53.247    <none>        80/TCP              3h12m
    web-app-canary   ClusterIP   10.43.8.90      <none>        80/TCP              3h12m
    ```

### 5. Enable Telepresence Docker mode

You can simply add the docker flag to any Telepresence command, and it will start your daemon in a container. Thus removing the need for root access, making it easier to adopt as an organization.

1.  Confirm that the Telepresence CLI is now installed, we expect to see that the daemons are not yet running: `telepresence status`

    ```
    $ telepresence status
      User Daemon: Not running
      Root Daemon: Not running
      Ambassador Cloud:
        Status      : Logged out
      Traffic Manager: Not connected
      Intercept Spec: Not running
    ```

    \{% hint style="info" %\} **macOS users:** If you receive an error when running Telepresence that the developer cannot be verified, open **System Preferences → Security & Privacy → General**. Click **Open Anyway** at the bottom to bypass the security block. Then retry the `telepresence status` command. \{% endhint %\}
2.  Log in to Ambassador Cloud:

    ```
    $ telepresence login
    ```
3.  Then, install the Helm chart and quit Telepresence:

    ```bash
    telepresence helm install
    telepresence quit -s
    ```
4.  Finally, connect to the remote cluster using Docker mode:

    ```
    $ telepresence connect --docker
    Connected to context default (https://default.cluster.bakerstreet.io)
    ```
5.  Verify that you are connected to the remote cluster by listing your Docker containers:

    ```
    $ docker ps
    CONTAINER ID   IMAGE                          COMMAND                  CREATED          STATUS          PORTS                        NAMES
    7a0e01cab325   datawire/telepresence:2.12.1   "telepresence connect…"   18 seconds ago   Up 16 seconds
    ```

This method limits the scope of the potential networking issues since everything stays inside Docker. The Telepresence daemon can be found under the name `tp-<your-context>` when listing your containers.

### 6. Set up your local development environment and make a global intercept

Start your intercept handler (interceptor) by targeting the daemon container --network=container:tp-`<your-context>`, and open the preview URL to see the traffic routed to your machine.

1.  Run the Docker container locally, by running this command inside your local terminal. The image is the same as the one you ran in the previous step (step 1) but this time, you will run it with the `--network=container:tp-<your-context>` flag:

    ```bash
    docker run -d --name ambassador-demo --pull always --network=container:tp-default --rm -it datawire/demoemojivoto
    ```
2.  With Telepresence, you can create global intercepts that intercept all traffic going to a service in your cluster and route it to your local environment instead/ Start a global intercept by running this command in your terminal:

    ```
    $ telepresence intercept web --docker --port 8080 --ingress-port 80 --ingress-host edge-stack.ambassador -n emojivoto --ingress-l5 edge-stack.ambassador --preview-url=true
      Using Deployment web
    Intercept name         : web-emojivoto
    State                  : ACTIVE
    Workload kind          : Deployment
    Destination            : 127.0.0.1:8080
    Service Port Identifier: http
    Volume Mount Point     : /var/folders/n5/rgwx1rvd40z3tt2v473h715c0000gp/T/telfs-2663656564
    Intercepting           : HTTP requests with headers
          'x-telepresence-intercept-id: 8ff55336-9127-43b7-8175-08c598699bdb:web-emojivoto'
    Preview URL            : https://unruffled-morse-4172.preview.edgestack.me
    Layer 5 Hostname       : edge-stack.ambassador
    ```

    \{% hint style="info" %\} Learn more about [intercepts](../technical-reference/intercepts/configure-intercept-using-cli.md) and how to use them. \{% endhint %\}### 7. Make a personal intercept

Personal intercepts allow you to be selective and intercept only some of the traffic to a service while not interfering with the rest of the traffic. This allows you to share a cluster with others on your team without interfering with their work.

1.  First, connect to telepresence docker mode again:

    ```
    $ telepresence connect --docker
    ```
2.  Run the docker container again:

    ```
    $ docker run -d --name ambassador-demo --pull always --network=container:tp-default --rm -it datawire/demoemojivoto
    ```
3.  Create a personal intercept by running this command in your terminal:

    ```
    $ telepresence intercept web --docker --port 8080 --ingress-port 80 --ingress-host edge-stack.ambassador -n emojivoto --ingress-l5 edge-stack.ambassador --preview-url=true
      Using Deployment web
    Intercept name         : web-emojivoto
    State                  : ACTIVE
    Workload kind          : Deployment
    Destination            : 127.0.0.1:8080
    Service Port Identifier: http
    Volume Mount Point     : /var/folders/n5/rgwx1rvd40z3tt2v473h715c0000gp/T/telfs-2663656564
    Intercepting           : HTTP requests with headers
          'x-telepresence-intercept-id: 8ff55336-9127-43b7-8175-08c598699bdb:web-emojivoto'
    Preview URL            : https://unruffled-morse-4172.preview.edgestack.me
    Layer 5 Hostname       : edge-stack.ambassador
    ```
4. Open the preview URL to see the traffic routed to your machine.
5.  To stop the intercept, run this command in your terminal:

    ```
    $ telepresence leave web-emojivoto
    ```

### What's Next?

You've intercepted a service in one of our demo clusters, now you can use Telepresence to [intercept a service in your own environment](../how-do-i.../intercept-a-service-in-your-own-environment.md)!
