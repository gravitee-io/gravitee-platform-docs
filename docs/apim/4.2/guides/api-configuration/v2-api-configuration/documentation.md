---
description: >-
  This article walks through how to create documentation for your APIs in
  Gravitee
---

# Documentation

{% @arcade/embed url="https://app.arcade.software/share/2NtJYq9KSReDKxJPQD2q" flowId="2NtJYq9KSReDKxJPQD2q" %}

{% hint style="info" %}
**v4 API limitations**

As of Gravitee 4.0, you can not yet create documentation for v4 APIs. Support for this is planned for future releases.
{% endhint %}

## Introduction

The easiest way to create documentation for your APIs is to use the Gravitee API Designer. However, if you aren't using Gravitee API Designer, you can create API documentation, import API documentation, and add API Metadata using the Gravitee API Management Console. As of today, Gravitee supports the following API documentation formats:

* ASCIIDOC
* AsyncAPI spec
* OpenAPI spec
* Swagger
* Markdown

## Import documentation files

If you didn't import documentation during the API creation phase, you can easily import documentation on the API's documentation page. To do this, select APIs in the left-hand nav, and select your API from the APIs list.

Then, select Documentation under the Portal section. You'll have two main ways to import documentation files:

* Import multiple files at once: On the **Pages** tab, select **Import multiple files.** If you choose this option, you'll need to select your source, which, as of now, can be Github or GitLab.
* Import individual files while creating new API documentation (see the "Create API documentation" section below)

## Create API documentation

To create API documentation, select the <img src="../../../../../../.gitbook/assets/Screen Shot 2023-06-08 at 3.06.53 PM (1).png" alt="" data-size="line"> icon. Then, select your preferred format, and create the documentation. Choose your preferred documentation format.

After you choose your format, you'll need to:

* Give your documentation a name
* Choose whether to:
  * Set the documentation as the API homepage
  * Publish the documentation page
  * Make the documentation private to authorized users
* Define how to create, or get, the documentation content:
  * Fill in the documentation inline yourself: if you select this option, you'll be given the option to start typing your documentation
  * Import the documentation from a file
  * Import documentation from an external source: Gravitee supports Bitbucket, git repository, Github, GitLab, and public URLs.

Once you've either written or imported your API documentation, select **Save.**

## Add API metadata

If you want to add metadata to your API, select the **Metadata** tab. Then, select <img src="../../../../../../.gitbook/assets/Screen Shot 2023-06-08 at 3.14.20 PM (1).png" alt="" data-size="line">. From here, you just need to choose a name for your API, select the format (string, numeric, boolean, date, mail, url), and define the value. Then, select **Save.**
