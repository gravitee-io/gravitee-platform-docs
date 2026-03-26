---
description: Configuration guide for v4 Proxy API Endpoints.
---

# v4 Proxy API Endpoints

## Configuration

To configure v4 proxy API endpoints:

1. Select **APIs** from the left nav
2. Select your API
3. Select **Backend services** from the Endpoints section of the inner left nav

Refer to the following sections for step-by-step configuration details.

### 1. Define your target URL

Enter your target URL in the **Target URL** text field.

### **2. Define your HTTP options**

1. Choose to either allow or disallow h2c clear text upgrade by toggling **Allow h2c Clear Text Upgrade** ON or OFF.
   * You'll need to select the HTTP protocol version to use. HTTP/1.1 and HTTP/2 are supported.
2. Choose to either enable or disable keep-alive by toggling **Enable keep-alive** ON or OFF.
   * If enabled, you'll need to define a numeric timeout value in the **Connect timeout** text field by either entering a numerical value or using the arrow keys.
3. Choose to either enable or disable HTTP pipelining by toggling **Enable HTTP pipelining** ON or OFF.
   * If enabled, you'll need to define a numeric timeout value in the **Read timeout** text field by either entering a numerical value or using the arrow keys.
4. Choose to either enable or disable compression by toggling **Enable compression (gzip, deflate)** ON or OFF.
5. **Configure your idle timeout settings:** Define, in milliseconds, the maximum time a connection will stay in the pool without being used by entering a numeric value or using the arrow keys in the text field. Once the specified time has elapsed, the unused connection will be closed, freeing the associated resources.
6. Choose whether to follow HTTP redirects by toggling **Follow HTTP redirects** ON or OFF.
7. Define the number of max concurrent connections by entering a numeric value or using the arrow keys in the text field.
8. Choose to propagate client Accept-Encoding header by toggling **Propagate client Accept-Encoding header (no decompression if any)** ON or OFF.
9. Select **+ Add HTTP headers** to add headers that the Gateway should add or override before proxying the request to the backend API.

### **3. Define your Proxy options**

1. Choose whether to use a proxy for client connections by toggling **Use proxy** ON of OFF.
   * If enabled, you will need to select from the proxy types in the **Proxy type** drop-down: **HTTP proxy**, **SOCKS4**, or **SOCKS5**.
2. **Use system proxy:** Choose whether to use the proxy configured at system level. If enabled, you'll need to define the following:
   * **Proxy host:** Enter your proxy host in the text field.
   * **Proxy port:** Enter your proxy port in the text field.
   * (Optional) **Proxy username:** Enter your proxy username in the text field.
   * (Optional) **Proxy password:** Enter your proxy password in the text field.

### **4. Define your SSL options**

Define your SSL options.

### **5. Define your keystore**

Define your keystore.
