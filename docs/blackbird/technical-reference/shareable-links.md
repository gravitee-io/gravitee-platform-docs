---
description: Overview of Shareable Links.
noIndex: true
---

# Shareable Links

Blackbird generates shareable links (formerly called preview URLs) that replicate development environments for code run/code debug, mock, and deployment features in Blackbird. Shareable links are stable and globally available to allow you to work on a local copy of your service and share it with teammates to collaborate through pair programming. Anyone with a shareable link can access the environment, but you can secure the URLs with API keys.

Use shareable links when:

* Your team needs a shared development environment with a common set of services.
* You want to override a remote service with one running locally for development or testing.

## Prerequisites

Before using shareable links, ensure you meet the following requirements:

* You installed the Blackbird CLI. For more information, see [#getting-started-with-the-blackbird-cli](blackbird-cli/#getting-started-with-the-blackbird-cli "mention").
* You installed Docker. For more information, see [Get Docker](https://docs.docker.com/get-started/get-docker).

## Creating a shareable link

After you meet the prerequisites, use the following procedure to create the link.

> **Note:** This example uses `blackbird code run`, but you can also generate a shareable link using `blackbird code debug`, `blackbird mock create`, and `blackbird deployment create` commands.

**To create a shareable link:**

1.  Log into the Blackbird CLI.

    ```shell
    blackbird login
    ```
2.  Run `blackbird code run` to generate the shareable URL.

    ```shell
    blackbird code run <name> --context=STRING
    ```

    The command creates a local service and returns a URL that's accessible to anyone with the link.

### Shareable links and intercepts

Shareable links created with `blackbird code run` and `blackbird code debug` work with intercepts to redirect traffic to your local machine without affecting your production environment. For example, when you run `blackbird code run` on intercepted code, Blackbird launches a Docker instance and routes traffic from your shareable link to your local environment. Only shareable links route through your machine, so the rest of your cluster behaves normally.

You can access the endpoint your service normally uses. After the link is live, you can share it with a teammate to collaborate without affecting your production cluster.

## Securing a shareable link

You can secure shareable links using API keys. For more information, see [secure-instances-on-blackbird.md](secure-instances-on-blackbird.md "mention").
