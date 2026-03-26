# SAML IdP Plugin Version Upgrade Notes

## Related Changes

The `gravitee-am-idp-saml2` plugin was upgraded from version `4.0.3` to `5.0.0-alpha.3` to support metadata URL and metadata file configuration modes. The `gravitee-plugin-validator` dependency was updated from `2.0.2` to `2.3.0` to support validation of the new configuration properties. The SAML authentication flow remains unchanged—users initiate login via the client application, navigate to the SAML provider login page, submit credentials to the SAML IdP, and receive a SAML assertion that is validated and exchanged for an authorization code.
