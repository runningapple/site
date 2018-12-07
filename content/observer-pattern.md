---
title: 从大疆稳定器没货到观察者模式
date: 2018-02-07 19:16:46
comments: true
categories: R&D
tags: [研发,设计模式,技术]
---
今年 CES 会展上大疆公司出了一个手机稳定器 osmo mobile2 ，性价比非常高。昨天看了下相关的评测视频，心动了，就准备去买一个过年时候拍拍视频用，可气的是各种渠道都没有货了。官网只显示到货后通知。。。  
![](http://wx3.sinaimg.cn/mw690/ad108d28gy1fo82w06trlj20rr0af3z9.jpg)  
那过年只能用人体稳定器先将就一下了。<!--more-->
当然，今天也不是吐槽这件事的，而是和上面这幅图片有关“有现货通知我”------观察者模式。没错，又是一种设计模式。  
先来描述一下这个真实的场景：大疆公司和大疆商品潜在购买者的关系。大疆 osmo mobile2 现在没有货了，所以用户现在只能等着，但是用户是无法知道大疆什么时候会有货的，所以就需要大疆公司有货的时候，去通知这些潜在的购买者。这就是观察者模式的一种体现。  
言简意赅的说就是：观察者模式就是当一个对象被修改时，则会自动通知它的依赖对象。  
接下来用代码来描述这个真实的场景：  
```java
//抽象出客户类
public abstract class Customer {
    abstract void mailUpdate(String msg);
}
//抽象出供应商类
public class Provider {

    private List<Customer> customers = new ArrayList<Customer>();

    public void order(Customer customer) {      //添加订阅通知的客户
        customers.add(customer);
    }

    public void cancelOrder(Customer customer) {    //删除取消订阅通知的客户
        customers.remove(customer);
    }

    public void remind(String msg) {    //供应商通知每个有订阅通知的客户
        for (Customer customer : customers) {
            customer.mailUpdate(msg);
        }
    }
}
//大疆客户类
public class DJICustomer extends Customer {
    @Override
    void mailUpdate(String msg) {   //客户收到大疆有货的通知
        System.out.println(msg);
    }
}
//大疆供应商
public class DJIProvider extends Provider {
    public void hasProducts() { //供应商有货类就通知预定了产品的客户
        this.remind("DJI 有货了");
    }
}

public class ObserverTest {
    @Test
    public void obsTest() {
        DJIProvider provider = new DJIProvider();
        Customer lin = new DJICustomer();
        provider.order(lin);        //lin 订阅通知，即如果大疆有货就通知 lin。
        provider.hasProducts();//DJI 有货了
    }
}
```
观察者模式就是这么简单。当然这是属于“推”类型的，还有“拉”类型的，换汤不换药，只是通知的方法中传递类型改成 Provider ，这样让 Customer 自己来拉取需要什么数据。  
Java 的 java.util 库里面，提供了一个 Observable 类以及一个 Observer 接口，构成了 Java 对观察者模式的支持。  
观察者模式的有缺点：  
优点： 1、观察者和被观察者是抽象耦合的。 2、建立一套触发机制。  
缺点： 1、如果一个被观察者对象有很多的直接和间接的观察者的话，将所有的观察者都通知到会花费很多时间。 2、如果在观察者和观察目标之间有循环依赖的话，观察目标会触发它们之间进行循环调用，可能导致系统崩溃。 3、观察者模式没有相应的机制让观察者知道所观察的目标对象是怎么发生变化的，而仅仅只是知道观察目标发生了变化。