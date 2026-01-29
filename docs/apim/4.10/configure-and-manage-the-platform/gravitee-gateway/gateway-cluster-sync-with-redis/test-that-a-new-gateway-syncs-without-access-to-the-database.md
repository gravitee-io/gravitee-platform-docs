---
hidden: true
noIndex: true
---

# Test that a new Gateway syncs without access to the database

## Overview&#x20;

## Prerequisites&#x20;

* Complete the steps in [.](./ "mention").
* Deploy an API

## Test the sync

1. Start all your services expect for the secondary Gateway using the following command:

```
export APIM_REGISTRY=graviteeio.azurecr.io && export APIM_VERSION=master-latest && docker compose up -d redis-stack mongodb elasticsearch gateway_primary management_api management_ui
```

<figure><img src="../../../.gitbook/assets/unknown (3).png" alt=""><figcaption></figcaption></figure>

2. Deploy an API to your Gateway. For more information about deploying a an API, see [create-and-configure-apis](../../../create-and-configure-apis/ "mention").
3.  Call your API using the following command:<br>

    ```
    Curl http://localhost:8082/testMukul
    ```

    \
    You receive a 200 response.
4.  Verify that your primary Gateway wrote to your redis stack using the following command:<br>

    ```
    ```

    \
    You see the following output:

<figure><img src="../../../.gitbook/assets/unknown (4).png" alt=""><figcaption></figcaption></figure>

5.  Stop the the Primary Gateway and your database using the following command:<br>

    ```
    ```
6.  Add a new gateway using the following command:<br>

    ```
    ```

<figure><img src="../../../.gitbook/assets/unknown (5).png" alt=""><figcaption></figcaption></figure>

## Verification

Call your API using the following command:

```
Curl http://localhost:8082/testMukul
```

\
You receive a 200 response.<br>

