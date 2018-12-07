---
title: JAVA 拾遗之 switch 与 String
date: 2017-09-06 21:43:13
Modified:  2017-09-06 21:43:13
comments: true
category:  R&D
tags: 技术,研发,Java
Slug: java-switch
Author: 苍南竹竿君
---
在 Java1.7 版本之前，switch case 能够用来比较 byte, short, int, char, enum（枚举类型是通过该常量在所有枚举常量中的序号进行比较的）。在 Java1.7 版本之后 switch case 增加了对 String 的比较能力。像 byte, short, char 等都是通过数值及转换成对应的数值进行比较的，那么 String 又是如何比较的呢？为了一探究竟，今个儿就看看编译后的代码是怎么样的。  

初始代码：<!--more-->
```java
public static void main(String[] args) {
    //int 数值比较
    int i = 1;
    switch (i) {
        case 1:
            System.out.println("1");
            break;
        case 2:
            System.out.println("2");
            break;
        default:
            break;
    }
    //char 字符比较
    char c = 'a';
    switch (c) {
        case 'a':
            System.out.println("a");
            break;
        case 'b':
            System.out.println("b");
            break;
        default:
            break;
    }
    //字符串比较
    String str = "hello";
    switch (str) {
        case "hello":
            System.out.println("hello");
            break;
        case "world":
            System.out.println("world?");
            break;
        default:
            break;
    }

    //枚举类型比较
    Color color = Color.BLACK;
    switch (color) {
        case BLUE:
            System.out.println("blue");
            break;
        case BLACK:
            System.out.println("black");
            break;
        default:
            break;
    }
}

enum Color {
    BLACK("黑色", 1), BLUE("蓝色", 2), RED("红色", 3);

    private String name;
    private int index;

    private Color(String name, int index) {
        this.name = name;
        this.index = index;
    }

    public static String getName(int index) {
        for (Color c : Color.values()) {
            if (c.getIndex() == index) {
                return c.name;
            }
        }
        return null;
    }

    public String getName() {
        return name;
    }

    public void setName(String name) {
        this.name = name;
    }

    public int getIndex() {
        return index;
    }

    public void setIndex(int index) {
        this.index = index;
    }
}
```

编译后的代码：
```java
public static void main(String[] paramArrayOfString)
  {
      //int 数值比较
    int i = 1;
    switch (i)
    {
    case 1: 
      System.out.println("1");
      break;
    case 2: 
      System.out.println("2");
      break;
    }
    //char 字符比较
    int j = 97;
    switch (j)
    {
    case 97: 
      System.out.println("a");
      break;
    case 98: 
      System.out.println("b");
      break;
    }

    //字符串比较
    String str = "hello";
    Object localObject = str;
    int k = -1;
    switch (((String)localObject).hashCode())
    {
    case 99162322: 
      if (((String)localObject).equals("hello")) {
        k = 0;
      }
      break;
    case 113318802: 
      if (((String)localObject).equals("world")) {
        k = 1;
      }
      break;
    }
    switch (k)
    {
    case 0: 
      System.out.println("hello");
      break;
    case 1: 
      System.out.println("world?");
      break;
    }
    
    //枚举类型比较，通过 ordinal 方法获取该常量在枚举中的序号进行比较
    localObject = Color.BLACK;
    switch (GenericMethodTest.1.$SwitchMap$Color[localObject.ordinal()])
    {
    case 1: 
      System.out.println("blue");
      break;
    case 2: 
      System.out.println("black");
      break;
    }
  }
```
可以看到编译后的代码比较字符串类型的时候，进行了两次 switch case。首先定义来一个 int 整形变量 i ，i 的初始值为 -1。然后获取字符串对象的 hashCode 。然后通过 hashCode 进行比较，但是考虑到 hashCode 会出现碰撞的情况，就再进行的一次 equal 判断，在符合条件的 case 下，重新赋值。第二次 switch case 就是根据变量 i 来进行判断的。  

所以虽然在 Java1.7 后可以 switch 字符串了，但是在底层实现上还是没有变的，还是对数值进行判断操作。  