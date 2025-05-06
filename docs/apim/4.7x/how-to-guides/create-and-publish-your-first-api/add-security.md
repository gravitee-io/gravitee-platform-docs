# Add Security

## Add an API Key plan

To add an API Key plan, complete the following steps:

1. Select **APIs** from the APIM Console nav and click on your API.
2. Click **+ Add plan**, then select **API key**.&#x20;
3. Name your API plan and toggle **Auto validate subscription** to ON.
4. Click **Next**.&#x20;
5.  In the API Key authentication configuration screen, click **next**. \


    <figure><img src="../../.gitbook/assets/image (25).png" alt=""><figcaption></figcaption></figure>
6.  Click **Add plan**. \


    <figure><img src="../../.gitbook/assets/image (26).png" alt=""><figcaption></figcaption></figure>
7. Delete the default keyless plan. To delete the default keyless plan, navigate to **Default Keyless (UNSECURED)**, and then click the X.&#x20;
8. Click **Validate plans.**
9. In the Review your **API configuration screen**,  click **Save & Deploy API**.
10. Call the API. You recieve a 404 HTTP response, which shows that the API Key plan is in place.&#x20;

## Get the API Key

To test your API security, complete the following steps:

1. From the dashboard, click **Applications**.

<figure><img src="../../.gitbook/assets/image (27).png" alt=""><figcaption></figcaption></figure>

2. In the **Applications** screen, click **+ Add Application**.

<figure><img src="../../.gitbook/assets/image (28).png" alt=""><figcaption></figcaption></figure>

3. In the **Application creation** screen, add the following information:
   * Name&#x20;
   * Description&#x20;
4. In the **Security** section, click **Simple**.
5. Click **Create**.
6. In your Application's menu, click **Subscriptions**.&#x20;

<figure><img src="../../.gitbook/assets/image (29).png" alt=""><figcaption></figcaption></figure>

8. Click **+ Create a subscription**.
9. In the **Create a subscription** pop-up window, type the name of your API.
10. Select the API Key plan that you created.
11. Click **Create**. You now have an API key.

<figure><img src="../../.gitbook/assets/image (30).png" alt=""><figcaption></figcaption></figure>

10. Copy the API Key.

## Test your API Key

* In the header,  X-Gravitee-api-key - pass in the API key as an Auth header. It returns a 200 HTTP Response.
