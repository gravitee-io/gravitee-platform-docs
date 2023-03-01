---
title: APIM Installation Guide - Amazon Linux - Prerequisites - Setup Gravitee YUM repository
tags:
  - APIM
  - Installation
  - Prerequisites
  - Amazon
  - Java
---

# Overview

Running the Gravitee APIM components requires a Java 11 JRE. To set it up, follow the instructions below.

# Instructions

1.  Enable the repository that contains java:

```
  sudo amazon-linux-extras enable java-openjdk11
```

2.  Install Java:

```
  sudo yum install java-11-openjdk -y
```

3.  Verify:

```
  java -version
```

!!! note

    You don’t **have** to go for this particular implementation of openjdk, as long as you have a decent uncrippled Java 11 JRE it’s fine!

# Next steps

The next step is [installing MongoDB](installation-guide-amazon-prerequisite-mongodb.md).
