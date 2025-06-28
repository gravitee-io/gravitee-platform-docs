# Add a Policy

## Add a policy to your API

1.  From the dashboard, click **APIs**.\


    <figure><img src="../../.gitbook/assets/image (32).png" alt=""><figcaption></figcaption></figure>
2.  Click the API that you created.\
    &#x20;

    <figure><img src="../../.gitbook/assets/image (33).png" alt=""><figcaption></figcaption></figure>
3.  Click **Policies**. \


    <figure><img src="../../.gitbook/assets/image (34).png" alt=""><figcaption></figcaption></figure>
4. In the request phase, click the **+** icon.
5. In the Policies for Request phase pop-up window, search for **Rate Limit**
6.  Navigate to Rate Limit, and then click **Select**.\


    <figure><img src="../../.gitbook/assets/image (35).png" alt=""><figcaption></figcaption></figure>
7.  Navigate to the **Apply rate-limiting** section, and then in the **Max requests** field, type three. \
    \


    <figure><img src="../../.gitbook/assets/image (36).png" alt=""><figcaption></figcaption></figure>
8. Click **Add policy**.

## Test your API's policy&#x20;

* Call your API 4 times and see the following response:

```json
{
    "message": "Rate limit exceeded! You reached the limit of 1 requests per 3 seconds",
    "http_status_code": 429
}
```
