---
title: JAVA 拾遗之 Vector
date: 2017-09-24 17:08:16
Modified:  2017-09-24 17:08:16
comments: true
category:  R&D
tags: 技术,研发,Java
Slug: java-collections-vector
Author: 苍南竹竿君
---

### 概要
上回剖析了 ArrayList 的源码，今天继续来剖析一下两个集合类型的源码 --- Vector。  

Vector 类用起来就像数组一样可以使用整数索引来访问容器中的内容。和数组的区别是 Vectror 可以根据需要改变容量，以适应 Vector 创建后进行的添加或者删除元素操作。  
Vectror 容器会通过维护 capacity 和 capacityIncrement 来优化存储管理。  
Vector 的 iterator 和 ListIterator 方法所返回的迭代器是 fail-fast 的。如果在迭代器创建后在任意时间从结构上修改了容器（通过迭代器自身的 remove 或者 add 方法之外的其它方式），则迭代器会抛出 ConcurrentModificationException。<!--more-->  

### add/addElement
Vector 中的 add 方法和 addElement 方法唯一的区别就是 add 方法返回元素是否添加成功， addElement 方法不返回数据。一般情况下用 add 方法居多。  

源码：
```java
public synchronized boolean add(E e) {
    modCount++;
    ensureCapacityHelper(elementCount + 1);
    elementData[elementCount++] = e;
    return true;
}

public synchronized void addElement(E obj) {
    modCount++;
    ensureCapacityHelper(elementCount + 1);
    elementData[elementCount++] = obj;
}
```

### clone
clone 方法返回当前容器的一个副本，这个副本一个对内部数据数组副本的引用，而不是用容器对象的原始内部数据数组的引用。  

```java
public synchronized Object clone() {
    try {
        @SuppressWarnings("unchecked")
            Vector<E> v = (Vector<E>) super.clone();//创建一个容器副本。
        v.elementData = Arrays.copyOf(elementData, elementCount);//复制原始数据数组，并将副本容器的 elementData 变量指向复制后的数组。
        v.modCount = 0;
        return v;
    } catch (CloneNotSupportedException e) {
        // this shouldn't happen, since we are Cloneable
        throw new InternalError(e);
    }
}
```

### copyInto
copyInto 方法将容器中的元素复制到指定数组中。其实就是调用了 System.arrayCopy 方法。  

```java
public synchronized void copyInto(Object[] anArray) {
    System.arraycopy(elementData, 0, anArray, 0, elementCount);
}
```  

### elementAt
 elemenmtAt 方法和 get 方法一模一样。都是返回制定索引处的元素。  

 ```java
public synchronized E elementAt(int index) {
    if (index >= elementCount) {
        throw new ArrayIndexOutOfBoundsException(index + " >= " + elementCount);
    }

    return elementData(index);
}

public synchronized E get(int index) {
    if (index >= elementCount)
        throw new ArrayIndexOutOfBoundsException(index);

    return elementData(index);
}
 ```

### elements
返回容器对象中的元素的枚举（Enumeration）。Enumeration 接口可以理解为迭代器，目前已经被迭代器取代，在如今已很少使用到。  

```java
public Enumeration<E> elements() {
    return new Enumeration<E>() {
        int count = 0;

        public boolean hasMoreElements() {
            return count < elementCount;
        }

        public E nextElement() {
            synchronized (Vector.this) {
                if (count < elementCount) {
                    return elementData(count++);
                }
            }
            throw new NoSuchElementException("Vector Enumeration");
        }
    };
}
```

### equals
比较指定对象与此容器对象到相等性。当指定到对象也是一个 List，两个 List 大小相同，并且其中所有对应的元素都相等的时候才返回 true。这个 equals 方法是调用其父类 AbstractList 的 equals 方法。  

```java
public boolean equals(Object o) {
    if (o == this)
        return true;
    if (!(o instanceof List))
        return false;

    ListIterator<E> e1 = listIterator();
    ListIterator<?> e2 = ((List<?>) o).listIterator();
    while (e1.hasNext() && e2.hasNext()) {
        E o1 = e1.next();
        Object o2 = e2.next();
        if (!(o1==null ? o2==null : o1.equals(o2)))
            return false;
    }
    return !(e1.hasNext() || e2.hasNext());
}
```

### insertElementAt
insertElementAt 方法和 ArrayList 中的 add(int index, E element) 方法如出一辙，而且 Vector 中的 add(int index, E element) 方法也是直接调用 insertElementAt 方法的。  
```java
public synchronized void insertElementAt(E obj, int index) {
    modCount++;
    if (index > elementCount) {
        throw new ArrayIndexOutOfBoundsException(index
                                                    + " > " + elementCount);
    }
    ensureCapacityHelper(elementCount + 1);
    System.arraycopy(elementData, index, elementData, index + 1, elementCount - index);
    elementData[index] = obj;
    elementCount++;
}
```

### clear/removeAllElements/removeAll
clear 方法直接调用 removeAllElements 方法。removeAllElements 方法的实现和 ArrayList 中的 clear 方法一样，都是先将数组引用设置为 null，设置 elementCount 为 0。最后等待 GC。  

```java
public synchronized void removeAllElements() {
    modCount++;
    // Let gc do its work
    for (int i = 0; i < elementCount; i++)
        elementData[i] = null;

    elementCount = 0;
}
```

removeAll 方法调用的是父类 AbstractList 中的 removeAll(Collections<?> e) 方法。删除容器中包含在 Collection 中的所有元素。  

```java
public boolean removeAll(Collection<?> c) {
    Objects.requireNonNull(c);
    boolean modified = false;
    Iterator<?> it = iterator();
    while (it.hasNext()) {
        if (c.contains(it.next())) {
            it.remove();
            modified = true;
        }
    }
    return modified;
}
```

### toArray
toArray 方法返回一个书中，包含容器中所有的元素。返回数组中的运行时类型为指定数组的类型。如果容器中的元素数量小于指定数组的大小，则返回该书中。否则使用此数组的运行时类型和此容器的元素数量分配一个新数组。  
如果容器中的元素数量小于指定数组容量，那么会在紧跟元素末尾的数组元素设置为 null。（这需要使用者知道容器中不包含任何 null 元素的情况下，才能确定容器的长度。）  
```java
public synchronized <T> T[] toArray(T[] a) {
    if (a.length < elementCount)
        return (T[]) Arrays.copyOf(elementData, elementCount, a.getClass());

    System.arraycopy(elementData, 0, a, 0, elementCount);

    if (a.length > elementCount)
        a[elementCount] = null;

    return a;
}
```

### Stack
Vector 有一个子类 Stack ，就是后进先出（LIFO）的栈。Stack 类有五个自有的方法（empty， peek， pop， push， search）。这五个自有方法的实现都是通过从 Vector 继承过来的方法实现的。  