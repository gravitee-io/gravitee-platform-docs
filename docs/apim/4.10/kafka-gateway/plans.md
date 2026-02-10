## Configure mTLS Plans and Subscriptions in APIM

mTLS plans for native Kafka APIs work the same way as for HTTP/Message APIs. You can create an mTLS plan, publish it, and associate client certificates with subscriptions to authenticate Kafka clients.

### Create an mTLS Plan

1. Navigate to your Kafka API in APIM Console.
2. Select **Plans** from the API menu.
3. Click **Add new plan**.
4. Configure the plan:
    - **Name**: Enter a descriptive name for the mTLS plan.
    - **Security type**: Select **mTLS**.
5. Configure additional plan settings as needed (rate limits, quotas, etc.).
6. Click **Save**.
7. Publish the plan by clicking **Publish** in the plan list.

{% hint style="warning" %}
Kafka APIs can't have Keyless, mTLS, and authentication plans (OAuth2, JWT, API Key) published simultaneously. You must choose one security approach per API.
{% endhint %}

### Create an Application with a Client Certificate

Before subscribing to an mTLS plan, you must create an application that contains the client certificate.

1. Navigate to **Applications** in APIM Console.
2. Click **Add application**.
3. Enter the application details (name, description, etc.).
4. Click **Create**.
5. Open the application and navigate to **Subscriptions**.
6. In the **Client Certificate** section, upload the PEM-formatted client certificate that the Kafka client will use.
7. Click **Save**.

### Subscribe to the mTLS Plan

1. From the application, click **Subscribe to API**.
2. Select your Kafka API.
3. Select the mTLS plan you created.
4. Click **Subscribe**.
5. Wait for the subscription to be approved (if manual validation is required).

Once the subscription is active, the Gateway will authenticate Kafka clients using the certificate associated with the subscription. Metrics and analytics will correctly attribute traffic to the subscription, application, and plan.

### Runtime Behavior

When a Kafka client connects:

1. The client initiates a TLS connection and presents its client certificate.
2. The Gateway validates the certificate against known subscription certificates.
3. If the certificate matches a subscription, the connection is authorized.
4. The Gateway populates the execution context with plan, application, and subscription information.
5. Metrics reflect the resolved subscription instead of showing ANONYMOUS.