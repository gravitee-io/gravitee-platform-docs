---
description: This article describes how to create documentation for v2 APIs
---

# Documentation

## Overview

With the APIM Console, you can create API documentation, import API documentation, and add API metadata. Gravitee supports ASCIIDOC, AsyncAPI spec, OpenAPI spec, Swagger, and Markdown formats.

You can add the documentation through the API Management (APIM) Console to inform API consumers how to use an API. If the API and documentation are both published to the Developer Portal, the documentation appears in the Portal.

## Import documentation files

To import documentation:

1. Sign in to your APIM Console
2. From the navigation menu, select **APIs**
3. Select your API.
4. From the inner left nav, select **Documentation**.
5. Select the **Pages** tab.
6. To import documentation files, choose either of the following options:
   *   Click on **Import multiple files**

       <figure><img src="broken-reference" alt=""><figcaption><p>Import multiple files</p></figcaption></figure>

       * Toggle **Publish all imported pages** ON or OFF
       * To **Select your source**, choose from: Bitbucket, git, GitHub, GitLab, or a URL
       * Fill in the information appropriate to and required by your selection
       * Click **IMPORT**
   * Import individual files while creating new API documentation:
     *   Under the **Pages** tab, click the <img src="broken-reference" alt="" data-size="line"> icon

         <figure><img src="broken-reference" alt=""><figcaption><p>Import via page creation</p></figcaption></figure>
     * Select one of the following options:
       * ASCIIDOC
       * ASYNCAPI
       * SWAGGER
       * MARKDOWN
     * At the bottom of the configuration page, click **Choose File**.
     * After you select your file, click **SAVE**.

## Create API documentation

1. SIgn in to your APIM Console
2. From the left nav, select **APIs**
3. Select the API that you want to add documentation to.
4. From the inner left nav, select **Documentation**.
5. Under the **Pages** tab, select the <img src="broken-reference" alt="" data-size="line"> icon.
6. Select your preferred format.
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

    <figure><img src="broken-reference" alt=""><figcaption><p>Add API metadata</p></figcaption></figure>
7. Choose a name for your API, select the format (string, numeric, boolean, date, mail, url), and define the value
8. Click **Save**
