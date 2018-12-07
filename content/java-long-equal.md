---
title: Java 长整型相等判断
date: 2018-07-09 21:35:08
comments: true
categories: R&D
tags: [研发,Java,技术,GAN计划]
---
上周在做一个 ID 相等判断的时候，因为是 ID 是 Long 类型，所以当时出现了一个问题“明明是一样的 ID，却怎么也不相等”。<!--more-->    
后来自己测试了下：  
```java
Long a = 1L;
Long b = 1L;
System.out.println(a == b);//true
Long c = 1233L;
Long d = 1233L;
System.out.println(c == d);//false
```
上面代码编译后为：  
```java
Long var1 = Long.valueOf(1L);
Long var2 = Long.valueOf(1L);
System.out.println(var1 == var2);
Long var3 = Long.valueOf(1233L);
Long var4 = Long.valueOf(1233L);
System.out.println(var3 == var4);
```
看看 Long 类中的 valueOf 方法：  
```java
public static Long valueOf(long l) {
    final int offset = 128;
    if (l >= -128 && l <= 127) { // will cache
        return LongCache.cache[(int)l + offset];
    }
    return new Long(l);
}
```
从源码可以看出来，当数值在[-128, 127]范围内的，都会被放入缓存中，否则就创建一个 Long 对象。我们都知道对象判断相等不能用 == ，而是用 equals 方法。所以判断 Long 类型对象是否相等，应该这么写：  
```java
Long c = 1233L;
Long d = 1233L;
System.out.println(c.equals(b));//true
```