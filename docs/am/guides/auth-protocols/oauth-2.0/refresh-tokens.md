# Refresh Tokens

A refresh token is used to get a new access token without user interaction (i.e sign-in process).

This allows good practices such as shorten the access token lifetime for security purposes without involving the user when the access token expires.

|   | By default the refresh token is single use only and must be use to request new access token until it expires. See [Refresh Token Rotation](https://docs.gravitee.io/am/current/am\_userguide\_oauth2\_refresh\_tokens\_rotation.html) for more information. |
| - | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |

|   | For security reasons a refresh token must be stored in a secure place (i.e server side) because they essentially allow a user to remain authenticated forever. |
| - | -------------------------------------------------------------------------------------------------------------------------------------------------------------- |

### See also

* [How to get Refresh Tokens](https://docs.gravitee.io/am/current/am\_userguide\_oauth2\_refresh\_tokens\_get.html)
* [How to use Refresh Tokens](https://docs.gravitee.io/am/current/am\_userguide\_oauth2\_refresh\_tokens\_use.html)
* [How to revoke Refresh Tokens](https://docs.gravitee.io/am/current/am\_userguide\_oauth2\_refresh\_tokens\_revoke.html)
* [Refresh Token Rotation](https://docs.gravitee.io/am/current/am\_userguide\_oauth2\_refresh\_tokens\_rotation.html)
