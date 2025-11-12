# Roles

## Overview

Roles are used to specify system access to authorized users. Each role provides a set of permissions representing operations that users can perform on specific services.

## Create role

You create roles in a security domain.

1. Log in to AM Console.
2. Click **Settings > Scopes**.
3. Click the plus icon ![plus icon](https://docs.gravitee.io/images/icons/plus-icon.png) and create a scope called `admin`.
4. Click **Settings > Roles**.
5. Click the plus icon ![plus icon](https://docs.gravitee.io/images/icons/plus-icon.png).
6.  Give your role a name and a description and click **SAVE**.

    You will be redirected to the created role’s page.
7. Select the `admin` scope permission and click **SAVE**.

## Use roles

You can use roles to supplement an access token’s claims, for example, to limit the scope of operation of your protected services and APIs. See [custom claims](docs/am/4.1/getting-started/tutorial-getting-started-with-am/get-user-profile-information.md#custom-claims) for more information.
