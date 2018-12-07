---
title: 从唐伯虎点秋香到迭代器模式
date: 2018-02-07 00:01:23
Modified:  2018-02-07 00:01:23
comments: true
category:  R&D
tags: 研发,设计模式,技术
Slug: iterator-pattern
Author: 苍南竹竿君
---
![](http://wx4.sinaimg.cn/mw690/ad108d28gy1fo763toi44j20og0dw75h.jpg)  
在电影唐伯虎点秋香中，华夫人为了为难唐伯虎，让秋香和华府都所有丫鬟都盖上红头巾，排排站，让唐伯虎在几米开外指认出秋香，唐伯虎每次指认一个人，华府都“保安头头”就会去掀起那位姑娘都头巾，确认是否为秋香。当然在电影中唐伯虎只有 3 次指认机会。  
其实唐伯虎点秋香有点儿类似设计模式中的迭代器模式---<font color=blue face="黑体">提供一种方法顺序访问一个聚合对象中各个元素, 而又无须暴露该对象的内部表示。</font>(有一点是在迭代器模式中没有被要求说只能迭代查找 3 次。)<!--more-->  

下面用代卖来演示以下：
```java
//定义一个迭代器都接口
public interface Iterator {
    boolean hasNext();
    Object next();
}
//容器都接口。
public interface Container {
    void add(Object obj);
    Iterator createIterator();//工厂模式创建新的迭代器。
}
//实现我们自己的迭代器。（保安头头）
public class MyIterator implements Iterator {
    private List<Object> list;
    private Integer index;

    public MyIterator(List<Object> list) {
        this.list = list;
        index = 0;
    }

    public boolean hasNext() {
        return index != list.size();
    }

    public Object next() {
        if (hasNext()) {
            return list.get(index++);
        }
        return null;
    }
}

//实现自己的迭代器。
public class MyContainer implements Container {
    private List<Object> list;

    public MyContainer(List<Object> list) {
        this.list = list;
    }

    public void add(Object obj) {
        list.add(obj);
    }

    public Iterator createIterator() {
        return new MyIterator(list);
    }
}

public class IteratorTest {

    @Test
    public void iteratorTest() {
        List<Object> list = new ArrayList<Object>();
        list.add("石榴姐");
        list.add("冬香");
        Container container = new MyContainer(list);
        container.add("秋香");
        Iterator iterator = container.createIterator();
        while (iterator.hasNext()) {
            System.out.println(iterator.next());
        }
        //石榴姐 冬香 秋香
    }
}

```
上面代码中生成迭代器使用了工厂模式，简化了用户创建迭代器的过程。  
接下来看看跌倒器模式的有缺点。
> 优点： 1、它支持以不同的方式遍历一个聚合对象。 2、迭代器简化了聚合类。 3、在同一个聚合上可以有多个遍历。 4、在迭代器模式中，增加新的聚合类和迭代器类都很方便，无须修改原有代码。  
缺点：由于迭代器模式将存储数据和遍历数据的职责分离，增加新的聚合类需要对应增加新的迭代器类，类的个数成对增加，这在一定程度上增加了系统的复杂性。
