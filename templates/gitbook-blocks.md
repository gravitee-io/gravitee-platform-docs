# GitBook Blocks

H1 heading:

## H1 heading

H2 heading:

### H2 heading

H3 heading:

#### H3 heading

Ordered list:

1. First step
2. Second step
3. Third step

Unordered list:

* Bullet 1
* Bullet 2
* Bullet 3

Task list:

* [ ] Task 1
* [ ] Task 3
* [ ] Task 3

Hint (tip):

{% hint style="info" %}
This hint type is reserved for helpful information.
{% endhint %}

Hint (caution):

{% hint style="warning" %}
This hint type is reserved for warnings.
{% endhint %}

Hint (alert):

{% hint style="danger" %}
This hint type is reserved for critical alerts.
{% endhint %}

Hint (success):

{% hint style="success" %}
This hint type is reserved for affirmations/success.// Some code
{% endhint %}

Code block (plain, with caption, wrapped):

{% code title="Caption" overflow="wrap" %}
```
// Some code
```
{% endcode %}

Code block (JSON):

```json
// Some code
```

Code block (YAML):

```yaml
// Some code
```

Code block (HCL):

```hcl
// Some code
```

Hint with code block and image:

{% hint style="info" %}
Here is a hint.

<img src=".gitbook/assets/02.png" alt="" data-size="original">

```
// Some code
```
{% endhint %}

Tabs with code blocks, image, hint:

{% tabs %}
{% tab title="JavaScript" %}
```javascript
const message = "hello world";
console.log(message);
```
{% endtab %}

{% tab title="Python" %}
```python
message = "hello world"
print(message)
```
{% endtab %}

{% tab title="Ruby" %}
```ruby
message = "hello world"
puts message
```
{% endtab %}

{% tab title="Untitled" %}
<figure><img src=".gitbook/assets/02.png" alt=""><figcaption></figcaption></figure>

{% hint style="info" %}
Here is a hint.
{% endhint %}

```
// Some code
```
{% endtab %}
{% endtabs %}

Expandable:

<details>

<summary>Expandable</summary>

Text

</details>

Expandable with image, list, code block, hint:

<details>

<summary>Expandable</summary>

<figure><img src=".gitbook/assets/02.png" alt=""><figcaption></figcaption></figure>

* Item 1
* Item 2
* Item 3

```
// Some code
```

{% hint style="info" %}
Here is a hint.
{% endhint %}

</details>

Table with code block, hint, image, link:

<table><thead><tr><th>Header 1</th><th>Header 2</th><th>Header 3</th></tr></thead><tbody><tr><td>parameter 1</td><td>value 1</td><td><p>code block</p><pre><code>// Some code
</code></pre></td></tr><tr><td>parameter 2</td><td>value 2</td><td></td></tr><tr><td>parameter 3</td><td>value 3</td><td><p>hint</p><div data-gb-custom-block data-tag="hint" data-style="info" class="hint hint-info"><p>Here is a hint.</p></div></td></tr><tr><td></td><td><img src=".gitbook/assets/02.png" alt=""></td><td><a data-mention href="gitbook-blocks.md#python">#python</a></td></tr></tbody></table>

Cards with image, link, file:

<table data-view="cards"><thead><tr><th></th><th data-type="content-ref"></th><th data-type="files"></th><th data-hidden data-card-cover data-type="image">Cover image</th></tr></thead><tbody><tr><td></td><td><a href="gitbook-blocks.md#h1-heading">#h1-heading</a></td><td></td><td><a href=".gitbook/assets/02.png">02.png</a></td></tr><tr><td></td><td></td><td><a href=".gitbook/assets/02.png">02.png</a></td><td></td></tr></tbody></table>

Columns:

{% columns %}
{% column %}
<figure><img src=".gitbook/assets/02.png" alt=""><figcaption></figcaption></figure>
{% endcolumn %}

{% column %}
column 2

{% hint style="info" %}
Here is a hint.
{% endhint %}

```
// Some code
```
{% endcolumn %}
{% endcolumns %}

Drawing:

<img src=".gitbook/assets/file.excalidraw.svg" alt="" class="gitbook-drawing">

Examples of indentation:

*   {Write the step here. Begin the step with a base form verb.}{Optional: Explanatory text.} \
    {Optional: Indented screenshot that is associated with the step.}<br>

    <figure><img src=".gitbook/assets/02.png" alt=""><figcaption><p>Example  screenshot</p></figcaption></figure>
*   {Write the step here. Begin the step with a base form verb.}{Optional: Explanatory text.} \
    {Optional: Indented code sample. Select the programming language from the drop-down menu that appears in the upper right of the code block. Enter the filename as the code block caption.}<br>

    <pre data-title="filename.ext"><code><strong>// Some code
    </strong></code></pre>

    \
    {Optional: The result of completing this step.}
* {Write the step here. Begin the step with a base form verb.}
  1.  {Ordered sub-step 1}{Optional: Indented screenshot that is associated with the sub-step.}<br>

      <figure><img src=".gitbook/assets/02.png" alt=""><figcaption><p>Example  screenshot</p></figcaption></figure>
  2. {Ordered sub-step 2}
* {Write the step here. Begin the step with a base form verb.}
  *   {Unordered or optional sub-step 1}<br>

      <div data-gb-custom-block data-tag="hint" data-style="info" class="hint hint-info"><p>{Optional: Indented admonition.}</p></div>


  * {Unordered or optional sub-step 2}

OpenAPI spec:

{% openapi-operation spec="mapi-v1-file" path="/auth/cockpit" method="get" %}
[OpenAPI mapi-v1-file](https://4401d86825a13bf607936cc3a9f3897a.r2.cloudflarestorage.com/gitbook-x-prod-openapi/raw/dfe98bd3e124bf2dfe64e9f4a08af46943f7c95f2e8da7ef449c70e6e01dcbbd.txt?X-Amz-Algorithm=AWS4-HMAC-SHA256&X-Amz-Content-Sha256=UNSIGNED-PAYLOAD&X-Amz-Credential=dce48141f43c0191a2ad043a6888781c%2F20251121%2Fauto%2Fs3%2Faws4_request&X-Amz-Date=20251121T180544Z&X-Amz-Expires=172800&X-Amz-Signature=782dab55baac6e51742b0d79f2f6b571728f1ddae47753cad14fd483fb77b3d6&X-Amz-SignedHeaders=host&x-amz-checksum-mode=ENABLED&x-id=GetObject)
{% endopenapi-operation %}

{% openapi-operation spec="mapi-v1-file" path="/auth/external" method="get" %}
[OpenAPI mapi-v1-file](https://4401d86825a13bf607936cc3a9f3897a.r2.cloudflarestorage.com/gitbook-x-prod-openapi/raw/dfe98bd3e124bf2dfe64e9f4a08af46943f7c95f2e8da7ef449c70e6e01dcbbd.txt?X-Amz-Algorithm=AWS4-HMAC-SHA256&X-Amz-Content-Sha256=UNSIGNED-PAYLOAD&X-Amz-Credential=dce48141f43c0191a2ad043a6888781c%2F20251121%2Fauto%2Fs3%2Faws4_request&X-Amz-Date=20251121T180544Z&X-Amz-Expires=172800&X-Amz-Signature=782dab55baac6e51742b0d79f2f6b571728f1ddae47753cad14fd483fb77b3d6&X-Amz-SignedHeaders=host&x-amz-checksum-mode=ENABLED&x-id=GetObject)
{% endopenapi-operation %}

{% openapi-operation spec="mapi-v1-file" path="/organizations/{orgId}" method="get" %}
[OpenAPI mapi-v1-file](https://4401d86825a13bf607936cc3a9f3897a.r2.cloudflarestorage.com/gitbook-x-prod-openapi/raw/dfe98bd3e124bf2dfe64e9f4a08af46943f7c95f2e8da7ef449c70e6e01dcbbd.txt?X-Amz-Algorithm=AWS4-HMAC-SHA256&X-Amz-Content-Sha256=UNSIGNED-PAYLOAD&X-Amz-Credential=dce48141f43c0191a2ad043a6888781c%2F20251121%2Fauto%2Fs3%2Faws4_request&X-Amz-Date=20251121T180544Z&X-Amz-Expires=172800&X-Amz-Signature=782dab55baac6e51742b0d79f2f6b571728f1ddae47753cad14fd483fb77b3d6&X-Amz-SignedHeaders=host&x-amz-checksum-mode=ENABLED&x-id=GetObject)
{% endopenapi-operation %}
