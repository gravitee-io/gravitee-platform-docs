---
description: This page summarizes rules and best practices for docs code
---

# Code Blocks

* Enable the correct syntax highlighting for each code block.
* Use the caption feature to label specific files or add context.

{% code title="values.yml" %}
```yaml
jdbc:
  driver: https://jdbc.postgresql.org/download/postgresql-42.2.23.jar
  url: jdbc:postgresql://postgres-apim-postgresql:5432/graviteeapim
  username: postgres
  password: P@ssw0rd
management:
  type: jdbc
```
{% endcode %}

* Enable horizontal scrolling to prevent commands from wrapping.
* Do not include more than one complex command in a code block.
* For one-line commands, do not include the command prompt (the `$` symbol).
* For multi-line commands, always inlcude the command prompt (the `$` symbol).

```sh
$ cd [DESTINATION_FOLDER]/graviteeio-apim-gateway-3.20.0
$ ./bin/gravitee
```

* Add comments where appropriate.
* Only include output within the context of an example or to set user expectations. When showing output, use a separate code block and add a label.
