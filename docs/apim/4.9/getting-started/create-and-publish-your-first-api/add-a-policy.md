# Add a Policy

## Overview

This guide explains how to add the **Rate Limit** policy to your API.

## Prerequisites

* Complete the steps in [create-an-api.md](create-an-api.md "mention").
* Complete the steps in [add-security.md](add-security.md "mention").

## Add a policy to your API

1.  From the **Dashboard**, click **APIs**.

    <figure><img src="broken-reference" alt=""><figcaption></figcaption></figure>
2.  Click your API that you created in [create-an-api.md](create-an-api.md "mention").

    <figure><img src="broken-reference" alt=""><figcaption></figcaption></figure>
3.  Click **Policies**.

    <figure><img src="broken-reference" alt=""><figcaption></figcaption></figure>
4.  In the **Request phase**, click the **+** icon.

    <figure><img src="broken-reference" alt=""><figcaption></figcaption></figure>
5. In the **Search** field of the **Policies for Request phase** pop-up window, type **Rate Limit**.
6.  Navigate to Rate Limit, and then click **Select**.

    <figure><img src="broken-reference" alt=""><figcaption></figcaption></figure>
7. Navigate to the **Apply rate-limiting** section, and then add the following information:
   1. In the **Max requests** field, type the number **1**.
   2.  In the **Time duration** field, delete the number **1**, and then type the number **3**.

       <figure><img src="broken-reference" alt=""><figcaption></figcaption></figure>
8.  Click **Add policy**.

    <figure><img src="broken-reference" alt=""><figcaption></figcaption></figure>
9.  In the **Policies** screen, click **Save**.

    <figure><img src="broken-reference" alt=""><figcaption></figcaption></figure>
10. Click **Deploy API**.

    <figure><img src="broken-reference" alt=""><figcaption></figcaption></figure>
11. In the **Deploy your API** pop-up window, click **Deploy**.

    <figure><img src="broken-reference" alt=""><figcaption></figcaption></figure>

## Verification

*   Call your API twice within three seconds with the following command:

    ```
    curl -i "http://<gateway-domain>:<gateway-port>/<api-context-path>" \
      -H "X-Gravitee-Api-Key: <your-api-key>"
    ```

    * Replace `<gateway-domain>` with the hostname or IP address of your Gravitee gateway. For example, `localhost:` .
    * Replace `<gateway-port>` with the port where the gateway is exposed. For example, `8082` .
    * Replace `<api-context-path>` with the context path for your API. For example, myfirstapi.
    * Replace `<your-api-key>` with the API for your subscription that you created in [add-security.md](add-security.md "mention").

You receive the following message:

```json
{
    "message": "Rate limit exceeded! You reached the limit of 1 requests per 3 seconds",
    "http_status_code": 429
}
```

## Next steps

Add documentation to your API. For more information about adding documentation to your API, see [add-api-documentation.md](add-api-documentation.md "mention").
