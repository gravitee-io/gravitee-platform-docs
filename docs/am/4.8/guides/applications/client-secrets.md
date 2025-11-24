---
description: Overview of Client Secrets.
---

# Client Secrets

Gravitee AM supports enhanced client secret management, allowing for multiple secrets for each application and configurable expiration policies at both the domain level and application level. These features improve security and flexibility in managing client credentials.

## Multiple Client Secrets for each Application

### Overview

* **Multiple Secrets:** Each application can have multiple active client secrets. This facilitates secret rotation without downtime, as new secrets can be added before deprecating old secrets.
* **Management:** Secrets can be added, renewed, and revoked through the Gravitee AM UI Console or using the Management API.

### Use Cases

* **Secret Rotation:** Introduce a new secret while keeping the old one active to ensure uninterrupted service during rotation.
* **Environment Separation:** Assign different secrets for different environments under the same application. For example, development, staging, and production.
* **Third-Party Access:** Provide distinct secrets to third-party partners, allowing for individual revocation if necessary.

### Managing Secrets

You can manage secrets by adding, renewing, and deleting them from Application. Default limitation of client secrets for each Application is 10. You can override this in `gravitee.yml` like the following example:

```yaml
applications:
  secretsMax: 20
```

#### **Accessing Application Settings:**

1. Navigate to the **Applications** section in the Gravitee AM Console.
2. Select the application. that you want to configure.
3. Go to **Settings**, and select **Secrets & Certificates.**

#### **Adding a new secret:**

1.  Click **"+ New client secret"**.

    <figure><img src="../../.gitbook/assets/Screenshot 2025-06-02 at 11.56.31 (1).png" alt=""><figcaption><p>New client secret</p></figcaption></figure>
2.  Provide description of new secret.

    <div align="left"><figure><img src="../../.gitbook/assets/Screenshot 2025-06-02 at 11.57.31 (1).png" alt="" width="308"><figcaption><p>New client secret description</p></figcaption></figure></div>
3.  Copy generated secret.

    <div align="left"><figure><img src="../../.gitbook/assets/Screenshot 2025-06-02 at 11.57.49.png" alt="" width="305"><figcaption><p>New client secret - copy</p></figcaption></figure></div>
4. Click OK.

{% include "../../.gitbook/includes/am-secret-store.md" %}

#### **Renewing a secret:**

1. In the **Secrets & Certificates** tab, locate the secret to renew.
2.  Click **renew button** next to the corresponding secret.

    <figure><img src="../../.gitbook/assets/Screenshot 2025-06-02 at 12.32.24.png" alt=""><figcaption><p>Renew Client Secret</p></figcaption></figure>
3. Copy generated secret.\
   ![](<../../.gitbook/assets/Screenshot 2025-06-02 at 12.00.01.png>)
4. Click OK.

{% include "../../.gitbook/includes/am-secret-store.md" %}

#### Deleting a secret:

1. In the **Secrets & Certificates** tab, locate the secret that you want to delete.
2.  Click the **delete button** next to the corresponding secret.\\

    <figure><img src="../../.gitbook/assets/Screenshot 2025-06-02 at 12.32.45.png" alt=""><figcaption><p>Delete Client Secret</p></figcaption></figure>
3. Confirm that you want to delete the secret by entering secret description.\
   ![](<../../.gitbook/assets/Screenshot 2025-06-02 at 12.00.38.png>)

{% hint style="warning" %}
Revoked secrets are immediately invalidated and cannot be used for authentication.
{% endhint %}

## Configurable Client Secret Expiration

### **Domain-Level Configuration:**

* **Purpose:** Set a default expiration duration for all client secrets within a domain to enforce regular rotation.
* **Configuration Steps:**
  1. Navigate to the **Domain**.
  2.  Go to **Settings**, and then **Client Secrets.**

      <figure><img src="../../.gitbook/assets/Screenshot 2025-06-02 at 12.06.56.png" alt=""><figcaption><p>Domain Secret Settings</p></figcaption></figure>
  3. Enable client secret expiry.
  4. Set the **Expiry Time Unit** and **Expiry Time Duration**. For example, 3 months.
  5. Save the changes.

### **Application-Level Configuration:**

* **Purpose:** Override the domain-level expiration setting for specific applications requiring different policies.
* **Configuration Steps:**
  1. Navigate to the **Applications** section in the Gravitee AM Console.
  2. Select the desired application.
  3. Go to **Settings**, and then **Secrets & Certificates**.
  4.  Click **Settings**.

      <figure><img src="../../.gitbook/assets/Screenshot 2025-06-02 at 12.28.04 (1).png" alt=""><figcaption><p>Application Secret Settings</p></figcaption></figure>
  5. Toggle **Use Domain Rules**, and then and select **Expiry Time Unit** and **Expiry Time Duration**.\
     ![](<../../.gitbook/assets/image (10).png>)
  6. Save the changes.

### **Behavior:**

* When a new secret is generated or a existing secret is renewed, the expiration date is calculated based on the configured duration.
* When Expiry Time Unit is set to NONE in application settings, no policy is applied for new/renewed secrets in application and expiry time is not set.
* Expired secrets are automatically invalidated and cannot be used for authentication.

### **Best Practices:**

* **Regular Rotation:** Implement a rotation policy that aligns with your organization's security requirements.
* **Monitoring:** Regularly monitor set alerts about upcoming expirations.

## Monitoring Client Secret Expiration

Gravitee AM provides support for monitoring client secret expiration through customizable notifications, allowing proactive management of client credentials.

### Notification Events

#### Notifications can be triggered automatically in the following two scenarios:

* **Client Secret Expired**: A notification is sent when a client secret reaches its expiration date.
* **Upcoming Secret Expiration**: Periodic notifications can be sent ahead of time, based on a configurable cron schedule, to proactively manage client secrets approaching expiration.

These notifications facilitate timely renewal of client secrets and reduce the risk of authentication failures due to expired credentials.

For detailed instructions on configuring the notification mechanisms, refer to the [AM API configuration](../../getting-started/configuration/configure-am-api/#configure-notifications-on-certificates-and-client-secret-expiry) section.
