---
description: Overview of User.
---

# User attributes

User profiles in Access Management mainly contains of two sections: general details and additional information.\
\
General details are attributes mandatory for each profile, such as username, name, email, password. Mainly the information you see at the top section if you visit the users profile.\
\
The additional information section is more flexible, and you can choose to enrich each user profile with custom keys and values that can be used to make decisions in login flow, such as MFA, or be a holder of permissions such as group information or write roles.

### Make email optional

In some particular cases you may want to make the email as optional for the user. For example if you want to onboard temporary users in you operations that will not be given an email address.\
\
For these cases you can set email as optional. This is done by configuring email required to false in the gravitee.yml file of Access Management Gateway.\
\
Bear in mind that features that require an email will not work for these users.

```
email:
    # Set required: false to make email optional for internal identity providers' users.
    # WARNING: Features that rely on having an email available won't work for such users!
    # E.g.: password reset, Email MFA, pre-registration
    #required: true
    policy:
      pattern: ^[a-zA-Z0-9_+-]+(?:\.[a-zA-Z0-9_+-]+)*@(?:[a-zA-Z0-9-]+\.)+[a-zA-Z]{2,15}$
```
