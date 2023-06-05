---
description: The administrator's guide to the developer portal
---

# Configuration

## Introduction

Configuration of the developer portal takes place through the management UI **Settings** page as highlighted in the image below.&#x20;

<figure><img src="../../../.gitbook/assets/dev_portal_settings.png" alt=""><figcaption><p>Developer portal settings</p></figcaption></figure>

The developer portal settings can be broken into the following major categories:

* General Settings
* User sign-up and support
* Layout and theme customization
* Documentation

## General settings

Select the **Settings** tab in the secondary sidebar and scroll down to the **Portal** subheader. As shown in the arcade above, you have the following configuration options:

* **Api-key Header:** Modify the `api-key` header shown in the developer portal's CURL commands

{% hint style="warning" %}
Note, this only impacts the developer portal's UI. You must modify the YAML configuration to impact the gateway.
{% endhint %}

* **Portal URL:** Provide the URL of the developer portal. This will add a link to the developer portal on the top navigation bar of the management UI as shown in the image below. Additionally, the [theme editor](./#theme-customization) will have a live preview of the developer portal.

<figure><img src="../../../.gitbook/assets/dev_portal_link.png" alt=""><figcaption><p>Link to developer portal from management UI</p></figcaption></figure>

* **Override homepage title:** Activating this toggle allows you to change the developer portal title from "Unleash the power of your APIs." to a custom title
* **Options**
  * **Use Tiles Mode:** Sets the default all APIs view to tiles as opposed to a list view
  * **Activate Support:** Adds a **Contact** and **Tickets** tab to each API.  Email must be configured as detailed in the [Email configuration](./#email-notifications) section for the contact form to work
  * **Activate Rating:** Allow API consumers to leave written reviews and ratings
  * **Force user to fill comment:** Requires all subscription requests to have a comment
  * **Allow User Registration:** Allow API consumers to create an account from the developer portal. Email must be configured as detailed in the [Email configuration](./#email-notifications) section for registration to work.
    * **Enable automatic validation:** Automatically approve all accounts created on the developer portal
  * **Add Google Analytics:** Add a Google Analytics tracking ID to the developer portal
  * <mark style="color:yellow;">**Allow Upload Images:**</mark> <mark style="color:yellow;"></mark> <mark style="color:yellow;"></mark><mark style="color:yellow;">Unknown</mark>
* **OpenAPI Viewers:** Select the viewer you would like to use to display your API documentation
* **Schedulers:** Configure the frequency the developer portal runs background tasks such as syncing data and sending/receiving notifications
* <mark style="color:yellow;">**Documentation:**</mark> <mark style="color:yellow;"></mark><mark style="color:yellow;">Unknown</mark>

{% hint style="info" %}
All of the general settings can be overridden in the `gravitee.yaml` file as detailed in the Configuration section.
{% endhint %}

## User sign-up and support

Now, in the previous section we simulated internal exposure of our API by using the same admin account for both the API producer and API consumer. However, external exposure necessitates the ability to create new accounts which requires some additional configuration. We’ll walk you through how to set that up.

The ability to create new user accounts has [two requirements](https://docs.gravitee.io/apim/3.x/apim\_consumerguide\_create\_account.html#prerequisites):

1. the “Allow User Registration” option enabled in settings
2. email [SMTP (simple mail transfer protocol) configuration 1](https://docs.gravitee.io/apim/3.x/apim\_installguide\_rest\_apis\_configuration.html#smtp-configuration)

User registration is already enabled by default, but emailing is disabled since it requires configuring an SMTP email service. To set that up, return to the management console and select **Settings** in the main menu and select **Settings** again under the **Portal** header in the submenu.

[![Screen Shot 2023-02-20 at 10.13.49 PM](https://europe1.discourse-cdn.com/business20/uploads/graviteeforum/optimized/2X/d/d033d41925c00cd1b56d9934ca774e89d4d118a2\_2\_690x312.png)Screen Shot 2023-02-20 at 10.13.49 PM3840×1738 427 KB](https://europe1.discourse-cdn.com/business20/uploads/graviteeforum/original/2X/d/d033d41925c00cd1b56d9934ca774e89d4d118a2.png)

Here, you can customize a number of aspects of the developer portal, but notice the warning at the top of the page. It essentially says the configuration file takes precedence. For example, if you scroll to the bottom of that page, you will see the SMTP settings, but the option to enable emailing is greyed out due to the previously mentioned configuration file.

[![Screen Shot 2023-02-20 at 10.11.35 PM](https://europe1.discourse-cdn.com/business20/uploads/graviteeforum/optimized/2X/a/abe13454c6d7c6a968428f085632edd92d44276c\_2\_690x312.png)Screen Shot 2023-02-20 at 10.11.35 PM3840×1738 307 KB](https://europe1.discourse-cdn.com/business20/uploads/graviteeforum/original/2X/a/abe13454c6d7c6a968428f085632edd92d44276c.png)

This configuration file is known as the `gravitee.yml` file. It is one of [three ways to configure settings for your APIM environment 1](https://docs.gravitee.io/apim/3.x/apim\_installguide\_rest\_apis\_configuration.html#overview): environment variables, system properties, and `gravitee.yml`, in order of precedence. We will be overriding these settings using environment variables, but first, we want to show you where in our docker installation the `gravitee.yml` file for APIM lives.

Open **Docker Desktop**, click on the `gio_apim_management_api` container, and switch to the **Terminal** tab. The `gravitee.yml` file lives in the `config` directory as shown in the image below. If you use the `cat` command to print the contents of the file, you will be able to search for and see the default SMTP settings.

> ![:bulb:](https://emoji.discourse-cdn.com/twitter/bulb.png?v=12) The gateway component has a separate `gravitee.yml` file.

[![Screen Shot 2023-02-22 at 11.43.42 PM](https://europe1.discourse-cdn.com/business20/uploads/graviteeforum/optimized/2X/f/f9048fa605cb73e34636e17358268f1f4e4e0193\_2\_690x261.png)Screen Shot 2023-02-22 at 11.43.42 PM2194×832 107 KB](https://europe1.discourse-cdn.com/business20/uploads/graviteeforum/original/2X/f/f9048fa605cb73e34636e17358268f1f4e4e0193.png)\
[![Screen Shot 2023-02-20 at 10.38.06 PM](https://europe1.discourse-cdn.com/business20/uploads/graviteeforum/optimized/2X/1/18291fe9b031f5d3becfdc0c6750eeffc1f4b96d\_2\_690x277.png)Screen Shot 2023-02-20 at 10.38.06 PM2116×850 90.9 KB](https://europe1.discourse-cdn.com/business20/uploads/graviteeforum/original/2X/1/18291fe9b031f5d3becfdc0c6750eeffc1f4b96d.png)

Rather than modify this file directly, we’re going to stick with our theme of using environment variables. Environment variables have precedence over the other two configuration types and allow us to define them in the same `.env` file we created earlier.

> ![:bulb:](https://emoji.discourse-cdn.com/twitter/bulb.png?v=12) **Gravitee Environment Variable Syntax**
>
> ***
>
> Unlike our `REACT_APP_API_KEY` environment variable which was injected into our todo application, these environment variables are being used to modify Gravitee specific configurations. You must ensure you use the correct syntax for each property:
>
> * Each level of indentation in the `gravitee.yml` file needs to be seperated by an underscore. For example, this inside a `gravitee.yml` file
>
> ***
>
> ```yaml
> management:
>    Mongodb:
>       dbname: myDatabase
> ```
>
> ***
>
> **becomes** `gravitee_management_mongodb_dbname=myDatabase`
>
> * Some properties are case-sensitive and cannot be written in uppercase (for example, `gravitee_security_providers_0_tokenIntrospectionEndpoint`). Therefore, we advise you to define all Gravitee environment variables in lowercase.
> * In some systems, hyphens are not allowed in variable names. For example, you may need to write `gravitee_policy_api-key_header` as `gravitee_policy_apikey_header`.

Open the `.env` file created in the Internal Exposure section and add the following environment variables:

```ini
gravitee_email_enabled=true
gravitee_email_host=fqdn-smtp-service-provider.com
gravitee_email_username=your-email@your-email-host.com
gravitee_email_password=your-password
gravitee_email_from=your-email@your-email-host.com
```

where `fqdn-smtp-service-provider` (fqdn = fully qualified domain name) and `your-email-host` is dependent on the email service you would like to use (e.g. Gmail, Yahoo, etc.). For Gmail, they have several options as [detailed here](https://support.google.com/a/answer/176600?hl=en). The rest should be self-explanatory; however, if you are using two-factor authentication with Gmail, then you need to [generate an application password](https://security.google.com/settings/security/apppasswords). This password will be used in place of your standard account password for the `gravitee_email_password` environment variable.

Similar to before, once you’ve input your email information, you need to make sure the environment variables are passed to the `management_api` container. Open the `docker-compose.yml` file again and uncomment lines 141 and 142. Finally, save the files and run `docker-compose up -d` to rebuild and restart the necessary containers one more time.

[![Screen Shot 2023-02-20 at 11.09.46 PM](https://europe1.discourse-cdn.com/business20/uploads/graviteeforum/optimized/2X/5/5e88cbd9ab8cc9e67bcb48cf9e780cbdfbb3368a\_2\_690x322.png)Screen Shot 2023-02-20 at 11.09.46 PM2736×1278 339 KB](https://europe1.discourse-cdn.com/business20/uploads/graviteeforum/original/2X/5/5e88cbd9ab8cc9e67bcb48cf9e780cbdfbb3368a.png)

After you give the containers a chance to restart, you should be able to return to the management console to see your updated settings. You also now have the option to enable auth and TLS in the management console which is recommended.

[![Screen Shot 2023-02-20 at 11.15.11 PM](https://europe1.discourse-cdn.com/business20/uploads/graviteeforum/optimized/2X/9/96bc69d764fee7a570e2bb2b238424769d72ce1a\_2\_690x149.png)Screen Shot 2023-02-20 at 11.15.11 PM1924×418 17.1 KB](https://europe1.discourse-cdn.com/business20/uploads/graviteeforum/original/2X/9/96bc69d764fee7a570e2bb2b238424769d72ce1a.png)

Alright, let’s test these new settings by attempting to create a new user. We recommend [opening the developer portal 1](http://localhost:8085/) in an incognito window to avoid being automatically signed out of the admin account being used in the management console. In the new incognito window, click **Sign in** then **Sign up**. Enter a name and functioning email.

[![Screen Shot 2023-02-20 at 11.27.01 PM](https://europe1.discourse-cdn.com/business20/uploads/graviteeforum/optimized/2X/4/423e485a2a5abd1477b326d9f795408e556dbe08\_2\_370x500.png)Screen Shot 2023-02-20 at 11.27.01 PM838×1130 22.6 KB](https://europe1.discourse-cdn.com/business20/uploads/graviteeforum/original/2X/4/423e485a2a5abd1477b326d9f795408e556dbe08.png)

If all goes smoothly, you should get a registration confirmation and an email to the address you provided. Open the email and click on the link. Make sure the link opens in the incognito tab; otherwise, it will just open the developer portal with the admin account signed in.

You will taken to a page to finalize your account and add a password. By default, the password must meet the following requirements:

* 8 to 32 characters
* no more than 2 consecutive equal characters
* min 1 special characters (@ & # …)
* min 1 upper case character

> ![:bulb:](https://emoji.discourse-cdn.com/twitter/bulb.png?v=12) **Password Customization**
>
> ***
>
> Password requirements can be modified by changing the regex pattern under **User Management Configuration** in the `gravitee.yml` file or by using environment variables. Additionally, you can provide [custom UI errors](https://docs.gravitee.io/am/current/am\_userguide\_user\_management\_password\_policy.html#custom\_ui\_errors) for future new users by modifying the sign up and register HTML templates.

Once you finish creating your password, you should be able to sign in without issue. The newly created external user will also be immediately visible in the admin’s management console. Leave the incognito window and return to the standard window where you are singed in as an admin in the management console. In the sidebar menu, you can reach your organization settings by clicking on **Organization** at the bottom. Once there, navigate to the **Users** tab in the sidebar. Here you will see a list of all current users tied to the organization. As an admin, you can click on any user for more details and to apply administrative policies. Additionally, admins can pre-register users by clicking the **Add user** button in the top right.

[![Screen Shot 2023-02-23 at 1.55.44 AM](https://europe1.discourse-cdn.com/business20/uploads/graviteeforum/optimized/2X/7/712b65b5d81ff0459a41a4f2f76487611d5ce4f8\_2\_690x312.png)Screen Shot 2023-02-23 at 1.55.44 AM3838×1740 280 KB](https://europe1.discourse-cdn.com/business20/uploads/graviteeforum/original/2X/7/712b65b5d81ff0459a41a4f2f76487611d5ce4f8.png)

Next, click on **Applications** in the sidebar. Interestingly, you should see a new application called **Default application** which is owned by the user you just created.

[![Screen Shot 2023-02-21 at 12.26.03 AM](https://europe1.discourse-cdn.com/business20/uploads/graviteeforum/optimized/2X/1/186f0300a51db63b3fece375675232e15e40486e\_2\_690x312.png)Screen Shot 2023-02-21 at 12.26.03 AM3834×1734 314 KB](https://europe1.discourse-cdn.com/business20/uploads/graviteeforum/original/2X/1/186f0300a51db63b3fece375675232e15e40486e.png)

So why did the new user not have to create a first application like the admin? In order to allow new users to quickly move forward with API consumption, the default settings are every new user automatically has a default application created. This can be easily disabled through the aforementioned three configuration options.

To follow the wisdom of Gravitee’s creators and take advantage of this default setting meant to promote speed of API consumption, let’s quickly have our external user subscribe to the **Dev Guide API**. Return to the developer portal in the incognito tab and navigate to the **Dev Guide API** inside the catalog. Once there, we will subscribe to **External API Key Plan** just like we did previously with our internal consumer and the original **API Key Plan**. Complete and submit the subscription request.

## Layout and theme customization

This section will detail how to modify how APIs are presented to API consumers.

### API Sidebar&#x20;

Administrators can modify what is shown in the sidebar of an API's **General information**.

<div data-full-width="false">

<figure><img src="../../../.gitbook/assets/Screenshot 2023-05-31 at 1.57.16 PM.png" alt=""><figcaption><p>Developer portal API sidebar</p></figcaption></figure>

</div>

In APIM, select **API Portal Information** in the secondary sidebar to display the following options:

<figure><img src="../../../.gitbook/assets/dev_portal_api_display_settings.png" alt=""><figcaption><p>Developer portal API sidebar display settings</p></figcaption></figure>

* **Add extra information**
  * **Show tags list in the API header:** Display all API labels in the developer portal
  * **Show categories list in the API header:** Display all API categories in the developer portal
* **Configure the information list:** Display custom values in the developer portal. Use the **+ icon** in the bottom right to add new values.
* **API Page list options:** Detailed in the [catalog tabs](./#catalog-tabs) section below

{% hint style="info" %}
Additionally, API publishers can modify the API sidebar by adding links to external documentation as detailed in the [Publish APIs documentation](../publish-apis.md).
{% endhint %}

### API Catalog

Administrators can also modify how API consumers browsing experience in the developer portal's API catalog.&#x20;

#### Promotion banner

In APIM, select **API Portal Information** in the secondary sidebar to display the following options shown below.&#x20;

<figure><img src="../../../.gitbook/assets/image (1).png" alt=""><figcaption><p>Developer portal API display settings</p></figcaption></figure>

* The other options are detailed in the [API sidebar](./#api-sidebar) section above.
*   **API Page list options**

    * **Display promotion banner:** Adds a banner to the top of each page in the API catalog to promote a particular API. The API that is promoted is determined automatically based on the tab. For example, the **Starred** tab will show the API that was most recently reviewed in the promotion banner.

    <figure><img src="../../../.gitbook/assets/Screenshot 2023-05-31 at 2.21.47 PM.png" alt=""><figcaption><p>Developer portal promotion banner</p></figcaption></figure>

#### Categories tab

Administrators have the option to include a **Categories** tab in the API catalog. This organizes APIs based on the category applied to a gateway API. Categories can be added on the **General** page of a gateway API as shown below:

<figure><img src="../../../.gitbook/assets/api_categories.png" alt=""><figcaption><p>Applying categories to a gateway API</p></figcaption></figure>

To enable the Categories tab in the developer portal, go to APIM and select **Categories** in the secondary sidebar. Here you can also create new categories and modify or delete existing categories.

<figure><img src="../../../.gitbook/assets/Screenshot 2023-06-01 at 1.59.06 PM.png" alt=""><figcaption><p>APIM categories settings page</p></figcaption></figure>

With the toggle enabled, users accessing the developer portal will have access to the page shown below:

<figure><img src="../../../.gitbook/assets/dev_portal_categories.png" alt=""><figcaption><p>Dev portal categories page</p></figcaption></figure>

#### Top/featured APIs

Administrators also have control over what is displayed on the **Featured** page of the API catalog by modifying the top APIs. Navigate to APIM **Settings** and select **Top APIs** in the secondary sidebar.

<figure><img src="../../../.gitbook/assets/Screenshot 2023-06-01 at 2.10.58 PM.png" alt=""><figcaption><p>Top APIs settings</p></figcaption></figure>

From here, administrators can add new APIs with the **+ icon**, reorder the top APIs, and remove APIs from the list. APIs added here are displayed on both the developer portal's homepage and on the API catalog's **Featured** page as shown below.

<figure><img src="../../../.gitbook/assets/dev_portal_homepage.png" alt=""><figcaption><p>Developer portal homepage displaying top APIs</p></figcaption></figure>

<figure><img src="../../../.gitbook/assets/Screenshot 2023-06-01 at 2.14.32 PM.png" alt=""><figcaption><p>Developer portal Featured page in API catalog</p></figcaption></figure>

{% hint style="info" %}
**Top API visibility**

If you are having issues seeing gateway APIs you added to the Top APIs list, make sure the API is public or the user logged into the developer portal has access to that API. Administrators can see all the APIs but individual users are restricted to public APIs and APIs they have been granted access to through user and group access settings.
{% endhint %}

### Navigation

Administrators can customize the developer portal navigation in the header and footer. This is done by creating link pages in Gravitee's system folders. There are three kinds of links:

* External link
* Link to an existing documentation page
* Link to a category

Each link is treated as a new documentation page. To learn about all the features and functionality of developer portal documentation, head to the[ Documentation section](./#documentation) of this page.

#### System folders

Gravitee's system folders are accessible in the management UI under **Settings > Documentation** and can be identified by their padlock icon as shown below.

<figure><img src="../../../.gitbook/assets/Screenshot 2023-06-05 at 10.44.36 AM.png" alt=""><figcaption><p>Gravitee's system folders</p></figcaption></figure>

There are three system folders: `Header`, `TopFooter` and `Footer`. Each system folder corresponds to an area of the developer portal:

<figure><img src="https://docs.gravitee.io/images/apim/3.x/api-publisher-guide/documentation/graviteeio-page-link-portal-zones.png" alt=""><figcaption><p>Developer portal - system folder mapping</p></figcaption></figure>

{% hint style="warning" %}
**`TopFooter`system folder nesting**

The`TopFooter`system folder is the only system folder that accepts nested folders. As shown in the image above, folders nested under the `TopFooter` system folder are used to group links together.

It is important to note that nested folders must be published to be seen in the developer portal.

<img src="../../../.gitbook/assets/Screenshot 2023-06-05 at 11.24.49 AM.png" alt="" data-size="original">
{% endhint %}

#### Manage Links <a href="#manage_links" id="manage_links"></a>

To create a link, open a system folder and select the **+ icon** then select the **Link** icon**.** This will take you to a new page to select your link type and provide some additional information about your link.

<figure><img src="../../../.gitbook/assets/dev_portal_create_a_link.png" alt=""><figcaption><p>Create a new developer portal link</p></figcaption></figure>

Select **Save**, and navigate to the developer portal to see your new link in action.

<figure><img src="../../../.gitbook/assets/dev_portal_custom_link_example.png" alt=""><figcaption><p>Sample "Gravitee Homepage" custom link</p></figcaption></figure>

Each custom link has additional features such as translations and access control that you can learn more about in the [Documentation section](./#documentation).

{% hint style="warning" %}
**Publishing`TopFooter`nested folders**

The`TopFooter`system folder is the only system folder that accepts nested folders. It is important to note that nested folders must be published to be seen in the developer portal.

<img src="../../../.gitbook/assets/Screenshot 2023-06-05 at 11.24.49 AM.png" alt="" data-size="original">
{% endhint %}

### Theming

Administrators can change the default theme of the developer portal to their own custom theme. To modify the theme, in the APIM settings select **Theme** in the secondary sidebar.

<figure><img src="../../../.gitbook/assets/Screenshot 2023-06-01 at 2.50.54 PM.png" alt=""><figcaption><p>Developer portal theme settings</p></figcaption></figure>

This page allows the administrator to customize every aspect of the developer portal's look and feel. Edits made are shown in a live preview to the right.

{% hint style="warning" %}
**Enable live preview**

If you are not seeing a live preview, this is due to not providing a Portal URL as detailed in the [General settings section](./#general-settings).
{% endhint %}

#### Top menu

The top menu provides the following options:

* **Fullscreen:** This button opens the preview in a new window, making it easier to edit if you have several screens
* **Reset:** This button allows you to reset the theme from the last backup. Backups occur when you select the **Save** button
* **Save:** This button saves your theme
* **Enabled:** This toggle activates the theme in APIM Portal
* **Import:** Upload a custom theme in `JSON` format. To see the required structure of the `JSON` file, export the current theme
* **Export:** Download your current theme in `JSON` format
* **Restore Default Theme:** This button overwrites your modifications with the theme provided by default

## Documentation

Outside of APIs and applications, administrators can also provide site-wide documentation for API publishers and consumers. Developer portal site-wide documentation is accessed on the **Documentation** page as shown below.

<figure><img src="../../../.gitbook/assets/Screenshot 2023-06-05 at 10.24.20 AM.png" alt=""><figcaption><p>Developer portal documentation page</p></figcaption></figure>

