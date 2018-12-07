---
title: 将csv数据导入到mysql
date: 2018-03-07 18:49:39
Modified:  2018-03-07 18:49:39
comments: false
category:  R&D
tags: R&D,技术,研发,奇技淫巧
Slug: 将csv数据导入到mysql
Author: 苍南竹竿君
---
之前用想用 Navicat 将 csv 的数据导入到 MYSQL 时候，发现有行数限制，上个星期改用了 DataGrip 工具来操作数据库，发现可以没有限制的导入数据了（很是 happy）。  
但是对于 datetime 类型的数据导入还是会有问题的，需要做点处理。下面就来演示一遍。<!--more-->  

1. 将表中的 Datetime 类型改成 varchar 类型。
```sql
ALTER TABLE package CHANGE scan_time scan_time VARCHAR(50);
```
2. 导入数据  
![](http://upload-images.jianshu.io/upload_images/7896037-b6e1a1910bc2ff4c.gif?imageMogr2/auto-orient/strip)
3. 修改日期字符串的格式 ‘YYYY-MM-DD hh:mm:ss’   
```sql
UPDATE package
SET package.scan_time = concat(
    substr(package.scan_time, 7, 4), '-',
    substr(package.scan_time, 4, 2), '-',
    substr(package.scan_time, 1, 2), ' ',
    substr(package.scan_time, 12));
```
4. 将 varchar 类型修改成 Datetime 类型。
 ```sql
ALTER TABLE package CHANGE scan_time scan_time DATETIME;
```
![](http://upload-images.jianshu.io/upload_images/7896037-a6a22bf880f3022b.gif?imageMogr2/auto-orient/strip)

另外好像也可以用命令行直接导入 csv 数据，我在 docker 环境里试了下，不顶用～。  
```sql
LOAD DATA INFILE "/home/paul/clientdata.csv"
INTO TABLE CSVImport
COLUMNS TERMINATED BY ','
OPTIONALLY ENCLOSED BY '"'
ESCAPED BY '"'
LINES TERMINATED BY '\n'
IGNORE 1 LINES;
```
