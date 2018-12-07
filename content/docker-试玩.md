---
title: docker 试玩
date: 2018-02-20 15:45:31
Modified:  2018-02-20 15:45:31
comments: true
category:  R&D
tags: 研发,技术
Slug: docker-试玩
Author: 苍南竹竿君
---
![](http://wx4.sinaimg.cn/mw690/ad108d28gy1fomxv6myrmj20hr099q31.jpg)  
最近放假在家里没事做，在自己电脑上试玩了下 docker。如果用一个字来概括试玩的感受，那就是“爽”。  
要知道先前因为嫌装各种诸如 mysql，tomcat 之类的开发软件太麻烦，就一直没有在自己电脑上安装。自从用了 docker，可以把这些乱七八糟的东西通通都仍到 docker 里去。用的时候启动一下，不用的时候，直接删掉就好了。而且还是存粹的 linux 环境，命令行定位配置，加上 volume 数据卷进行文件共享（通过数据卷可以对数据进行持久化操作）。所以用着用着都觉得下版本的 mac os 或者 windows 系统应该预装 docker 了。<!--more-->  
那接下来演示 docker 安装 mysql，并用 Spring jdbctemplate 读写表。  
1. 首先我们需要安装 docker，如果是 windows7 系统，那就先升到 windows10 吧，不然出现各种乱七八糟到问题。如果是 mac os 最好了，我们直接在官网下载安装就可以了。  
![](http://wx3.sinaimg.cn/mw690/ad108d28gy1fomxv62xn8j20o006udgd.jpg)  
不要被网上一些旧的博客误导了，现在安装 docker 不需要像以前那样要安装 toolbox 了。  
安装好后打开命令行，输入如下命令，能得到正确回显就说明已经安装正确了。
```shell
lin-desk:~ lin$ docker --version
Docker version 17.12.0-ce, build c97c6d6
lin-desk:~ lin$ docker-compose --version
docker-compose version 1.18.0, build 8dd22a9
lin-desk:~ lin$ docker-machine --version
docker-machine version 0.13.0, build 9ba6da9
```
2. 接下来我们就要安装mysql了。
首先我们先把 mysql 镜像 pull 下来。
```shell
lin-desk:~ lin$ docker pull mysql:5.6
5.6: Pulling from library/mysql
4176fe04cefe: Downloading [=====>                                             ]  5.394MB/52.61MB
d1e86691d483: Download complete 
ffadeffb3eb4: Download complete 
6c2c640eac6b: Download complete 
cc4146cb804c: Downloading [=========>                                         ]  1.631MB/8.461MB
7de5ccbd771a: Download complete 
775e0cecdad2: Download complete 
88d4255f1a7b: Downloading [>                                                  ]  431.7kB/42.67MB
d1b4737edd2f: Waiting 
9d87f540bc85: Waiting 
```
pull 好后，我们可以用命令行查看镜像信息。  
```shell
lin-desk:~ lin$ docker image ls mysql
REPOSITORY          TAG                 IMAGE ID            CREATED             SIZE
mysql               5.6                 f8418f2b6a58        5 weeks ago         299MB
```
现在已经安装好 mysql 镜像了，接下来要做到就是启动 mysql 实例。  
```shell
lin-desk:~ lin$ docker run -p 3306:3306 --name mysql -v /Users/lin/temp/data:/var/lib//mysql -v /Users/lin/temp/conf:/etc/mysql/conf.d -e MYSQL_ROOT_PASSWORD=123456 -d mysql:5.6
```
这个命令行解释一下：-p 3306:3306 的意思是将容器的 3306 端口映射到主机的 3306 端口。  
-v /Users/lin/temp/data:/var/lib//mysql 讲当前主机的temp/data目录挂载到容器的/var/lib/mysql目录。  
-e MYSQL_ROOT_PASSWORD=123456 初始化 root 用户密码。  
以上就已经把 mysql 启动了，我们可以进入 mysql 容器查看数据库信息。
![](http://upload-images.jianshu.io/upload_images/7896037-fa28a2ba33186079.gif?imageMogr2/auto-orient/strip)

3. 用 Spring jdbctemplate 读写表
![](http://upload-images.jianshu.io/upload_images/7896037-8f0269ed09cc8e95.gif?imageMogr2/auto-orient/strip)  

OK，以上就是 docker 容器配置运行 mysql 的过程了，很简单，当然 docker 能力不限于这么简单一点，还有隔离应用，整合服务器，快速部署等等其它应用场景，以后在演示。