# GitHub Actions

## Telepresence with GitHub Actions

Telepresence combined with [GitHub Actions](https://docs.github.com/en/actions) allows you to run integration tests in your continuous integration/continuous delivery (CI/CD) pipeline without the need to run any dependent service. When you connect to the target Kubernetes cluster, you can intercept traffic of the remote services and send it to an instance of the local service running in CI. This way, you can quickly test the bugfixes, updates, and features that you develop in your project.

You can [register here](https://app.getambassador.io/auth/realms/production/protocol/openid-connect/auth?client_id=telepresence-github-actions\&response_type=code\&code_challenge=qhXI67CwarbmH-pqjDIV1ZE6kqggBKvGfs69cxst43w\&code_challenge_method=S256\&redirect_uri=https://app.getambassador.io) to get a free Ambassador Cloud account to try the GitHub Actions for Telepresence yourself.

### GitHub Actions for Telepresence

Ambassador Labs has created a set of GitHub Actions for Telepresence that enable you to run integration tests in your CI pipeline against any existing remote cluster. The GitHub Actions for Telepresence are the following:

* **install**: Installs Telepresence in your CI server with latest version or the one specified by you.
* **login**: Logs into Telepresence and allows you to create a [personal intercept](../core-concepts/types-of-intercepts.md#personal-intercept). You'll need a Telepresence API key which you must set as an environment variable in your workflow. See the [acquiring an API key guide](../technical-reference/client-reference/telepresence-login.md#acquiring-an-api-key) for instructions on how to get one.
* **helm**: Installs the telepresence traffic manager in the cluster.
* **connect**: Connects to the remote target environment.
* **intercept**: Redirects traffic to the remote service to the version of the service running in CI so you can run integration tests.

Each action contains a post-action script to clean up resources. This includes logging out of Telepresence, closing the connection to the remote cluster, and stopping the intercept process. These post scripts are executed automatically, regardless of job result. This way, you don't have to worry about terminating the session yourself. You can look at the [GitHub Actions for Telepresence repository](https://github.com/datawire/telepresence-actions) for more information.

## Using Telepresence in your GitHub Actions CI pipeline

### Prerequisites

To enable GitHub Actions with telepresence, you need:

* A [Telepresence API KEY](../technical-reference/client-reference/telepresence-login.md#acquiring-an-api-key) and set it as an environment variable in your workflow.
* Access to your remote Kubernetes cluster, like a `kubeconfig.yaml` file with the information to connect to the cluster.
*   If your remote cluster already has Telepresence installed, you need to know whether Telepresence is installed [Cluster wide](../technical-reference/rbac.md#cluster-wide-telepresence-user-access) or [Namespace only](../technical-reference/rbac.md#namespace-only-telepresence-user-access). If telepresence is configured for namespace only, verify that your `kubeconfig.yaml` is configured to find the installation of the Traffic Manager. For example:

    ```yaml
    apiVersion: v1
    clusters:
    - cluster:
        server: https://127.0.0.1
        extensions:
        - name: telepresence.io
          extension:
            manager:
              namespace: traffic-manager-namespace
      name: example-cluster
    ```
* You need a GitHub Actions secret named `TELEPRESENCE_API_KEY` in your repository that has your Telepresence API key. See [GitHub docs](https://docs.github.com/en/github-ae@latest/actions/security-guides/using-secrets-in-github-actions#creating-secrets-for-a-repository) for instructions on how to create GitHub Actions secrets.
* You need a GitHub Actions secret named `KUBECONFIG_FILE` in your repository with the content of your `kubeconfig.yaml`).

### Using Telepresence in your GitHub Actions workflows

1.  In the `.github/workflows` directory create a new YAML file named `run-integration-tests.yaml` and modify placeholders with real actions to run your service and perform integration tests.

    ```yaml
      name: Run Integration Tests
      on:
        push:
          branches-ignore:
          - 'main'
      jobs:
        my-job:
          name: Run Integration Test using Remote Cluster
          runs-on: ubuntu-latest
          env:
            TELEPRESENCE_API_KEY: ${{ secrets.TELEPRESENCE_API_KEY }}
            KUBECONFIG_FILE: ${{ secrets.KUBECONFIG_FILE }}
            KUBECONFIG: /opt/kubeconfig
          steps:
          - name : Checkout
            uses: actions/checkout@v3
            with:
              ref: ${{ github.event.pull_request.head.sha }}
          #---- here run your custom command to start your local service
          #- name: Run local service for testing
          #  shell: bash
          #  run: ./run_local_service
          #----
          - name: Create kubeconfig file
            run: |
              cat <<EOF > /opt/kubeconfig
              ${{ env.KUBECONFIG_FILE }}
              EOF
          - name: Install Telepresence
            uses: datawire/telepresence-actions/install@v1.1
            with:
              version: 2.19.0 # Change the version number here according to the version of Telepresence in your cluster or omit this parameter to install the latest version
          # First you need to log in to Telepresence, with your api key
          - name: Login
            uses: datawire/telepresence-actions/login@v1.1
            with:
              telepresence_api_key: ${{ secrets.TELEPRESENCE_API_KEY }}
          - name: Install Traffic manager"
            uses: datawire/telepresence-actions/helm@v1.1
          - name: Telepresence connect
            uses: datawire/telepresence-actions/connect@v1.1
            with:
              namespace: namespacename-of-your-service
          - name: Intercept the service
            uses: datawire/telepresence-actions/intercept@v1.1
            with:
              service_name: service-name
              service_port: 8081:8080
              http_header: "x-telepresence-intercept-test=service-intercepted"
              print_logs: true # Flag to instruct the action to print out Telepresence logs and export an artifact with them
          #---- here run your custom command
          #- name: Run integrations test
          #  shell: bash
          #  run: ./run_integration_test
          #----
    ```

The previous is an example of a workflow that:

* Checks out the repository code.
* Has a placeholder step to run the service during CI.
* Creates the `/opt/kubeconfig` file with the contents of the `secrets.KUBECONFIG_FILE` to make it available for Telepresence.
* Installs Telepresence.
* Runs Telepresence Connect.
* Logs into Telepresence.
* Intercepts traffic to the service running in the remote cluster.
* Is a placeholder for an action that would run integration tests, such as one that makes HTTP requests to your running service and verifies it works while dependent services run in the remote cluster.

This workflow gives you the ability to run integration tests during the CI run against an ephemeral instance of your service to verify that any change that is pushed to the working branch works as expected. After you push the changes, the CI server will run the integration tests against the intercept. You can view the results on your GitHub repository, under the "Actions" tab.
