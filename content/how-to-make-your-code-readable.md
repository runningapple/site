---
title: 如何让你的代码更具有可读性
date: 2018-07-04 19:32:19
Modified:  2018-07-04 19:32:19
comments: true
category:  R&D
tags: 研发,技术,GAN计划
Slug: how-to-make-your-code-readable
Author: 苍南竹竿君
---
![](http://wx2.sinaimg.cn/mw690/ad108d28gy1fsy89smpy4j21pc0yiwl2.jpg)  
我们都曾见过（或者写过）一些“坏”代码。我们也都希望能够改善写代码的技能，而不仅仅是学习新的技能。<!--more-->  

### 为什么我们需要写优秀的代码，而不仅仅是性能良好的代码？
虽然你开发的产品或者网站的性能表现非常重要，但是你写的代码的“颜值”其实也很重要。这背后的原因是需要读你代码的“人”并不是只有机器。  
首先，也是最重要的一点是如果因为 bug 而不得不重新阅读自己写的代码，如果不是读全部代码的话，那时候就算是再“高性能”的代码也不会对理解自己所写的代码有所帮助，更别说修复问题所在。  
其次，如果你是和一个团队一起工作的话，那么任何时候你团队里其他小伙伴都有可能不得不阅读你的代码并以他们自己的方式来理解代码的意思。为了让小伙伴们更加容易理解代码，我们在写代码的时候应该考虑变量以及方法的命名，每一行的长度，代码的结构，以及其它注意事项。  
最后，代码的“颜值”就会足够高了。  

### 如何识别坏代码？
我以为有一种非常简单方式来识别坏代码，就以句子或者短语的方式来阅读你的代码。  
例如：
```js
const traverseUpUntil = (el, f) => {
    let p = el.parentNode
    while (p.parentNode && !f(p)) {
        p = p.parentNode
    }
    return p
}
```
上面的方法的功能是，传进一个元素和一个条件方法，返回最靠近元素的父节点并且当前节点能通过条件方法的判断。  

```js
const traverseUpUntil = (el, f) => {
```
根据识别坏代码的思想，代码需要像平时写文字一样可阅读，那么这一行代码已经有 3 个致命破绽。  
* 方法参数无法像词语一样可读（可理解）
* 虽然 el 通常能被理解为 element，但是变量名 f 并不能解释其作用
* 假使你要使用这个方法，你可能会这样理解这个方法：“遍历元素直到 el 通过 f 的判断”，当然如果能这样理解更好：“从 el 中遍历元素直到元素通过 f 的判断”。诚然，处理这个问题的最好方式就是允许方法能以 el.tranverseUpUnti(f) 调用，但是这就是另外一个问题了。

```js
let p = el.parentNode
```
第二行代码同样有命名问题。如果一个人看到这行代码应该能理解这个 p 是什么，就是参数 el 的 parentNode。但是，如果我们看到其他地方使用了 p 的话，我们就很难去理解这个 p 了，因为我们已经没有上下文可以去解释它了。  

```js
while (p.parentNode && !f(p)) {
```
在这一行，我们碰到的主要问题是无法知晓功能的 !f(p) 到底是什么意思，它是做什么的，因为 f 可以代表任何方法在这里。而阅读代码的人应该把 !f(p) 理解为确认当前的节点是否能够通过其条件判断。如果能通过，则停止循环。  

```js
p = p.parentNode
```
这一行具有非常好的自译性。  

```js
return p
```
这一行由于糟糕的变量命名，并不能 100% 的清楚到底返回了什么。  
![](http://wx4.sinaimg.cn/mw690/ad108d28gy1fsy89rpbh5j21n20x813d.jpg)  

### 开始改进代码
```js
const traverseUpUntil = (condition, node) => {
    let parent = node
    do {
        parent = parent.parentNode
    } while (parent.parentNode && !condition(parent))
    return parent
}
```
首先我们先将变量名和其顺序做了调整：(el, f) => 改为了 (condition, node) =>  
你可能会奇怪为什么不用 element， 而是用 node 命名。我使用 node 命名的原因如下：  
* 我们在写代码的时候已经有节点（nodes）这个概念，比如 .parentNode，所以为什么不让所以节点命名都统一呢？
* node 写起来比 element 短而且也不会失去其作用。我之所以这么说的原因是它对所有具有 parentNode 属性的节点元素都起作用，而不仅仅是 HTML 元素。

接下来我们再给变量名润色：  
```js
let parent = node
```
用变量名完整的阐述变量的含义这很重要，p 现在改为了 parent，你可能注意到了我们并没有以获取到 node.parentNode 作为开始，而是只是获取到 node 就开始了。  
接着让我们进入接下来的几行代码：  
```js
do {
    parent = parent.parentNode
} while (parent.parentNode && !condition(parent))
```
我们用 do...while 替换了 while 循环。这就代表着我们只需要获取一次 parent 节点，因为条件判断是在花括号里的代码执行之后才执行的。do...while 的使用也让我们回到了能像写文章一样的去阅读代码方式。  

让我们尝试读懂它：“让 parent 等于 parent 的父节点（parent node）当这个节点有父节点并且条件判断方法返回 true 时”。虽然这看起来可能有点儿奇怪，但是在我们读这段代码的时候能帮助我们非常容易的理解这段代码的意思。  

```js
return parent
```
虽然很多人会选择使用 ret 这种通用的变量名（或者 returnValue），但是 返回一个以 ret 命名的变量并不是一个好的尝试。如果你返回了一个以合适的变量名命名的变量，那么你返回的内容就变得显而易见，更容易让人理解。有时候方法体可能非常长也可能非常短导致一个方法可能非常混乱。在这种情况下，我的建议是将你的方法切分为多个方法，如果这样还是很复杂，那么添加一些注释会有所帮助。  

### 简化代码
你已经让你的代码变得可读可理解了，现在是时候将不必要的代码去除掉了。我相信你们之中的有些人已经注意到，我们实际上并不需要 parent 变量。  
```js
const traverseUpUtil = (condition, node) => {
    do{
        node = node.parenNode
    } while (node.parentNode && !condition(node))
    return node
}
```
我所做的就是移除了第一行，并且用 node 替换了 parent。这样我们就绕过了创建 parent 的过程，直接进入循环了。  
![](http://wx4.sinaimg.cn/mw690/ad108d28gy1fsy89q2jw6j21pc0yin3q.jpg)  

### 关于变量名？
虽然 node 这个变量名已经很“像样”的描述了变量的含义，但是这次让我们不要安逸于“像样”，我们来重新为它取个名字。currentNode 如何？  
```js
const traverseUpUntil = (condition, currentNode) => {
    do {
        currentNode = currentNode.parentNode
    } while (currentNode.parentNode && !condition(currentNode))
    return currentNode
}
```
这样就好多了！当我们再读这段代码可以知道无论怎么样 currentNode 都将代表当前的节点而不是其它节点。  



原文：https://medium.com/@chbchb55/the-importance-of-readable-code-165895e939c7