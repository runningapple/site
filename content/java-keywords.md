---
title: JAVA 拾遗之关键字篇
date: 2017-09-02 2017-09-02 18:27:41
Modified:  2017-09-02 2017-09-02 18:27:41
comments: true
category:  R&D
tags: 技术,研发,Java
Slug: java-keywords
Author: 苍南竹竿君
---
## strictfp
strictfp，即strict float point（精确浮点）  
strictfp 关键字可以用于类，接口和方法。使用 strictfp 关键字声明一个方法时，该方法中的所有浮点数计算都要严格遵守 IEEE-754 规范。同理类和接口一样。加 strictfp 关键字可以防止不同的硬件平台上浮点数计算结果不一致。（但是我在 windows 和 linux 下都试过相同的代码都没有出现数据不一致的情况，估计和 Java 版本有关，这个关键字是 Java2 中加的，那么用 Java2 应该能够重现出来）。
```java
public strictfp void sfpTest() {
    float aFNum = 0.3f;
    float bFNum = 0.01f;
    System.out.println(aFNum-bFNum);//0.29000002
}

public void fTest() {
    float aFNum = 0.3f;
    float bFNum = 0.01f;
    System.out.println(aFNum-bFNum);//0.29000002
}
```
<!--more-->

## transient
transient 是用来在数据转换成字节流进行持久化的时候标记一些不需要持久化的属性，让其不转成字节流。我们都知道数据在网络中传输是以流形式（序列式）的，将数据转换成字节流在网络中传输，当字节流被接收后，这些字节流会重新创建出原来的数据（对象），这时候如果对象所对应的类属性中有被标记了 transient 关键字的，则该属性所对应的值不会被转换出来。transient 需和序列化接口 Serializable 配套使用。
```java
public void transientTest() {
    User user = new User();
    user.setUsername("runningapple");
    user.setPasswd("abc");

    System.out.println("username： " + user.getUsername());//username： runningapple
    System.out.println("password： " + user.getPasswd());//password： abc

    try {
        ObjectOutputStream os = new ObjectOutputStream(new FileOutputStream("E:/user.txt"));
        os.writeObject(user);
        os.flush();
        os.close();
    } catch (FileNotFoundException ex) {
        ex.printStackTrace();
    } catch (IOException ioe) {
        ioe.printStackTrace();
    }

    try {
        ObjectInputStream is = new ObjectInputStream(new FileInputStream("E:/user.txt"));
        user = (User) is.readObject();
        is.close();
        System.out.println("username: " + user.getUsername());//username: runningapple
        System.out.println("password: " + user.getPasswd());//password: null
    } catch (FileNotFoundException ex) {
        ex.printStackTrace();
    } catch (IOException ioe) {
        ioe.printStackTrace();
    } catch (ClassNotFoundException cne) {
        cne.printStackTrace();
    }

}

class User implements Serializable {

    private String username;
    private transient String passwd;

    public String getUsername() {
        return username;
    }

    public void setUsername(String username) {
        this.username = username;
    }

    public String getPasswd() {
        return passwd;
    }

    public void setPasswd(String passwd) {
        this.passwd = passwd;
    }
}
```
