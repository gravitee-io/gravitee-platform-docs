# Password Policy

> A key concern when using passwords for authentication is password strength. A "strong" password policy makes it difficult or even improbable for one to guess the password through either manual or automated means.

— OWASP\
[_Authentication cheat sheet_](https://cheatsheetseries.owasp.org/cheatsheets/Authentication_Cheat_Sheet.html#implement-proper-password-strength-controls)

## Configure a password policy

You can configure the password policy settings for your end users during the **sign up** and **reset password** actions.

1. Log in to AM Console.
2. Select your application and click **Settings > Password policy**.
3. Configure your password policy settings and click **SAVE**.

{% hint style="info" %}
You can also configure password policy settings at the security domain level, to be applied across all applications.
{% endhint %}

## Password settings characteristics

You can set the following password characteristics:

* **Minimum & Maximum length**: length of the passwords that should be enforced by the application.
* **Numbers**: must include at least one number.
* **Expiry Duration**: the expiration duration (in days) of a password.
* **Special characters**: must include at least one special character.
* **Mixed case**: must include lowercase and uppercase letters.
* **Exclude common passwords**: will exclude common passwords from a dictionary.
* **Exclude user profile information from passwords**: will exclude user profile information from use in passwords (case insensitive).
* **History**: prevent the usage of old passwords.

## Password dictionary

By default, the password dictionary includes [ten thousand common passwords](https://github.com/danielmiessler/SecLists/blob/master/Passwords/Common-Credentials/10k-most-common.txt).

If you wish to use your own password dictionary or add entries to the existing password dictionary, update the `gravitee.yml` file (on both AM Gateway and AM API) as follows:

```yaml
user:
  password:
    policy:
      ...
      ## Password dictionary to exclude most commons passwords
      ## You need to enable the feature in the AM Management Console

      dictionary:
        filename: /path/to/dictionary.txt
        watch: true # true|false:boolean
```

Where:

* `user.password.policy.dictionary.filename` is the path of the file containing the passwords.
* `user.password.policy.dictionary.watch` if true, will listen for any change on the current `filename` and update the dictionary without restarting the service.

## Custom UI errors

You can access the password policy settings in your **Sign Up** and **Register** [HTML templates](../branding/README.md#custom-pages), making it possible to customize the error messages your end users see.

{% code overflow="wrap" %}
```html
  <div th:if="${passwordSettings != null}" id="passwordSettings">
      <span
              th:if="${passwordSettings.minLength != null || passwordSettings.includeNumbers || passwordSettings.includeSpecialCharacters
              || passwordSettings.lettersInMixedCase || passwordSettings.maxConsecutiveLetters != null ||
              passwordSettings.excludePasswordsInDictionary || passwordSettings.excludeUserProfileInfoInPassword}"
              class="small-font grey" th:text="#{password.validation.label}"/>

      <p th:if="${passwordSettings.minLength != null}" id="minLength" class="invalid"><span th:text="#{password.minLength.before}" /> <span th:text="${passwordSettings.minLength}"/> <span th:text="#{password.minLength.after}"/></p>
      <p th:if="${passwordSettings.includeNumbers}" id="includeNumbers" class="invalid" th:text="#{password.include.numbers}" />
      <p th:if="${passwordSettings.includeSpecialCharacters}" id="includeSpecialChar" class="invalid" th:text="#{password.include.special.characters}" />
      <p th:if="${passwordSettings.lettersInMixedCase}" id="mixedCase" class="invalid" th:text="#{password.letters.mixed.cases}" />
      <p th:if="${passwordSettings.maxConsecutiveLetters != null}" id="maxConsecutiveLetters" class="valid" ><span th:text="#{password.max.consecutive.letters.before}" /> <span th:text="${passwordSettings.maxConsecutiveLetters}"/> <span th:text="#{password.max.consecutive.letters.after}" /></p>
      <p th:if="${passwordSettings.excludeUserProfileInfoInPassword}" id="excludeUserProfileInfoInPassword" class="invalid" th:text="#{password.exclude.user.info}"/>
      <p th:if="${passwordSettings.excludePasswordsInDictionary}" id="excludePasswordsInDictionary" class="black" th:text="#{password.exclude.common.passwords}"/>
      <p th:if="${passwordSettings.passwordHistoryEnabled}" id="excludePasswordsInHistory" class="invalid"><span th:text="#{password.history.before}" /> <span th:text="${passwordSettings.oldPasswords}"/> <span th:text="#{password.history.after}"/></p>
      <p id="matchPasswords" class="invalid" th:text="#{password.confirmation.match}"/>
  </div>
```
{% endcode %}
