---
hidden: true
noIndex: true
---

# Test that a new Gateway in a cluster user bridge syncs if the bridge crashes



## Overview&#x20;

## Prerequisites&#x20;

## Test the Gateway sync

1.  Start the bridge Gateway server and client Gateway using the following commandd:<br>

    ```shellscript
    export APIM_REGISTRY=graviteeio.azurecr.io && export APIM_VERSION=master-latest && docker compose up -d redis-stack mongodb elasticsearch gateway_server gateway_client management_api management_ui
    ```
2. Deploy an API to the Gateway. For more information about creating an API, see [create-and-configure-apis](../../../create-and-configure-apis/ "mention").
3.  Call your API using the following command:<br>

    ```
    Curl http://localhost:18092/_bridge/apis
    ```

    \
    You see the following response:<br>

    ```
    ```
4.  Verify Redis using the following command:<br>

    ```
    ```

    \
    You see the following response:<br>

    ```
    ```
5.  Stop the bridge and mongodb using the following command:<br>

    ```
    ```
6.  Add a new Gateway using the following command:<br>

    ```
    ```

The new Gateway syncs with Redis. Here is an example output:<br>

<figure><img src="../../../.gitbook/assets/unknown (17).png" alt=""><figcaption></figcaption></figure>

## Verification

*   Call an API with the new Gateway using the following command:<br>

    ```
    // Some code
    ```
