---
description: Overview of Intercepts.
noIndex: true
---

# Types of Intercepts

## No intercept

<figure><img src="../.gitbook/assets/00 tp 4.png" alt=""><figcaption></figcaption></figure>

This is the normal operation of your cluster without Telepresence.

## Global intercept

<figure><img src="../.gitbook/assets/00 tp 5.png" alt=""><figcaption></figcaption></figure>

**Global intercepts** replace the Kubernetes "Orders" service with the Orders service running on your laptop. The users see no change, but with all the traffic coming to your laptop, you can observe and debug with all your dev tools.

#### Creating and using global intercepts

1.  Creating the intercept: Intercept your service from your CLI:

    ```shell
    telepresence intercept SERVICENAME --http-header=all
    ```

    {% hint style="info" %} Make sure your current kubectl context points to the target cluster. If your service is running in a different namespace than your current active context, use or change the `--namespace` flag. {% endhint %}
2.  Using the intercept: Send requests to your service:

    All requests will be sent to the version of your service that is running in the local development environment.

## Personal intercept

**Personal intercepts** allow you to be selective and intercept only some of the traffic to a service while not interfering with the rest of the traffic. This allows you to share a cluster with others on your team without interfering with their work.

Personal intercepts are subject to different plans. To read more about their capabilities & limits, see the [subscription management page](../manage-my-subscriptions.md).

<figure><img src="../.gitbook/assets/00 tp 6.png" alt=""><figcaption></figcaption></figure>

In the illustration above, <mark style="color:red;">**red**</mark> requests are being made by Developer 2 on their laptop and the <mark style="color:green;">**green**</mark> are made by a teammate, Developer 1, on a different laptop.

Each developer can intercept the Orders service for their requests only, while sharing the rest of the development environment.

#### Creating and using personal intercepts

1.  Creating the intercept: Intercept your service from your CLI:

    ```shell
    telepresence intercept SERVICENAME --http-header=Personal-Intercept=126a72c7-be8b-4329-af64-768e207a184b
    ```

    We're using `Personal-Intercept=126a72c7-be8b-4329-af64-768e207a184b` as the header for the sake of the example, but you can use any `key=value` pair you want, or `--http-header=auto` to have it choose something automatically.

    {% hint style="info" %} Make sure your current kubect context points to the target cluster. If your service is running in a different namespace than your current active context, use or change the `--namespace` flag. {% endhint %}
2.  Using the intercept: Send requests to your service by passing the HTTP header:

    ```http
    Personal-Intercept: 126a72c7-be8b-4329-af64-768e207a184b
    ```

    {% hint style="info" %} Need a browser extension to modify or remove an HTTP-request-headers?

    [Chrome](https://chrome.google.com/webstore/detail/modheader/idgpnmonknjnojddfkpgkljpfnnfcklj) | [Firefox](https://addons.mozilla.org/firefox/addon/modify-header-value/) {% endhint %}3. Using the intercept: Send requests to your service without the HTTP header:

    Requests without the header will be sent to the version of your service that is running in the cluster. This enables you to share the cluster with a team!

#### Intercepting a specific endpoint

It's not uncommon to have one service serving several endpoints. Telepresence is capable of limiting an intercept to only affect the endpoints you want to work with by using one of the `--http-path-xxx` flags below in addition to using `--http-header` flags. Only one such flag can be used in an intercept and, contrary to the `--http-header` flag, it cannot be repeated.

The following flags are available:

| Flag                          | Meaning                                                          |
| ----------------------------- | ---------------------------------------------------------------- |
| `--http-path-equal <path>`    | Only intercept the endpoint for this exact path                  |
| `--http-path-prefix <prefix>` | Only intercept endpoints with a matching path prefix             |
| `--http-path-regex <regex>`   | Only intercept endpoints that match the given regular expression |

**Examples:**

1.  A personal intercept using the header "Coder: Bob" limited to all endpoints that start with "/api':

    ```shell
    telepresence intercept SERVICENAME --http-path-prefix=/api --http-header=Coder=Bob
    ```
2.  A personal intercept using the auto generated header that applies only to the endpoint "/api/version":

    ```shell
    telepresence intercept SERVICENAME --http-path-equal=/api/version --http-header=auto
    ```

    or, since `--http-header=auto` is the implicit when using `--http` options, just:

    ```shell
    telepresence intercept SERVICENAME --http-path-equal=/api/version
    ```
3.  A personal intercept using the auto generated header limited to all endpoints matching the regular expression "(staging-)?api/.\*":

    ```shell
    telepresence intercept SERVICENAME --http-path-regex='/(staging-)?api/.*'
    ```
