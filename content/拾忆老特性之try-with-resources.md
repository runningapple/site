---
title: 拾忆老特性之try-with-resources
date: 2018-06-13 21:25:14
Modified:  2018-06-13 21:25:14
comments: true
category:  R&D
tags: 研发,Java,技术,GAN计划
Slug: 拾忆老特性之try-with-resources
Author: 苍南竹竿君
---
现在 Java 10 都出来了，而还有好多公司都在用着 Java 7 或者 Java 6。说实话就算是 Java 7 ，想必也有很多有用的新特性都没有被用到实际开发中，大部分都是延续着 Java 6 的写法。  
比如今天要说（翻译）的 try-with-resources 语句。之前一直都是用 try-catch-finally，前段时间看了一篇讲异常的文章，正好提到了 try-with-resources 就记在了心上，今天来翻译一下 oracle 官网对 try-with-resources 的介绍。  
以下是正文：  
try-with-resources 是一种声明了一个或者多个资源的 try 语句。资源是一种程序结束后必须要关闭的对象。try-with-resources 语句确保每一个资源都能在语句结束后被关闭。任何实现了 java.lang.AutoCloseable,或者实现了 java.io.Closeable 接口的对象都能被作为资源。<!--more-->  

如下是读取文件对第一行的例子。例子中用对是 BufferddReader 实例从文件中读取数据。BufferedReader 是一个必须要在程序执行完后必须关闭对资源。  
```java
static String readFirstLineFromFile(String path) throws IOException {
    try (BufferedReader br = new BufferedReader(new FileReader(path))) {
        return br.readLine();
    }
}
```
在这个例子中，被声明在 try-with-resources 语句里对资源是 BufferedReader.声明语句紧跟在 try 关键字后面对小括号里。BufferedReader 在 Java SE 7 以及之后对版本中都实现了 java.lang.AutoCloseable 接口。因为因为 BufferedReader 实例被声明在了 try-with-resources 语句里，所以无论 try 语句是否正常执行（比如 readLine 突然抛出了一个 IOException 异常）资源都能正常关闭。  

在 Java SE 7 之前对版本，无乱 try 语句是否正常执行，你都可以使用 finally 块来确保资源关闭。下面就是使用 finally 块来替代 try-with-resources 语句对实现方式：  
```java
static String readFirstLineFromFileWithFinallyBlock(String path) throws IOException{
    BufferedReader br = new BufferedReader(new FileReader(path));
    try {
        return br.readLine();
    } finally {
        if (br != null) br.close();
    }
}
```
但是在这个例子中，如果 readLine 和 close 方法抛出了异常，那么 readFirstLineFromFileWithFinallyBlock 方法会抛出 finally 块中都异常。 try 语句块中的异常被压制了。相反，在 readFirstLineFromFile 例子中，如果 try 语句块和 try-with-resources 声明中都抛出了异常，那么 readFirstLineFromFile 方法最终将会抛出 try 语句块中的异常，try-with-resources 中都异常被压制了。在 Java SE7 之后的版本，你可以找回被压制的异常。  

你可以在 try-with-resources 里声明多个资源。下面这个例子是一个从名为 zipFileName 的 zip 文件中检索出所有文件名然后创建一个文本文件存储这些文件名。  
```java
public static void writeToFileZipFileContents(String zipFileName,
                                           String outputFileName)
                                           throws java.io.IOException {

    java.nio.charset.Charset charset =
         java.nio.charset.StandardCharsets.US_ASCII;
    java.nio.file.Path outputFilePath =
         java.nio.file.Paths.get(outputFileName);

    // Open zip file and create output file with 
    // try-with-resources statement

    try (
        java.util.zip.ZipFile zf =
             new java.util.zip.ZipFile(zipFileName);
        java.io.BufferedWriter writer = 
            java.nio.file.Files.newBufferedWriter(outputFilePath, charset)
    ) {
        // Enumerate each entry
        for (java.util.Enumeration entries =
                                zf.entries(); entries.hasMoreElements();) {
            // Get the entry name and write it to the output file
            String newLine = System.getProperty("line.separator");
            String zipEntryName =
                 ((java.util.zip.ZipEntry)entries.nextElement()).getName() +
                 newLine;
            writer.write(zipEntryName, 0, zipEntryName.length());
        }
    }
}
```
在这个例子中，try-with-resources 声明了两个资源（ZipFile，BufferedWriter），并用分号隔开。当代码快终止，不论是正常结束还是因为异常结束，BufferedWriter 和 ZipFile 对象的 close 方法都会按照资源声明创建的相反顺序调用。  

下面是一个使用 try-with-resources 声明自动关闭 java.sql.Statement 对象的例子：  
```java
public static void viewTable(Connection con) throws SQLException {

    String query = "select COF_NAME, SUP_ID, PRICE, SALES, TOTAL from COFFEES";

    try (Statement stmt = con.createStatement()) {
        ResultSet rs = stmt.executeQuery(query);

        while (rs.next()) {
            String coffeeName = rs.getString("COF_NAME");
            int supplierID = rs.getInt("SUP_ID");
            float price = rs.getFloat("PRICE");
            int sales = rs.getInt("SALES");
            int total = rs.getInt("TOTAL");

            System.out.println(coffeeName + ", " + supplierID + ", " + 
                               price + ", " + sales + ", " + total);
        }
    } catch (SQLException e) {
        JDBCTutorialUtilities.printSQLException(e);
    }
}
```
在例子中使用的 java.sql.Statement 是 JDBC 4.1 及之后版本的 API。  
注意：try-with-resources 语句也可以有 catch 和 finally 块，就像 try 语句一样。在 try-with-resources 语句中，任何 catch 或者 finally 块都会在被声明的资源关闭后执行。  

异常压制  
一个异常可能被 try-with-resources 语句相关的代码块抛出。在 writeToFileZipFileContents 例子中，一个异常可能被 try 代码块抛出，同时当试图关闭 ZipFile 和 BufferedWriter 对象时， try-with-resources 语句可能抛出两个异常。如果一个异常被 try 代码块抛出同时一个活着多个异常被 try-with-resources 语句抛出，那么 try-with-resources 语句中的异常将会被压制，并且最终在 writeToFileZipFileContents 方法中抛出的异常就是 try 代码块中抛出的那个异常。你可以通过 Throwable.getSuppressed 方法找回被压制的异常。  

看 Javadoc 中关于 AutoCloseable 和 Closeable 接口，列举类一些实现类。Closeable 接口继承类 AutoCloseable 接口。Closeable 接口的 close 方法抛出了 IOException 异常，而 AutoCloseable 接口的 close 方法抛出了 Exception 异常。所以 AutoCloseable 接口的子类可以重写父类的 colse 方法抛出更详细的异常，例如 IOException，或者不抛出异常。  


原文：https://docs.oracle.com/javase/tutorial/essential/exceptions/tryResourceClose.html