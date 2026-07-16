---
description: Introduction to the basics of API
---

# API Basics

An application programming interface, or API, is a set of publicly exposed specifications that define the logic of how to integrate with a particular piece of software. These conventions establish a contract and provide the structure that allows computer programs or applications to communicate.

While "API" and "web API" are often used interchangeably, web APIs are a specific subset of API that operate over a network. "API" has much broader implications and includes every method or function called in programming, whether built into a language or made available by a 3rd party package or module.

Consider the following Python snippet:

```python
from datetime import datetime

date_str = "12/25/1996"
date_object = datetime.strptime(date_str, "%m/%d/%Y")
```

Importing the `datetime` module provides access to public methods, or APIs, like `strptime` to convert a `string` into a `datetime` object. Although not network-related, this API still imposes a software contract, which guarantees the stability of the API with respect to the current software version. The contract allows the programmer to have confidence in the API's expected behavior without understanding how the input data is transformed.

{% hint style="info" %}
Respecting API contracts is the basis for **semantic versioning** in software. Check out [this article](https://blog.webdevsimplified.com/2020-01/semantic-versioning/) for an introduction to semantic versioning and to learn how API contracts are managed as software is continuously updated.
{% endhint %}

APIs enable the trusted layers of abstraction that are critical to programming. For example, most developers prefer to use a high-level programming language like Python as opposed to a [low-level assembly language](https://www.investopedia.com/terms/a/assembly-language.asp). Numerous abstractions allow a Python print statement to look like this:

```python
print('Hello, World')
```

instead of this:

```asm6502
; hello-DOS.asm - single-segment, 16-bit "hello world" program
;
; assemble with "nasm -f bin -o hi.com hello-DOS.asm"

    org  0x100        ; .com files always start 256 bytes into the segment

    ; int 21h is going to want...

    mov  dx, msg      ; the address of or message in dx
    mov  ah, 9        ; ah=9 - "print string" sub-function
    int  0x21         ; call dos services

    mov  ah, 0x4c     ; "terminate program" sub-function
    int  0x21         ; call dos services

    msg  db 'Hello, World!', 0x0d, 0x0a, '$'   ; $-terminated message
```

Beyond developer experience and productivity, abstraction remains critical. For example, the vast majority of people don't have a a low-level understanding of how email works, just that there are inputs (i.e., interface conventions): recipients, subject, message body, the send button, etc., and output: a rapid form of text-based communication. Abstractions, and therefore APIs, are necessary for efficiency and innovation.

<figure><img src="https://europe1.discourse-cdn.com/business20/uploads/graviteeforum/original/2X/a/a8a51b9365a05b24e391d475f37a6fb6408d9150.png" alt=""><figcaption><p>Abstraction meme posted on reddit</p></figcaption></figure>

{% hint style="warning" %}
Gravitee uses the terms "web API" and "API" synonymously. An API that does not communicate over a network is explicitly referred to as a local API.
{% endhint %}
