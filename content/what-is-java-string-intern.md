---
title: 初探 String.intern
date: 2018-07-01 14:03:29
comments: true
categories: R&D
tags: [研发,Java,技术,GAN计划]
---
### 瞎扯
前天晚上看了《深入理解JVM》的第一章内容，发现有太多东西都不理解，比如显卡和 CPU 的计算能力区别，再比如为什么 JVM在 32 位和 64 位架构下性能会不一样等。这些点后续还是要去查资料理清楚，今天抽点时间让自己熟悉一下之前从未用过的一个 String 方法 intern(JDK 1.8)。<!--more-->  

### intern 方法是什么？
关于 intern 方法，先看下相关 api 的介绍。  
```java
/**
* Returns a canonical representation for the string object.
* <p>
* A pool of strings, initially empty, is maintained privately by the
* class {@code String}.
* <p>
* When the intern method is invoked, if the pool already contains a
* string equal to this {@code String} object as determined by
* the {@link #equals(Object)} method, then the string from the pool is
* returned. Otherwise, this {@code String} object is added to the
* pool and a reference to this {@code String} object is returned.
* <p>
* It follows that for any two strings {@code s} and {@code t},
* {@code s.intern() == t.intern()} is {@code true}
* if and only if {@code s.equals(t)} is {@code true}.
* <p>
* All literal strings and string-valued constant expressions are
* interned. String literals are defined in section 3.10.5 of the
* <cite>The Java&trade; Language Specification</cite>.
*
* @return  a string that has the same contents as this string, but is
*          guaranteed to be from a pool of unique strings.
*/
public native String intern();
```
intern 方法是一个 native 方法。从 api 的注释可以知道，intern 方法是返回一个字符串对象引用的。  
当一个字符串对象调用了 intern 方法，如果常量池中已经存在该字符串，则直接返回常量池中该字符串对象的引用。否则在常量池中加入该对象，并返回该对象的引用。  

### 举个栗子
```java
String str1 = "a";
String str2 = "b";
String str3 = "ab";
String str4 = str1 + str2;
String str5 = new String("ab");

//true，字符串比较
System.out.println(str5.equals(str3)); 

//false，地址比较
System.out.println(str5 == str3);

//true，str5 执行 intern 方法，从常量池中查找是否有字符串对象 “ab”，发现已经存在了，即 str3，所以直接直接返回常量池中 “ab”的地址。
System.out.println(str5.intern() == str3);

//false，str1+str2 实际上是使用了 StringBuilder.append 来生成了新的对象。
System.out.println(str5.intern() == str4);，

String ss2 = new String("1");
ss2.intern();
String tt = "1";
//false，ss2 还是堆中字符串对象“1”的地址。
System.out.println(ss2 == tt);


String s3 = new String("1") + new String("1");
s3.intern();
String s4= "11";
//true，s3.intern() 在常量池中添加了一个对堆中字符串对象 “11” 的引用。s4 = “11” 发现字符串常量池中已经存在字符串对象”11“了，所以直接返回该字符串地址
//(注意这里是引用 ，就是这个区别于JDK 1.6的地方。在JDK1.6下是生成原字符串的拷贝)
System.out.println(s3 == s4);

String s5 = new String("1") + new String("1");
String s6= "11";
s5.intern();
//false，s6 = "11" 先查找字符串常量池中是否有字符串对象”11“，发现没有，然后在字符串常量池中添加字符串对象”11“。s5.intern() 也先查找字符串常量池中是否存在字符串对象”11“，发现已经存在，则直接返回该字符串的地址（注意这里只是返回字符串常量池中”11“的地址，并没有把返回的地址赋值给 s5）。
System.out.println(s5 == s6);
```
以上例子基本能说明 intern 方法究竟是做什么的了。  

### 使用场景
个人想到的是如果在一个场景中需要用到很多字符串，但是大部分字符串都是重复的，那么我们就可以用 intern 方法来减少创建重复字符串的内存开销。  
```java
String[] names = {"TOM AND JERRY", "ONE PIECE", "OLD MAN AND THE SEA"};
String[] result = new String[];
for (int i = 0; i < 1000; i++) {
    result[i] = new String(names[i % names.length]).intern();
}
System.gc();
```

参考：  
《深入理解JVM》  
https://www.cnblogs.com/Kidezyq/p/8040338.html  
https://blog.csdn.net/soonfly/article/details/70147205  