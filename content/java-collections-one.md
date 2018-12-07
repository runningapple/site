---
title: JAVA 拾遗之集合接口
date: 2017-09-14 22:40:32
Modified:  2017-09-14 22:40:32
comments: true
category:  R&D
tags: 技术,研发,Java
Slug: java-collections-one
Author: 苍南竹竿君
---
### 概要
与现代等数据结构类库一样（C++ 中的 STL），Java 集合类库也将接口与实现分离。值得一提的是从 Java 1.5 之后，集合类都是带有类型参数的泛型类，这对于开发带来的便利性不言而喻。  

### 集合接口  
#### Collection
在 Java 类库中，集合类的基本接口是 Collection 接口。Collection 只表示一组对象，这些对象也称之为 collection 的元素。一些 collec 允许有重复的元素，而外一些则不允许。一些是 collection 是有序的，另外一些则是无序的。JDK 不提供此接口的任何直接实现。它在子接口中提供更具体的实现（如 Set 和 List）。  
```java
public interface Collection<E> {
    boolean add(E element);
    Iterator<E> iterator();
    ...
}
```
在 Collection 接口中有几个方法，包括 add, addAll, remove 等。其中一个 iterator 方法用于返回一个实现了 Iterator 接口的对象。我们可以使用这个对象依次遍历集合中的元素。 <!--more--> 

#### Iterator
在 Java8 之前，Iterator 接口只包含三个方法：
```java
public interface Iterator<E> {
    E next();
    boolean hasNext();
    void remove();
}
```
可以通过调用 next 方法来遍历集合中等元素。但是如果到达了集合等末尾，next 方法将抛出一个 NoSuchElementException 。因此在调用 next 方法之前应该先调用 hasNext 方法，如果迭代器对象还有多个可访问等元素，hasNext 方法将返回 true。  
```java
List<String> list1 = new ArrayList<String>();
list1.add("hello");
list1.add("world");
Iterator<String> iter = list1.iterator();
while (iter.hasNext()) {
    System.out.println(iter.next());
}
```

#### Iterable
从 Java5 开始多了一种优雅等方式来遍历集合---“for each”。这里等 “for each” 与 Java8 中的 for each 还是不一样的（待研究过 Java8 细节后再来探讨异同之处）。
```java
List<String> list1 = new ArrayList<String>();
list1.add("hello");
list1.add("world");
Iterator<String> iter = list1.iterator();
for(String item : list1) {
    System.out.println(item);
}
```
可以看出比用迭代器遍历简洁优雅许多。  
但是，只有数组或者实现了 Iterable 接口的对象才能使用 “for each” 来遍历。因为 Collection 接口扩展了 Iterable 接口，所以在 Java 标准库中的任何集合都是可以使用 “for each” 来遍历元素的。  
另外，通过查看编译后的字节码来看，“for each”更像是语法糖，它的实现只是编译器帮我们做了 for 遍历或者 迭代器遍历。
源代码：
```java
int[] a = {1,2,3};
for (int item : a) {
    System.out.println(item);
}
        List<String> list1 = new ArrayList<String>();
list1.add("hello");
list1.add("world");

for(String item : list1) {
    System.out.println(item);
}
```

编译后的字节码：
```java
int[] var1 = new int[]{1, 2, 3};
int[] var2 = var1;
int var3 = var1.length;

for(int var4 = 0; var4 < var3; ++var4) {
    int var5 = var2[var4];
    System.out.println(var5);
}

ArrayList var6 = new ArrayList();
var6.add("hello");
var6.add("world");
Iterator var7 = var6.iterator();

while(var7.hasNext()) {
    String var8 = (String)var7.next();
    System.out.println(var8);
}
```
所以说，其实你用迭代器和普通的 for 循环，还是用 for each 遍历其实效率上是差不多的，唯一的优势就是代码整洁性和代码编写效率上 for each 占很大优势。