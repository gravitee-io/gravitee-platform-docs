---
description: Overview of Account Token.
---

# Account Token

## Introduction

Account Token allows you to generate secure, long-living tokens that can be used to interact with your Cockpit Account via the Management API.

A sample use case would be to automate the creation of Organizations and Environments and then link them to your installations.

## How it works

Account Token management is available through Account Settings to Account Administrators only.

Account Token permissions are directly derived from the user who created the token. For example, if an an ACCOUNT\_PRIMARY\_OWNER creates an Account Token, the token will inherit the account permissions of this user.

A total of 10 Account Tokens can be active simultaneously.

## How to create a token

Follow the steps below to create and manage Account Tokens:

1.  Go to **Settings > Account Tokens**.

    <figure><img src="../.gitbook/assets/image (8).png" alt=""><figcaption></figcaption></figure>
2.  Click **Generate token**, give your Account Token a meaningful name, then click **Generate**.

    <figure><img src="../.gitbook/assets/account token_generate.png" alt=""><figcaption></figcaption></figure>
3.  The next dialogue box will show your Account Token and a CURL example of how to use it. Make sure to copy your Account Token, as this will not be possible once you close the dialogue box.

    <figure><img src="../.gitbook/assets/account token_copy.png" alt=""><figcaption></figcaption></figure>
4.  Your Account Token will now be listed in the table.

    <figure><img src="../.gitbook/assets/account token_listed.png" alt=""><figcaption></figcaption></figure>
5.  To delete a token, click the **trash icon** on the right of the Account Token entry, enter its name in the **Confirm** field, and, after verifying the token has no dependencies, click **I understand the consequences, revoke this token**.

    <figure><img src="../.gitbook/assets/account token_delete.png" alt=""><figcaption></figcaption></figure>
