---
title: 关于HBase的一些小结
date: 2018-10-20 15:49:00
comments: true
categories: R&D
tags: [R&D,HBase,技术,研发]
---
吼，最近的工作内容一直在围绕着系统优化进行着，特别是HBase相关的。  
因为之前也没很深入的理解这块内容，只是在项目里用过一次。  
但是呢，这次我发现如果只是单纯的会用，而不知道为什么要这么用，不知道什么时候可以用什么方式的话，对于高并发系统来说一次错误的使用可能会造成不堪设想的后果。  
所以，还是抽点时间去了解了下 HBase 相关的原理，然后浅显的汇总一下。  

---
#### HBase简介
HBase 是一个高可靠性、高性能、面向列、可伸缩的分布式存储系统，利用 HBase 技术可以在廉价的 PC Server 上搭建起大规模的结构化存储集群。  
HBase 不同于一般的关系型数据库，它是一个非结构化数据存储的数据库，同时 HBase 是基于列而不是基于行的模式。  
在 HBase 表中，一个数据行可以拥有一个可选择的键和任意数量的列，一个或者多个列组成一个列族（ColumnFamily），一个 Family 下的列位于一个 HFile 中，易于缓存数据。  
HBase 中数据是按主键排序的，同时表按主键划分为多个 Region。  

#### 认识 HBase 框架
![](http://wx3.sinaimg.cn/mw690/ad108d28ly1fwfx19gzcyj20j909nmy2.jpg)  
* HDFS & API & Client  
    HBase 是利用 Hadoop HDFS 作为其文件系统的  
    HBase 上层提供了访问数据的 Java API，当然也提供了传统的交互式命令 API  
    Client 使用 HBase RPC 机制与 Master 和 RegionServer进行通信（使用Protobuf作为用户请求和内部数据交换的数据格式。每个RegionServer都会和Master服务器保持一个长连接。）  
    Client 与 Master 进行管理类操作  
    Client 与 RegionServer 进行数据读写类操作  
<!--more-->  
在 HBase 集群中主要由 Master、Region Server 和 Zookeeper 组成。  
* Region  
    真是存放数据的地方，是 HBase 可用性和分布式的基本单位。如果当一个表很大，并且由多个列族组成，那么表数据将存放在多个 Region 之间，并且在每个 Region 椎间盘买个叫关联多个存储单元。（每个Region对象包含多个Store对象，每个Store包含一个MemStore或若干StoreFile，StoreFile包含一个或者多个HFile，MemStore存放在内存中，StoreFile存储在HDFS上）
* RegionServer  
    负责管理表格和实现读写操作。Client 直接连接 RegionServer，并通信获取 HBase 中的数据。
* Master  
    协调多个 RegionServer  
    分配 Region 给 RegionServer
    可以存在多个 Master，但是只能有一个 Master 是提供服务的
* Zookeeper  
    HBase Master 的 HA 解决方案。保证至少有一个 Master 处于运行状态，负责 Region 和 RegionServer 的注册。

条条框框看起来很复杂，我们类比一下就十分好理解了：  
Region 相当于一个国家的省或者洲。（Store即省下面的市，MemStore可以理解为市中心，StoreFile就是市边上的一些区县镇）  
RegionServer 相当于洲长，省长，管理自己所负责的洲（Region）。  
Master 相当于总统，负责管理洲长，省长（RegionServer），以及分配哪些地方给洲长管理。一个国家只能有一个总统，但是在总统选举的时候，可以有好多候选人。  
Zookeeper 相当于人民代表，人民代表会选出哪个总统候选人作为一个国家的总统（Master）。  

#### HBase 数据模型
![](http://wx1.sinaimg.cn/mw690/ad108d28ly1fwfx15s56vj20ei02jdg7.jpg)  
* RowKey  
    RowKey为字节数组，RowKey用来表示表中唯一一行记录的主键，HBase 数据是按照 RowKey 的字典序排序的。
* ColumnsFamily  
    包含一个或者多个相关列，列名都以列族为前缀。如：info:height,info:sex 都属于 info 这个列族。
* Cell  
    由 {RowKey, columnFamily, version} 唯一确定的单元。Cell中的数据是没有类型的，全部都是以字节码形式存储。
* TimeStamp  
    HBase中通过 RowKey 和 columns 确定的唯一一个存储单元称之为 Cell。每个 Cell 都保存着同一份数据的多个版本。版本通过时间戳来索引。时间戳也可以由用户显示赋值。

#### ROOT表和META表
HBase的所有Region元数据被存储在META表中，随着Region的增多，META表中的数据也会增大，并分裂成多个新的Region。为了定位META表中各个Region位置，把META表中所有Region的元数据保存在ROOT表中，最后由ZK记录ROOT表的位置。ROOT是不会被分割的，永远只保存一个Region里。  
META表：存储了对应的Region地址和开始结束信息。  
ROOT表：存储了对应的META地址和开始结束信息。  
客户端访问数据前操作：zk获取ROOT的位置---》访问ROOT表获取META表的位置---》根据META表中的信息确定用户数据存放的位置。  
![](http://wx2.sinaimg.cn/mw690/ad108d28ly1fwfwiu36qfj20dl07ewfo.jpg)  

#### 可靠性
WAL（write-ahead-log）预写日志：  
先介绍一下为什么要引入HLog：在分布式环境中，无法避免系统出错或者宕机，一旦RegionServer意外退出，MemStore中的内存数据就会丢失，引入HLog就是为了这种情况出现的补救方法。  
HLog工作机制：  
每个RegionServer中都会有一个HLog对象，RegionServer会将更新操作（Put，Delete）先记录到WAL（HLog）中，然后将其写入到Store的MemStore，最终MemStore会将数据写入到持久化的HFile中。HLog文件会定期滚动出新，并且删除就的文件（已经持久化到HFile中的数据）。  
**当RegionServer意外终止后，Master会通过ZK感知，Master首先处理遗留的HLog文件，将不同region的log数据拆分，分别放到相应的目录下，然后再将失效的region重新分配，领取到这些region的RegionServer在Load Region的过程中，会发现有历史HLog需要处理，因此会Replay Hlog中的数据到MemStore中，然后flush到StoreFiles，完成数据恢复**  
<font color='red'>（Master通过ZK感知，这里是ZK去通知Master还是咋样，需要了解一下ZK）</font>  
其它：  
Master容错：如果一个Master无服务，zk可以重新选择一个新的Master。没有Master过错中，数据读取仍然正常（client是通过RegionServer进行读取操作的），但是Region的切分、负载均衡等无法进行。  
RegionServer容错：RegionServer定时发送心跳给Master，如果一段时间内没有心跳，Master将该RegionServer上的Region重新分配到其它RegionServer上，失效服务器上的HLog由主服务器进行分割并派送给新的RegionServer。  
ZK容错：ZK就不用多讲了，到处都有它的身影。  

#### 读写流程
![](http://wx1.sinaimg.cn/mw690/ad108d28ly1fwfwj0sd8pj20kc0cm449.jpg)  
HBase 读操作流程：  
1. client 访问 ZK，查找 ROOT 表，获取 META 表信息。
2. 从 META 表查找存放目标数据的Region信息，从而找到对应的RegionServer。
3. 通过RegionServer获取要查找的数据。
4. RegionServer的内存分为MemStore和BlockCache两部分，MemStore主要负责写数据，BlockCache负责读数据，读请求会先到MemStore中查询数据，查不到数据就到BlockCache中查找，再查不到就到StoreFile中读取，并把读取到的结果放入BlockCache。
![](http://wx2.sinaimg.cn/mw690/ad108d28ly1fwfwj4rhaqj20ce03bq2q.jpg)  

HBase 写操作流程：  
1. client 通过zk调度，向RegionServer发出写数据请求，在Region中写数据。
2. 数据被写入Region的MemStore，直到MemStore达到（内存大小？）预设的阈值。
3. MemStore 中的数据被Flush成一个StoreFile。
4. 随着StoreFile文件的不断增多，其数量增长到一定阈值后，触发Compact合并操作，将多个StoreFile合并成一个StoreFile，同事进行版本合并和数据删除。
5. StoreFiles通过不断的Compact合并操作，逐步形成越来越大的StoreFile。
5. 单个StoreFile大小超过一定阈值后，触发Split操作，把当前的Region split成2个新的Region。父Region下线，新产生的2个子Region会被HMaster分配到相应的RegionServer上，使得原先1个Region的压力得以分流到2个Region上。  

题外话：其实HBase的写操作有点和JVM中的young gc类似，flush成一个StoreFile就像gc中的删除不再使用的对象，而compact操作就像是将Eden区的存活的对象移动在S0或者S1。Split操作及分配Region到RegionServer就好比将年龄达到一定值的对象晋级到Old区。  
而HBase读操作有点类似Java中创建一个对象的过程，栈区--》堆区--》方法区。

***---内容大部分参考至网络***