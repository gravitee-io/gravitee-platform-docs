---
description: Overview of Password Options.
---

# Password Options

Passwords are crucial for users as they protect sensitive information, secure online accounts, and prevent unauthorized access, ensuring privacy and safety.

Access Management allows you to tailor the experience for your users when it comes to setting and updating passwords. Below you may find a few options that can be helpful when, for example, provisioning users for the first time and making sure that the user controls setting their password.

### Force user to reset password on first login

Imagine the scenario, you want to create thousands of users enable them to sign in using Access Management. Maybe you create them directly in a database that is connected as a provider, or you create users directly in Access Management.

Its however important to you that you create the users first temporary password, maybe its a constraint in you database. You then provide the username and password to the user.\
\
Now, its very important that the user takes control over the password so the temporary password isn't used forever.\
\
For this purpose, you can now set a flag on the user profile that control if the users should be forced to update their password upon next login. So when provisioning users to Access Management, you simply set this flag to true and the user will be asked to update their password the first time they user their temporary password.

<figure><img src="../../../../4.4/.gitbook/assets/image (4).png" alt=""><figcaption><p>A user profile where Force Password Reset is set to true. This means that the user will be asked to update their password on the next login.</p></figcaption></figure>

### Send registration email to user and let user set pass

Imagine the same scenario as above, you want to create thousands of users enable them to sign in using Access Management. But this time, you want the user to set their first password themselves.

For this purpose, Access Management offers the feature pre-registration. If you set Enable pre-registration to true, then you as an admin will not be required to set a password for the user. Instead the user will receive a registration email to the email defined in the user profile. When the user clicks on this email, they will be taken to Access Management where they will be asked to set their password.

<figure><img src="../../../../4.4/.gitbook/assets/image (3).png" alt=""><figcaption><p>A user profile where Enable pre-registration is enabled. This means that the user will receive an email with a link that will allow the user to set their first password.</p></figcaption></figure>
