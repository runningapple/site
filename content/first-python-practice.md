---
title: 一次 Python 脚本实践
date: 2017-08-06 23:14:06
comments: true
categories: R&D
tags: [Python,技术,脚本,Linux]
---

最近在学习 python 脚本，原先打算这个周末写篇文章汇总一下学习记录的。正好上周正好想到有个项目平时部署时候要分不同环境配置不同参数，很是麻烦且很容易出错。所以上周花了半天的时间撸了一个验证和替换参数的脚本，下面就来记录一下。<!--more-->  
* *实际需求*  
    有个发布包（war包），需要在生产环境解压部署，并且有两个生产环境 A 和 B。A 和 B 环境部署时候需要对几个配置文件中的参数进行替换，注释和取消注释。言简意赅的描述就是：文件解压--->文件内容读取检查替换

* *研究方案*  
    经过一番调查发现 Python 在解压 zip,tar,rar,tgz,gz 格式的压缩包上是没有什么问题的，但是在解压 war 包上就没有什么先例了。没有先例就不做？这不是我的风格，好嘛。接下来我想了两种方案：  
    * 将文件重命名为 Python 能够解压的格式或者在本地解压后重新打包成 Python 能够解压的格式。  
    * 既然 Python 不能解压，那干脆就不用 Python 解压了，我们用 Linux命令 unzip 来解压不就好了吗。不过这里我们用 Python 来执行 Linux 的解压命令。    

    解压的方案1显然过于麻烦，所以这里我选择了方案2。  
    解压好了那接下来的步骤就是读取文件，这里2个比较头疼的地方：  
    * Python 版本不同读取文件姿势也有很大出入，我PC装的是 Python3 ，然后测试环境装的是 Python2.6，生产环境装的是 Python2.4。这着实是个坑，在 PC 上写的脚本在测试环境执行不了，测试环境调整好后的脚本在生产环境又执行不了，最后只能在生产环境继续调整。  
    * 以什么编码方式打开文件  
    
    上一步文件已经将文件读取进来了，剩下的就是重头戏文件内容替换。因为这里读取的文件格式有 properties 和 xml 类型的，如果对每个文件类型单独写个方法实在太麻烦，干脆只写一个通用方法来对文件内容进行操作。考虑到 properties 内容是 key=value 形式的，而 xml 内容是树形的 DOM 。所以并没有什么共同点可以抓，只能将读取的内容以字符串形式来处理，当然这里我用正则表达式进行匹配替换，简单粗暴却又不失美感。  
    最后将替换后的字符串重新写入一个新的文件，一定不要在文件打开读取后没关闭又进行写入操作。  

  
* *具体实现*  
```python
#!/usr/bin/python
# -*- coding: UTF-8 -*-
import os
import codecs
import re

demoTarget = '<!--helloworld:service ([\s\S]*)</helloworld:service-->'#被替换的内容（正则表达式来匹配）

demoReplace = """result string"""                                     #替换后的内容

def replaceFileContent(fileName, targetContent, replaceContent):      #方法（文件名，替换目标的内容，替换后的内容）
    f = codecs.open(fileName, "r", "UTF-8")                           #以只读，UTF-8方式编码读取打开文件
    content = f.read()                                                #读取文件内容
    f.close()                                                         #文件读取后记得关闭
    os.remove(fileName)                                               #删除文件
    content = re.sub(targetContent, replaceContent, content, 1)       #替换文件内容
    # content =  content.replace(targetContent, replaceContent)
    tempFile = codecs.open(fileName, "wb", 'UTF-8')                   #已二进制,写入，UTF-8编码方式打开一个新的文件
    tempFile.write(content)                                           #写入替换后全部的内容到新打开的文件中
    tempFile.close()                                                  #关闭文件
    #过滤文件中的 ^M 字符，该字符其实是回车符,因为 UNIX 下一般只有一个0x0A表示换行，Windows 下一般都是 0x0D 和 0x0A 两个字符，所以 Linux 下会多出一个 0x0A 字符，看到的结果就是每行后面都有一个 ^M 字符。所以需要过滤一下。
    os.system('sed -i "s/\r//g" ' + fileName)                         
    # os.system('dos2unix '+fileName) 需要服务器支持该命令，这个命令可以将文件内容转成适合 UNIX 格式的文件内容。

def App1():
    print("开始解压...")
    os.system('unzip -q helloworld.war -d /Data/deploy/helloworld')   #执行 Shell 命令
    print("解压完成")
    print("开始部署...")
    router = "/Data/deploy/helloworld/WEB-INF/classes"

    global demoTarget
    global demoReplace
    replaceFileContent(router+"/spring/http-client-config.xml", demoTarget, demoReplace) #调用方法

App1()
```
