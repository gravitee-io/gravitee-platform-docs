---
description: This article describes how to create documentation for v2 APIs
---

# Documentation

## Introduction

With the APIM Console, you can create API documentation, import API documentation, and add API metadata. Gravitee supports ASCIIDOC, AsyncAPI spec, OpenAPI spec, Swagger, and Markdown formats.

## Import documentation files

To import documentation:

1. Log in to your APIM Console
2. Select **APIs** from the left nav
3. Select your API
4. Select **Documentation** from the inner left nav
5. Select the **Pages** tab
6. Choose one of the following two options:
   *   Click on **Import multiple files**

       <figure><img src="../../../../.gitbook/assets/v2 docs_import multiple files (1).png" alt=""><figcaption><p>Import multiple files</p></figcaption></figure>

       * Toggle **Publish all imported pages** ON or OFF
       * To **Select your source**, choose from: Bitbucket, git, GitHub, GitLab, or a URL
       * Fill in the information appropriate to and required by your selection
       * Click **IMPORT**
   * Import individual files while creating new API documentation:
     *   Under the **Pages** tab, click the <img src="../../../../.gitbook/assets/Screen Shot 2023-06-08 at 3.06.53 PM (1).png" alt="" data-size="line"> icon

         <figure><img src="../../../../.gitbook/assets/v2 docs_create (1).png" alt=""><figcaption><p>Import via page creation</p></figcaption></figure>
     * Choose from **ASCIIDOC**, **ASYNCAPI**, **SWAGGER**, and **MARKDOWN**
     * Scroll down to the bottom of the configuration page and click **Choose File**
     * After selecting your file, click **SAVE**

## Create API documentation

To create API documentation:

1. Log in to your APIM Console
2. Select **APIs** from the left nav
3. Select your API
4. Select **Documentation** from the inner left nav
5. Under the **Pages** tab, select the <img src="../../../../.gitbook/assets/Screen Shot 2023-06-08 at 3.06.53 PM (1).png" alt="" data-size="line"> icon
6. Select your preferred format
7. Create and configure your documentation:
   1. Give your documentation a name
   2. Choose whether to:
      * Set the documentation as the API homepage
      * Publish the documentation page
      * Make the documentation private to authorized users
   3. Define how to create, or get, the documentation content:
      * Fill in the documentation inline yourself: If you select this option, you'll be given the option to start typing your documentation
      * Import the documentation from a file
      * Import documentation from an external source: Gravitee supports Bitbucket, git repository, Github, GitLab, and public URLs
8. Click **SAVE**

## Add API metadata

To add metadata:

1. Log in to your APIM Console
2. Select **APIs** from the left nav
3. Select your API
4. Select **Documentation** from the inner left nav
5. Select the **Metadata** tab
6.  Click on **+ Add API Metadata**

    <figure><img src="../../../../.gitbook/assets/v2 docs_metadata (1).png" alt=""><figcaption><p>Add API metadata</p></figcaption></figure>
7. Choose a name for your API, select the format (string, numeric, boolean, date, mail, url), and define the value
8. Click **Save**
