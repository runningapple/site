---
title: 从买房到工厂模式
date: 2018-02-03 15:23:16
Modified:  2018-02-03 15:23:16
comments: true
category:  R&D
tags: 研发,设计模式,技术
Slug: factory-pattern
Author: 苍南竹竿君
---
![](http://wx1.sinaimg.cn/mw690/ad108d28gy1fo3lzxi20ij20dw092dgt.jpg)  
最近发现一件很有意思的事情，就是和同事一起吃饭聊天的话题一直在改变。梳理以下就是这样一种过程：刚刚入职那会儿聊的内容一般都是游戏，中间有时候会讨论一会儿技术类的话题，而后话题就变成了旅游，再之后就变成了买房，现在变成了买房+理财。买房这个话题已经足足聊了半年多了，还没有终止的意思，所以可以窥见买房对一个社会人来说是多么重要，以至于能成为这么多人的共同话题。  
当然今天也不是来讨论买房的，毕竟不能像土豪同事，买房和买菜一样。今天要总结另外一种设计模式------工厂模式。  
看了下网上很多人都把工厂模式分为三种：1.简单工厂模式。2.工厂方法模式。3.抽象工厂模式。其实个人觉得就只有两种，一个简单工厂模式（不能算工厂的工厂模式），二就是抽象工厂模式了。这里还是按自己的想法来汇总。<!--more-->  

---
### *普通工厂模式*
现在有这么一个场景你想去租一个房，我们可以自己直接找房东租，也可以找中介租。普通工厂模式就可以理解为找中介租房。找中介有什么好处呢？安全，有保证等。这同样也是普通工厂模式的优点。当然你也可以选择直接找房东租，这样更经济，但是如果出了什么问题都需要你一个人区解决。  
所以可以总结以下普通工厂模式就是“甩锅模式”。下面用代码演示  
```java
public class House {}//定义一个房子类，这里就忽略房东了。

public class HouseAgency {//定义租房中介，它有一个租房等方法（就是提供房子的方法）
    public House provideHouse() {
        return new House();
    }
}

public class FactoryTest {
    @Test
    public void simpleFactoryTest() {
        //我们直接找房东租房，这里忽略房东
        House house1 = new House();

        //我们通过租房中介租房
        HouseAgency agency = new HouseAgency();
        House house2 = agency.provideHouse();
    }
}
```
---
### *工厂方法/抽象工厂模式*
工厂方法和抽象工厂模式就不好用买房来讲解了，那就看看这两种模式是怎么定义的。  
工厂方法模式：定义一个用户创建对象的接口，让子类决定要实例化哪个类，使一个类的实例化延迟到其子类。  
抽象工厂模式：提供一个创建一系列相关或者相互依赖对象的接口，而无需指定他们具体的类。  
当产品只有一个的时候，抽象工厂模式就变成类工厂方法模式，当工厂方法模式的产品变成多个的时候，工厂方法模式就变成了抽象工厂模式。  
下面来看一个买房的例子。  
```java
//定义房子接口，提供一个房产商名。
public interface House {
    String getBrandName();
}

//碧桂园类实现房子接口
public class BiGuiYuan implements House {
    public String getBrandName() {
        return "碧桂园";
    }
}
//万科类实现房子接口
public class WanKe implements House {
    public String getBrandName() {
        return "万科";
    }
}
//定义一个房产商中介类（其实这里也可以算是抽象工厂了），提供一个卖房的方法。
public abstract class HouseAgency {
    public abstract House provideHouse();
}
//碧桂园中介类实现房产商中介类。
public class BiGuiYuanAgency extends HouseAgency {
    @Override
    public House provideHouse() {
        return new BiGuiYuan();
    }
}
//万科中介类实现房产商中介类。
public class WanKeAgency extends HouseAgency {
    @Override
    public House provideHouse() {
        return new WanKe();
    }
}

public class FactoryTest {
    @Test
    public void FactoryTest() {
        HouseAgency biGuiYuanAgency = new BiGuiYuanAgency();
        System.out.println(biGuiYuanAgency.provideHouse().getBrandName());
        //碧桂园
        HouseAgency wanKeAgency = new WanKeAgency();
        System.out.println(wanKeAgency.provideHouse().getBrandName());
        //万科
    }
}
```
以上就是一个工厂方法模式，工厂模式的好处是可以容易横向扩展，即如果现在万达也开盘了，那么只要加个 WanDa 类实现 House 接口，再加个 WanDaAgency 工厂类继承 HouseAgency 就实现去万达中介买房了。  
这里也看出工厂方法模式有个缺点就是如果房产商很多的话，类也会随之增多。（这也没办法，世界完美的事物总是难有）  
如果什么时候这些房地产商不仅卖住宅还卖配套的设施服务，如学校等的时候，下面就需要在加 School 类，并在 HouseAgency 里添加一个 provideSchool 的方法（或者说是提供教学服务的方法）。这样一来，代码就变成抽象工厂模式了。