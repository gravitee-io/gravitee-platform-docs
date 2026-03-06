### Gateway Configuration

#### Email Service Properties

| Property | Description | Default |
|:---------|:------------|:--------|
| `user.magic.link.login.email.subject` | Subject line for magic link authentication emails | `"Sign in"` |
| `user.magic.link.login.time.value` | Magic link token expiration time value | `15` |
| `user.magic.link.login.time.unit` | Magic link token expiration time unit | `MINUTES` |

#### Login Settings

| Property | Description | Default |
|:---------|:------------|:--------|
| `magicLinkAuthEnabled` | Enable or disable magic link authentication feature | `false` |

Set `magicLinkAuthEnabled` to `true` in the domain's login settings to activate the feature. When enabled, the login page displays a "Sign in with Magic Link" option and the magic link form and email templates become available.

### Customizing Email Templates

Customize the magic link email by editing the `MAGIC_LINK` email template. The template supports the following internationalization keys:

**English:**

```properties
email.magic_link.header.title=Sign in to {0}
email.magic_link.header.description.first.row=Hi there,
email.magic_link.header.description.second.row=You requested to sign in to {0}. Click the button below to access your account:
email.magic_link.button=Sign in to {0}
email.magic_link.expiration=This link will expire in {0,number,integer} {1} for security.
email.magic_link.raw.link=If the button doesn't work, copy and paste this link into your browser:
```

**French:**

```properties
email.magic_link.header.title=Se connecter à {0}
email.magic_link.header.description.first.row=Bonjour,
email.magic_link.header.description.second.row=Une demande de connexion à {0} a été effectuée. Cliquez sur le bouton ci-dessous pour accéder à votre compte:
email.magic_link.button=Se connecter à {0}
email.magic_link.expiration=Pour des raisons de sécurité, ce lien expirera dans {0,number,integer} {1}.
email.magic_link.raw.link=Si le bouton ne fonctionne pas, veuillez copier et coller ce lien dans votre navigateur :
```
