---
title: 从中国式婚姻到责任链模式
date: 2018-01-31 10:09:43
comments: true
categories: R&D
tags: [研发,设计模式,技术]
---
![](http://wx2.sinaimg.cn/mw690/ad108d28ly1fnzktra1e7j20gy0bhq6e.jpg)  
### *前言*
不知是人老了，还是受环境浸染的原因，开始不自主的思考起婚姻这种人生中的大题了。想到未来要接受双方父母的考验，心里就开始慌张（紧张是不会紧张的，一个什么都不缺的 single man 有什么好紧张的呢）。  
当然今天不来吐槽中国式的婚姻，而是要来总结一种设计模式------责任链模式，这种模式应用起来和中国式婚姻有着异曲同工之妙。  
所谓的责任链模式，就是为请求创建了一个接收者对象的链。请求并不知道具体执行请求的对象是哪一个，这样就实现了请求与处理对象之间都解耦。  
一如中国式婚姻，男女双方都是一个请求，处理对象就是双方的父母，过了父亲这关，还要过母亲这关，而后过岳父那关，最后过岳母这关。这四关连在一起就是一条链，因为男女双方都要过这四关，所以最终这条链就形成了闭环。<!--more-->  
### *作用*
避免请求发送者与接收者耦合在一起，让多个对象都有可能接收请求，将这些对象连接成一条链，并且沿着这条链传递请求，直到有对象处理它为止。  
换句话说就是如果男女双方父母聚到一起，一起来评断对方的孩子，估计双方的爸爸没什么话语权，另外双方父母都应该会认为自己孩子很优秀，balabala。这就是耦合在一起的缺点，所以我们就需要把四位分隔开，然后各个击破。这就是责任链的作用。  

### *应用示例*
1. tomcat 对 Encoding 的处理。
2. Struts2 的拦截器。
3. JS 中的冒泡事件。
4. jsp servlet 的 Filter。  

### *优点*
1. 对请求者和处理者的关系解耦，提高代码的灵活性。
2. 方便添加新的处理者。
3. 方便改变链内处理者的先后顺序，和动态添加或者删除处理者。  
  
### *缺点*  
1. 如果是递归调用，所以如果处理者多的场景下，势必会影响性能。 
2. 处理者多的时候，容易产生比较多的处理者对象。
3. 不一定能被处理。每个处理者只负责自己处理的那部分，因此可能会出现某个请求过来，如果没有默认的处理者的话，把责任链都遍历完，还是没有对应的处理者来处理该请求。就像中国式婚姻的例子，你要是一对同性恋作为请求过来，双方父母作为请求的处理者，根本没有这方面的处理方法，那这两位请求者在这个模式下就只能自生自灭了XD。  

### *实现*
这里我们就用责任链模式实现一个典型的中国式婚姻家长审核链。  
1. 首先我们先定义一个 Person 类，用来描述婚姻前的男孩和女孩。  
```java
/**
 * Created by lin on 2018/1/30.
 */
public class Person {

    private String name;          //姓名
    
    private int age;              //年龄
    
    private int faceValue;        //颜值 1:低, 2:中, 3:高
    
    private double salary;        //薪水
    
    private boolean haveHouse;    //是否有房
    
    private boolean haveCar;      //是否有车
    
    private String loveOrLike;    //是喜欢还是爱
    
    private String result = "";   //经历四个审核之后的结果
    /******  下面的 getter/setter 方法略  ******/
}
```

2. 抽象处理者对象（即描述婚姻里一般父母会做对事儿，就是对男女双方的挑挑拣拣咯），这里就定义一个 Filter 接口，提供一个 doFilter 方法，后续的处理者对象只要实现这个接口就是符合我们的婚姻背景。（即我们详细定义家长会挑拣哪些条件，毕竟不同父母，期望的东西是不一样的。）  
```java
/**
 * Created by lin on 2018/1/30.
 */
public interface Filter {

    void doFilter(Person boy, Person girl, FilterChain chain);

}
```

3. 构造审核链数据结构，审核链之所以也实现 Filter 接口，是为了如果当前有两条审核链了，想要把这两条审核链合成一条，那么就实现同一接口，就可以实现这一需求了。（就像当前只是双方父母来审核，但是突然你的七大姑，八大姨也想来凑热闹，搞了条审核链，那么我们就需要把这些吃饱了撑着的人也合进去吧，不然他们玻璃心会碎的：）
```java
public class FilterChain implements Filter {

    private List<Filter> filters = new ArrayList<Filter>(); //用列表来存放处理者，可以理解为放双方父母

    private int index = 0;                                  //添加一个标记，用来记录当前是谁在审核。
    /**
     * 添加审核者的方法
     * @param filter
     * @return
     */
    public FilterChain addFilter(Filter filter) {
        this.filters.add(filter);
        return this;
    }

    /**
     * 遍历审核链，对男孩，女孩进行审核
     * @param boy
     * @param girl
     * @param chain
     */
    public void doFilter(Person boy, Person girl, FilterChain chain) {
        if (index == filters.size()) return;
        Filter f = filters.get(index);
        index++;
        f.doFilter(boy, girl, chain);
    }
}
```

4. 实现双方父母的审核要求。（就是具体要挑拣什么东东，描述出来）  
```java
/**
 * Created by lin on 2018/1/30.
 */
public class FatherFilter implements Filter {

    public void doFilter(Person boy, Person girl, FilterChain chain) {
        //filter girl 男方父亲审核女孩
        if (girl.getLoveOrLike().equals("love")) {
            girl.setResult(girl.getResult() + " 公公同意");
            chain.doFilter(boy, girl, chain);       //如果公公同意，那么就继续给婆婆审核
        } else {
            girl.setResult(girl.getResult() + " 公公不同意");
            return;
        }
        /** 自己的父母可以审核自己的孩子，也可以不审核，这里我就不审核了 **/
        //filter boy
//        if (boy.getLoveOrLike().equals("love")) {
//            boy.setResult(boy.getResult() + " 父亲同意");
//        } else {
//            boy.setResult(boy.getResult() + " 父亲不同意");
//            return;
//        }
    }
}

public class MotherFilter implements Filter {

    public void doFilter(Person boy, Person girl, FilterChain chain) {
        //filter girl  男方母亲审核女孩
        if (girl.getFaceValue() >= 2 && girl.getAge() - boy.getAge() < 3) {
            girl.setResult(girl.getResult() + " 婆婆同意");
            chain.doFilter(boy, girl, chain);       //如果婆婆同意，那么接下去，轮到女方父母来审核男孩。
        } else {
            girl.setResult(girl.getResult() + " 婆婆不同意");
            return;
        }
    }
}

public class FatherInLawFilter implements Filter {

    public void doFilter(Person boy, Person girl, FilterChain chain) {
        //filter boy 女方父亲审核男孩
        if (boy.getLoveOrLike().equals("love")) {
            boy.setResult(boy.getResult() + " 岳父同意");
            chain.doFilter(boy, girl, chain);       //如果岳父同意，那么继续让岳母审核男孩。
        } else {
            boy.setResult(boy.getResult() + " 岳父不同意");
            return;
        }
    }
}

public class MotherInLawFilter implements Filter {

    public void doFilter(Person boy, Person girl, FilterChain chain) {
        //filter boy
        if (boy.getFaceValue() >= 2 && girl.getAge() - boy.getAge() < 3 && boy.getSalary() > 4000
                && boy.isHaveHouse()) {
            boy.setResult(boy.getResult() + " 岳母同意");
            chain.doFilter(boy, girl, chain);       //如果岳母同意，那么这条审核链就算结束了。
        } else {
            boy.setResult(boy.getResult() + " 岳母不同意");
            return;
        }
    }
}
```

5. 开始审核操作
```java
public class ChainOfResponsibilityTest {

    @Test
    public void testChainOfResponsibility() {
        Person boy = new Person();
        //这个男孩没房，没车，颜值一般，薪水低。。。
        boy.setName("Tom");
        boy.setAge(25);
        boy.setFaceValue(2);
        boy.setHaveCar(false);
        boy.setHaveHouse(false);
        boy.setLoveOrLike("love");
        boy.setSalary(5000);

        Person girl = new Person();
        //这个女孩也就一普通女孩
        girl.setName("Lily");
        girl.setAge(24);
        girl.setFaceValue(2);
        girl.setHaveCar(false);
        girl.setHaveHouse(false);
        girl.setLoveOrLike("love");
        girl.setSalary(4000);

        FilterChain filterChain = new FilterChain();
        filterChain.addFilter(new FatherFilter())
                .addFilter(new MotherFilter())
                .addFilter(new MotherInLawFilter())
                .addFilter(new FatherInLawFilter());
        filterChain.doFilter(boy, girl, filterChain);

        System.out.println(girl.getName() + " : " + girl.getResult());
        //输出：Lily :  公公同意 婆婆同意
        System.out.println(boy.getName() + " : " + boy.getResult());
        //输出：Tom :  岳母不同意
    }
}
```  
经过双方父母的审核，结果还是很悲观的。所以，当感情被量化之后，婚姻也就简单多了，不是吗？
