---
description: Learn how to access and set up Gravitee Cockpit
---

# Access and setup

## Access Gravitee Cockpit

To get started with Gravitee Cockpit (GC), go to [https://cockpit.gravitee.io](https://cockpit.gravitee.io/), and click the **Register** button. Set up your account.

## Navigating Gravitee Cockpit

### Dashboard

After login, Gravitee Cockpit opens the dashboard, which displays some analytics about your account organizations, environments, and installations. You can access the dashboard at any time by clicking **Home** in the left-hand menu.

![cockpit add organizations or environments](https://docs.gravitee.io/images/cockpit/cockpit-add-organizations-or-environments.png)

In the Dashboard, you can create one or more organizations within your account and one or more environments within your organizations. Each environment can then be linked to existing APIM or AM installations.

* [Learn more about setting up your Cockpit hierarchy](../guides/set-up-your-gravitee-cloud-hierarchy.md)
* [Learn more about registering APIM and AM installations](../guides/register-installations.md)

### Hierarchy

You can click your organization name in the left-hand menu to access an interactive map of the organizational hierarchy associated with your account.

![cockpit dashboard](https://docs.gravitee.io/images/cockpit/cockpit-dashboard.png)

Click the settings icon ![cockpit settings icon](https://docs.gravitee.io/images/icons/cockpit-settings-icon.png) of any entity in the map to update its settings.

### API Management Free trial

If you want to sign up for Gravitee Cockpit in order to start an [enterprise API Management trail](https://documentation.gravitee.io/apim/overview/ee-vs-oss), head to [https://cockpit.gravitee.io/](https://cockpit.gravitee.io/), and enter in the required information to register.

You'll be taken to the Gravitee Cockpit setup flow. First, choose a **Company name**.

<figure><img src="../.gitbook/assets/Screen Shot 2023-07-19 at 8.38.13 AM.png" alt=""><figcaption><p>Set up your company</p></figcaption></figure>

Next, you'll have the option to choose either:

* **Quick setup**: automatically creates a Gravitee Cockpit account, a Gravitee organization and environment, and a free trial instance
* **Manual setup:** creates a Gravitee Cockpit instance, but then requires you to create and start a trial manually

We recommend the **Quick setup,** but do include instructions for starting a trial using the manual mode in the [Manual trial setup section](access-and-set-up.md#manual-trial-setup). The rest of this section assumes a **Quick setup.**

After you select Quick setup, select Continue, and then define your **Organization** and **Environment names**.

<figure><img src="../.gitbook/assets/Screen Shot 2023-07-19 at 8.42.47 AM.png" alt=""><figcaption><p>Define an Organization and Environment name</p></figcaption></figure>

Then, select **Complete setup.** At this point, Gravitee will handle trial set up. You'll be taken to the **Gravitee Cockpit Dashboard** while the trial initializes. This typically takes around 5 minutes.

<figure><img src="../.gitbook/assets/Screen Shot 2023-07-19 at 8.44.33 AM.png" alt=""><figcaption><p>Gravitee Cockpit Dashboard: trial initialization</p></figcaption></figure>

In the meantime, please feel free to check out the educational content. This content is useful for any team that's looking to find success with an enterprise APIM trial.

Once the trial is set up, you'll see the option to access your API Management trial both in the bottom left corner of the screen and in the top left block of your **Dashboard**. Select either to get started.

<figure><img src="../.gitbook/assets/Screen Shot 2023-07-19 at 8.46.28 AM.png" alt=""><figcaption><p>Gravitee Cockpit Dashboard: free trial</p></figcaption></figure>

### Try out the pre-configured trial walk throughs

Once you access your trial, you'll be brought to your Gravitee APIM trial environment. You'll have the option to follow pre-configured walk throughs that make use of a [Gravitee-built trial application](https://documentation.gravitee.io/apim/getting-started/tutorials), or explore APIM on your own. We recommend every team at least try the walk through first. To better assist you, we've documented the [free trial walk throughs in the Gravitee APIM free trial documentation.](https://documentation.gravitee.io/apim/getting-started/tutorials)

If, at any point, you want to contact sales to upgrade or book a demo, [you can do so here](https://www.gravitee.io/demo).

### Manual trial setup

If you choose the **Manual set up** option, you'll need to define your **Organization** and **Environment names**. When done, select **Complete setup.**

You'll be taken to the **Gravitee Cockpit Dashboard**.

<figure><img src="../.gitbook/assets/Screen Shot 2023-07-19 at 8.54.20 AM.png" alt=""><figcaption><p>Gravitee Cockpit Dashboard: manual setup</p></figcaption></figure>

To create a trial environment, select **Start your APIM trial** in the bottom left of the screen, and then select **Start my free trial** in the pop-up dialog.

Before initializing the trial, you'll need to select which **Organization** you want to link this trial to. Typically, this will be the **Organization** that you just created during Gravitee Cockpit registration.

From here, Gravitee will work on initializing your trial. Once initialized, we recommend exploring via the [pre-configured APIM trial walkthroughs.](access-and-set-up.md#try-out-the-pre-configured-trial-walk-throughs)
