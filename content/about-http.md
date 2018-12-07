---
title: HTTP协议总结
date: 2017-3-11 08:28:01
comments: true
categories: R&D
tags: [R&D,技术,研发]
---
#### HTTP 协议简介
HTTP 协议是从 1990 年开始背广泛应用于**客户端-服务端**模式网络的协议。在任何时候，只要你上网打开网页，你的浏览器就会向服务器发送 HTTP 请求信息。服务器便会处理请求，然后返回响应信息，响应信息里包含有客户端所请求的信息内容。<!--more-->  
******  
#### HTTP 请求信息  
HTTP请求信息是由一个简单的文本结构组成。  
下面是在IE浏览器下发送的一段请求信息：
<pre>
<code>
GET / HTTP/1.1
Accept: */*
Accept-Language: en-gb
Accept-Encoding: gzip, deflate
User-Agent: Mozilla/5.0 (Windows NT 6.3; WOW64; Trident/7.0; rv:11.0) like Gecko
Host: www.baidu.com
Connection: Keep-Alive
</code>
</pre>  
第一行请求信息包括：  
1. HTTP 对待请求方法。  
2. 相对 URL 地址或者绝对 URL 地址。  
3. 使用 HTTP 协议的版本。现在大部分使用的版本还是 1.1 版本的。  

剩下的信息包括由 name：value 结构组成的集合，就是HTTP表头。HTTP 客户端通过表头里的信息来告诉服务器如何处理请求的信息。例如，**Accept-Encoding: gzip, deflate** 就是告诉服务器，我们客户端用的是 gzip 或者 deflate 算法来压缩内容的。  
******  
#### HTTP 响应信息  
HTTP 响应信息和请求信息有着相似的结构，但是响应信息在其内容后面会跟着客户端所请求的内容，如 HTML 页面。下面是一段服务器端响应信息：  
<pre>
<code>
HTTP/1.1 200 OK
Date: Mon, 04 Jan 2015 12:04:43 GMT
Cache-Control: no-cache, no-store
Expires: -1
Content-Type: text/html; charset=utf-8
Content-Length: 14990

&lt;!DOCTYPE html>  &lt;html>...
</code>
</pre>  
第一行显示的是状态码，表示 HTTP 请求成功。返回 200 表示请求被正确接收处理，并且所请求的内容已经返回给客户端了。剩下的几行信息是用来描述服务端所返回的数据格式或者类型，或者处理方式等。例如，**Content-Type: text/html; charset=utf-8** 表示返回的内容是 text/html 格式。  
响应信息的表头用两个回车换行结束，即（CRLF，carriage return, line feed），两个回车换行后更着的内容就是客户端所请求的内容。  
  
**注意**，像图片，视频等内容并不会直接嵌入在页面中，而是指定用 HTML 中的 &lt;img> 等标签代替，使图片内容，和普通的文本内容分开，直到浏览器渲染时遇到了 &lt;img> 标签，遇到之后，浏览器就会去找对应的图片信息是否已经被加载到了内存中或者保存到了 cache 里了，如果找到了则将图片嵌入到页面中。如果浏览器没有找到对应的图片，则会另外发起一个 HTTP 请求，来请求图片。
******  
#### AJAX  
AJAX 是一种可以让 HTTP 请求不会导致页面整体刷新的技术。
在传统的 web 应用中，浏览器会因为服务端的一些操作导致渲染一系列 HTML 页面。  

在传统的 web 应用中，用户每次输入一些数据并提交表单，浏览器会向服务器发起请求，让服务端进行数据操作处理，服务端请求到内容返回给浏览器，浏览器将会重新渲染页面。  

使用 AJAX 技术的 web 应用，在向服务端发起请求后，服务端在操作处理后，会返回请求的数据，这里的数据不一定是 HTML 。因为使用 AJAX 技术的页面并不会自动渲染，而是用 JavaScript 操作 DOM 元素等一系列动作将数据展示到页面上。一般 AJAX 请求到数据是以 XML 或者 JSON 形式返回的。  

AJAX 主要的功能已经现在的绝大数浏览器的 XmlHttpRequest 对象里实现。下面展示一段用原生 javascript 使用 AJAX 技术发送数据。  
<pre>
<code>
&lt;script type="text/javascript">
function AddNumbers()
{
    // 创建一个 HTTP 对象实例
    var xmlHttp = new XMLHttpRequest();
    var value1 = document.getElementById("txtValue1").value;
    var value2 = document.getElementById("txtValue2").value;
    // 制定 HTTP POST 请求，这样请求参数才可以添加进去。
    // 请求体
    xmlHttp.open("POST", "add.aspx", false);
    // 发送数据
    xmlHttp.send(value1 + "," + value2);
    var result = document.getElementById("spanResult");
    // 将服务端发送过来的数据添加到对应的 HTML 元素里。
    result.innerHTML = xmlHttp.responseText;
}
&lt;/script>
&lt;form>
    &lt;input id="txtValue1"/>
   &lt;input id="txtValue2"/>
    &lt;input onclick="AddNumbers();"type="button" value="Add"/>
    &lt;p>Result:&lt;/p>
    &lt;span id="spanResult">&lt;/span>
&lt;/form>
</code>
</pre>  
另外，我们现在一般都用 JavaScript 库实现的 AJAX 。比如 JQuery。
