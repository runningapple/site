---
Title: JAVA 拾遗之数组篇
Date: 2017-09-02 18:25:42
Modified: 2017-09-02 18:25:42
Comments: false
Category: R&D
Tags: R&D,Java,技术,研发
Slug: java-array
Author: 苍南竹竿君
---
## 数组
数组是一种数据结构，用来存储同一类型值的集合。通过一个整型下标可以访问数组中的每一个值。  

## 数组初始化  
在 Java 中，数组在创建时会默认初始化值。数值型数组，所有元素都会初始化为 0 。boolean 数组初始化为 false 。对象数组初始化为 null 。<!--more-->  
```java
//整型数组初始化值为 0
int[] iArray = new int[2];
System.out.println(Arrays.toString(iArray)); //输出：[0, 0]

//boolean 数组初始化为 false
boolean[] bArray = new boolean[2];
System.out.println(Arrays.toString(bArray));//输出：[false, false]

String[] sArray = new String[2];
System.out.println(Arrays.toString(sArray));//输出：[null, null]

//创建数组的时候直接赋值
int[] iArrayb = {1, 2};
System.out.println(Arrays.toString(iArrayb));//输出：[1, 2]

//Java 中，数组长度可以为 0 。
int[] iArrayc = new int[0];
System.out.println(Arrays.toString(iArrayc));//输出：[]

//匿名数组
System.out.println(Arrays.toString(new boolean[]{true, false}));//输出：[true, false]
```
在 Java 中，数组长度可以为0 ，这里的 0 与 null 是不同的。数组长度可以为 0 ，在开发中十分有用，比如用写了一个返回数组结构的方法时，如果返回结果为空，比如查数据库没有查到对应条件的数据，就必须要返回一个空数组而不是一个 null 对象。  

## 数组遍历
Java 数组遍历有两种方式，一种是普通的下标遍历。第二种是 for each 循环遍历。这两种方式没有更好之分，需要根据场景来决定使用哪种方式。比如在需要逆序查找元素，或者指定下标查找元素的时候用下标遍历更方便。再比如只是要单纯的遍历所有元素，那么for each 遍历会更简洁方便，也不会有数组越界的风险。（for each 实现方式需要研究下）  
```java
int[] iArray = {1, 23, 6, 2, 3};

//用下标遍历数组
for (int i = 0; i < iArray.length; i++) {
    System.out.print(iArray[i] + ",");
}
//输出：1,23,6,2,3,

//用 for each 方式遍历数组
for (int item : iArray) {
    System.out.print(item + ",");
}
//输出：1,23,6,2,3,
```

## 数组复制
数组是存储在 Java 堆上的对象。每个变量指向的是对象的地址。所以想要复制数组的值不能使用 a = b 这种形式。  
```java
int[] aArray = {1, 2};
int[] bArray = {3, 4, 5};
aArray = bArray;                            //这里的赋值操作只是让 aArray 变量指向了 bRrray 对象的地址。
bArray[1] = 1;
System.out.println(Arrays.toString(aArray));//[3, 1, 5]
System.out.println(Arrays.toString(bArray));//[3, 1, 5]


//下面是两种数组的值复制方法
int[] cArray = {1, 2};
int[] dArray = {3, 4, 5};
cArray = Arrays.copyOf(dArray, dArray.length);
dArray[0] = 0;
System.out.println(Arrays.toString(cArray));//[3, 4, 5]

int[] eArray = {1, 2};
int[] fArray = {3, 4, 5};
System.arraycopy(fArray, 1, eArray, 0, 2);
System.out.println(Arrays.toString(eArray));//[4, 5]
```

## 多维数组
在 Java 中，其实没有真正的多维数组，只有一维数组，多维数组可以理解为数组中的数组。比如一个二维数组 A[2][2] 其实就是数组 A[0] 和 A[1] 里又分别存放了一个长度为 2 的一维数组。  
```java
int[][] aArrays = {{1, 2}, {3, 4}};
System.out.println(Arrays.deepToString(aArrays));//[[1, 2], [3, 4]]

int[][] bArrays = new int[2][2];
System.out.println(Arrays.deepToString(bArrays));//[[0, 0], [0, 0]]

int[][] cArrays = new int[2][];//不规则数组
cArrays[0] = new int[1];
cArrays[1] = new int[2];
System.out.println(Arrays.deepToString(cArrays));//[[0], [0, 0]]

//二维数组遍历
for (int i = 0; i < cArrays.length; i++) {
    for (int j = 0; j < cArrays[i].length; j++) {
        System.out.print(cArrays[i][j] + ",");
    }
    System.out.println();
}
/*
0,
0,0,
*/

for (int[] items : cArrays) {
    for (int item : items) {
        System.out.print(item + ",");
    }
    System.out.println();
}
/*
0,
0,0,
*/
```
## 命令行参数
每个 Java 应用程序都有一个 String[] args 参数。（~~~早期版本的 Java 需要通过这个参数来实现数据的输入，所以需要这个参数，但是现在可以用 Scanner 来输入数据。所以这个参数也就没有用了~~~）  
```java
public class MainArgsTest {

    public static void main(String[] args) {
        System.out.println("args : " + Arrays.deepToString(args));

        /*
        E:\PrivateWorkSpace\java_battle\src\test\java>java MainArgsTest -h a a
        args : [-h, a, a]
        */
    }

}
```

## 其它
在 Java 中，与数组类似的数据结构还有 List 。在功能较简单，长度确定的情况下，使用数组的效率会更高。至于 List 使用场景后续总结。