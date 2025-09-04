---
hidden: true
noIndex: true
---

# Manage my Subscriptions

Ambassador Labs provides a variety of different subscription options depending on your needs. Whether you're working with a small team with a few developers or a company with a large number of services, Ambassador Labs has flexible subscription options, catering to the needs of both teams and individual developers, for you to choose from.

### Check or upgrade your subscription

In user settings, go to the **Subscription** section.

The Subscription section of the Settings page shows your current utilization of Ambassador Cloud and the limits of your plan. Teams Edition and Developer subscribers can see their payment history here as well. If you’re nearing any of the quota limits, you can upgrade your subscription tier on this page. To learn more about the upgrade process, see the [upgrade your plan section](manage-my-subscriptions.md#upgrade-your-plan) below.

<figure><img src=".gitbook/assets/00 tp 7.png" alt=""><figcaption></figcaption></figure>

### Quota types

Quota limits are applicable to subscriptions:

* Telepresence Connect Sessions: Number of telepresence connects performed to your clusters.
* Requests per Month: Requests per month (RPM) is the total number of HTTP requests made to Edge Stack in the calendar month. For multiple clusters, RPM is the sum of all requests of each cluster. RPM is calculated from usage snapshots sent by Edge Stack every hour.
* Connected Clusters: The Kubernetes clusters you have connected to the Ambassador Cloud app.<mark style="background-color:blue;">Legacy</mark>
* Requests per Second: Requests per second (RPS) is the maximum usage in the cluster between Rate Limited Traffic and Authenticated Traffic. For multiple clusters, RPS is the sum of the maximum usage of each cluster. RPS is calculated from a database snapshot sent by Edge Stack every 30 seconds.<mark style="background-color:blue;">Legacy</mark>
* Active Services: Active services are those which have had an action performed on them within the last 28 days. Actions include intercepts, rollouts, and mappings.<mark style="background-color:blue;">Legacy</mark>
* Team Members: Ambassador Cloud users who have accepted an invitation sent by you through the Members page in your account settings.<mark style="background-color:blue;">Legacy</mark>

#### Active Services <mark style="background-color:blue;">Legacy</mark>

You can see which of your services are counting against your subscription by clicking **view active services** in the Active Services panel. If you delete your service and recreate it with the same name and in the same namespace, it will still count as 1 active service.

The active services list shows the services that have had intercepts, rollouts, or mappings in your organization for the last 28 days.

<figure><img src=".gitbook/assets/00 tp 8.png" alt=""><figcaption></figcaption></figure>

### Quota limits

Once you've reached a quota limit, you need to upgrade your plan to add more Requests per Month or extend your connect time. When the quota limit is reached, the following message is displayed:

<figure><img src=".gitbook/assets/00 tp 9.png" alt=""><figcaption></figcaption></figure>

### Upgrade your plan

If a quota does not fit your requirements, click **upgrade** to increase your quotas.

This opens the following page:

<figure><img src=".gitbook/assets/00 tp 10.png" alt=""><figcaption></figcaption></figure>

Once you have identified a more suitable subscription plan, click on **Buy Now** to be redirected to the checkout page, or **Contact Us** to talk to us about the details of the Enterprise plan.

#### Example

For instance, the subscription page indicates a RPM quota, allowing up to 10,000 requests in the Lite plan. When you reach this limit, you have to upgrade your plan to raise the quota.

<figure><img src=".gitbook/assets/00 tp 11.png" alt=""><figcaption></figcaption></figure>
