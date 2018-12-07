---
title: JAVA 拾遗之 ArrayList
date: 2017-09-16 21:34:12
comments: true
categories: R&D
tags: [技术,研发,Java]
---
### 概要
上篇文章已经总结了最原始的集合接口 Collection 和 工具类 Iterator 迭代器。这篇文章将更全面的梳理一下 Java 集合体系。  

在 Java 中，集合类主要是从 Collection 和 Map 这两个接口 extends 或者 implements 来的。  

Collection 体系树图：  
![](http://wx1.sinaimg.cn/mw690/ad108d28gy1fjlci6lgogj20nt0cqdfz.jpg)  

Collection 集合体系中，Queue 是 Java 提供的队列实现。另外 Set 和 List 接口是继承于 Collection 接口的子接口，Set 属于无序集合，List 属于有序集合。<!--more-->  

Map 体系树图：  
![](http://wx3.sinaimg.cn/mw690/ad108d28gy1fjlci6zkstj20lc0dm3yk.jpg)  

Map 集合体系相较于 Collection 集合体系有一个很明显的特征，Map 都是以 Key-value 形式保存数据的，并且 Key 值唯一。  

一般我们把 Java 中的集合分成三大类，List、Map、Set。  
* List：有序的集合，可以对列表中每个元素的位置进行精确的控制。可以根据元素的整数索引访问元素。列表允许重复的元素存在。  

* Set：不允许重复元素的集合（Set 不包含满足 e1.equals(e2) 的元素 e1 和 e2）。Set 中最多包含一个 null 元素。  

* Map：将键映射到值的对象。一个映射不能包含重复的键，每个键最多只能映射到一个值。Map 接口取代了 Dictionary （抽象）类。  


*下面来细细研究下 Java 中具体的集合实现*
### ArrayList

#### add 方法
ArrayList 类中提供了两个 add 方法。一个是直接向列表尾部添加元素的，另外一个是向指定位置添加元素的。 
```java
ArrayList<Integer> list = new ArrayList<Integer>(10);
list.add(1);
list.add(2);
list.add(3);
System.out.println(list);//[1, 2, 3]
list.add(1, 10);
System.out.println(list);//[1, 10, 2, 3]
```
来看一看这两个 add 方法的源码：  
```java
public boolean add(E e) {
    //如有必要，增加此 ArrayList 实例的容量，以确保它至少能够容纳最小容量参数所指定的元素数
    ensureCapacityInternal(size + 1);
    elementData[size++] = e;
    return true;
}

public void add(int index, E element) {
    rangeCheckForAdd(index);

    ensureCapacityInternal(size + 1);
    System.arraycopy(elementData, index, elementData, index + 1,
                        size - index);
    elementData[index] = element;
    size++;
}
```
从源码可以看出来向列表（数组实现的列表）尾部添加的元素的方法，没什么特别的只是先扩展了数组的空间，然后再向数组添加新的元素。  

向指定位置添加元素的方法实现还是比较有意思的，它首先检查了待插入元素的下标是否越界，如果越界的话会抛出 IndexOutOfBoundsException 异常，如果下标在数组的空间范围内，则对数组重新扩容，再之后将元素插入到指定的下标位置上（其实就是调用 System.arraycopy 对数组自身进行复制，空出 index 那个位置给待插入的元素，复制好后再进行插入操作）  

#### remove
ArrayList 类中也提供了两个 remove 方法。一个是直接移除指定下标的元素，另一个是移除列表中首次出现的元素。  
```java
ArrayList<Integer> list = new ArrayList<Integer>(10);
list.add(1);
list.add(2);
list.add(3);
list.add(4);
list.add(5);
System.out.println(list);//[1, 2, 3, 4, 5]
list.remove(2);
System.out.println(list);//[1, 2, 4, 5]
list.remove(new Integer(4));
System.out.println(list);//[1, 2, 5]
```

源码：  
```java
public E remove(int index) {
    rangeCheck(index);

    modCount++;//操作数
    E oldValue = elementData(index);

    int numMoved = size - index - 1;
    if (numMoved > 0)
        System.arraycopy(elementData, index+1, elementData, index,
                            numMoved);
    elementData[--size] = null;//指向 null ，等待垃圾回收

    return oldValue;
}

public boolean remove(Object o) {
    if (o == null) {
        for (int index = 0; index < size; index++)
            if (elementData[index] == null) {
                fastRemove(index);
                return true;
            }
    } else {
        for (int index = 0; index < size; index++)
            if (o.equals(elementData[index])) {
                fastRemove(index);
                return true;
            }
    }
    return false;
}

private void fastRemove(int index) {
    modCount++;
    int numMoved = size - index - 1;
    if (numMoved > 0)
        System.arraycopy(elementData, index+1, elementData, index,
                            numMoved);
    elementData[--size] = null;
}
```

从源码我们可以发现删除指定位置的元素其实和向指定位置添加元素的做法是差不多的。  
删除首次出现的元素比删除指定位置元素就多了两步操作。第一步是判断待删除的元素是否为 null。这里为什么要判断是否为 null 呢？这就考验基础知识扎实不扎实了，我们都知道 null 可是没有 equals 方法的，如果不进行判断，那么编译时虽然不会报异常，但是运行时如果传入了 null，那就报错了。所以这里必须要先判断待删除元素是否为 null 。第二步是遍历数组查找待删除元素在数组中的位置。找到了就进行删除操作，删除操作和第一种 remove 方法一致。  

#### clear  

clear 方法顾名思义就是清空列表中的所有元素。  

```java
ArrayList<Integer> list = new ArrayList<Integer>(10);
list.add(1);
list.add(1);
list.add(1);
System.out.println(list);//[1, 1, 1]
list.clear();
System.out.println(list);//[]
```

源码：  
```java
modCount++;

for (int i = 0; i < size; i++)
    elementData[i] = null;

size = 0;
```
clear 方法真的是言简意赅，直接将数组中的所有对象引用清空，全部指向 null 。剩下的操作就等着 JVM 进行垃圾回收处理了。  

#### indexOf  
indexOf 方法说白了就是第二种删除操作的第一步。  

#### ensureCapacity  
如有必要，增加此 ArrayList 实例的容量，以确保它至少能够容纳最小容量参数所指定的元素数。  
源码：  
```java
public void ensureCapacity(int minCapacity) {
    int minExpand = (elementData != EMPTY_ELEMENTDATA)
        ? 0 : DEFAULT_CAPACITY;

    if (minCapacity > minExpand) {
        ensureExplicitCapacity(minCapacity);
    }
}

private void ensureCapacityInternal(int minCapacity) {
    if (elementData == EMPTY_ELEMENTDATA) {
        minCapacity = Math.max(DEFAULT_CAPACITY, minCapacity);
    }

    ensureExplicitCapacity(minCapacity);
}

private void ensureExplicitCapacity(int minCapacity) {
    modCount++;

    if (minCapacity - elementData.length > 0)
        grow(minCapacity);
}

private static final int MAX_ARRAY_SIZE = Integer.MAX_VALUE - 8;

private void grow(int minCapacity) {
    int oldCapacity = elementData.length;
    int newCapacity = oldCapacity + (oldCapacity >> 1);
    if (newCapacity - minCapacity < 0)
        newCapacity = minCapacity;
    if (newCapacity - MAX_ARRAY_SIZE > 0)
        newCapacity = hugeCapacity(minCapacity);
    elementData = Arrays.copyOf(elementData, newCapacity);
}

private static int hugeCapacity(int minCapacity) {
    if (minCapacity < 0) 
        throw new OutOfMemoryError();
    return (minCapacity > MAX_ARRAY_SIZE) ?
        Integer.MAX_VALUE :
        MAX_ARRAY_SIZE;
}
```

从源码实现来看 ensureCapacity 方法可以扩大数组空间，默认情况下当数组空间已经不够的时候，数组长度会扩大为原来数组长度的 1.5 倍。当程序员自己设定大小的时候，如果设定的长度比原来数组长度的 1.5 倍小，则将数组扩大到程序员设定的值，反之设置为原来长度的 1.5 倍。  
在开发时，如果知道长度的情况下，可以先用 ensureCapacity 方法设定足够长的数组长度，避免程序运行时候进行重复的数值扩容操作，提高程序的效率。  

#### trimToSize  
trimToSize 方法作用是将列表对象的实例容量调整为列表当前大小。  
源码：  
```java
public void trimToSize() {
    modCount++;
    if (size < elementData.length) {
        elementData = Arrays.copyOf(elementData, size);
    }
}
```

#### RandomAccess  
RandomAccess 接口是一个标志接口，本身并没有提供任何方法，任何实现了 RandomAccess 接口的对象都可以认为是支持快速随机访问的对象。此接口的主要目的就是标识那些课支持快速随机访问的 List 实现。  
在 JDK 实现中，任何基于数组的 List 实现都实现了 RandomAccess 接口（也只有数组能够进行快速的随机访问了~），而基于链表的实现则没有。  
有了这个接口，我们就可以程序中要处理的 List 对象是否可以进行快速随机访问，针对不同 List 对象使用不同操作，以提高程序性能。  

```java
ArrayList<Integer> list = new ArrayList<Integer>(5);
list.add(1);
list.add(1);
list.add(1);
if (list instanceof RandomAccess) {
    for (int i = 0; i < list.size(); i++) {
        System.out.println(list.get(i));
    }
} else {
    Iterator iterator = list.iterator();
    while (iterator.hasNext()) {
        System.out.println(iterator.next());
    }
}
```

#### fail-fast  
fail-fast 机制还是今天刚刚知道的，所以这个知识对我来说是十分热乎的。fail-fast 是 Java 集合中的一种错误机制。当多个线程对同一个集合的内容进行操作时，就可能会产生 fail-fast 事件，抛出 ConcurrentModificationException 异常。而且 ArrayList 本来就不是线程安全的集合。  

源码：
```java
public void replaceAll(UnaryOperator<E> operator) {
    Objects.requireNonNull(operator);
    final int expectedModCount = modCount;
    final int size = this.size;
    for (int i=0; modCount == expectedModCount && i < size; i++) {
        elementData[i] = operator.apply((E) elementData[i]);
    }
    if (modCount != expectedModCount) {
        throw new ConcurrentModificationException();
    }
    modCount++;
}
```

从 replaceAll 方法的源码可以知道这个方法也有可能出现 fail-fast 事件。首先这里的 modCount 存储的是当前 ArrayList 对象进行操作的操作数，expectedModCount 是 final 修饰的，也就是说当前情况下 expectedModCount 这个变量的值是不能改变的。那么什么情况下会出现 modCount != expectedModCount 呢？很简单，如果此刻有一个线程对当前这个 ArrayList 对象进行了添加或者删除等操作，modCount 值就变了，就会抛出 ConcurrentModificationException 异常。  

*以下是待总结的集合*
### LinkedList

### Vector

### Stack

### ArrayDeque

### HashSet

### TreeSet

### EnumSet

### LinkedHashSet

### PriorityQueue

### HashMap

### HashTable

### TreeMap

### EnumMap

### LinkedHashMap

### WeakHashMap

### IdentityHashMap