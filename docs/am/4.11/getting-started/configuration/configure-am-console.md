---
metaLinks:
  alternates:
    - >-
      https://app.gitbook.com/s/H4VhZJXn1S232OEmh8Wv/getting-started/configuration/configure-am-console
description: Configure the Access Management 4.11 Console with a constants.json file. Follow the steps to set the values your deployment needs.
---

# AM Console

You can configure AM Console with a file named `constants.json`.

The only mandatory values in the `constants.json` file are:

```sh
$ cd gravitee-am-webui-3.21.0
$ vi constants.json

{
  "baseURL": "gravitee_am_management_api_url"
}
```

It describes where AM API lives, so that AM console can send requests to it.
