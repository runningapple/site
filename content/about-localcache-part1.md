---
title: 如何设计一个local cache
date: 2018-08-12 16:49:57
Modified:  2018-08-12 16:49:57
comments: true
category:  R&D
tags: R&D,Java,技术,研发
Slug: about-localcache-part1
Author: 苍南竹竿君
---
### 开篇
这一个月上手了几个项目，这些项目有部分框架及工具使用是一样的。今天要说的就是项目中都有用到的技术 local cache（本地缓存）。  
如果了解 NoSQL，一定知道有一些数据（集群环境下）如果是要高频访问的，那么就可以放在 Redis，Memcache 等缓存中，这样可以减少对数据库的直接访问。但是在一些（比较简单的）业务场景下，我们并不需要搭建一套复杂的缓存系统。比如（单应用下）我们只想要存储一些类似于淘宝商品菜单名和菜单 code 的映射数据，这种场景下使用本地缓存更加贴合场景。<!--more-->  

### 设计一个简单的LRU local cache
#### 目标：
设计一个支持 LRU（最近最少未使用）的本地缓存，这里不考虑多线程情况，如果要考虑直接加锁或者使用 ConcurrentHashMap 最为缓存的存储容器。  

#### 分析：
1. local cache 必须支持 get(key), put(key, value) 功能。
2. local cache 对 get 和 put 的复杂度最好是O(1)，不然就失去了缓存的意义了。
3. local cache 具有容量上限，达到上限后再插入数据会先删除最近最少未使用的数据。  

#### 思路：
要存储 key-value 形式的数据，Map 容器跑不了。有了存储容器后，就要考虑如何标记 LRU（最近最少未使用）的数据了。这里我想到的第一个实现方案是 优先队列，把使用次数作为权重，把数据彤彤塞到优先队列中，但是这种方案虽然可行，只是复杂度一下就上升到了O(nlogn)，这是很糟糕的。所以就想到了第二个方案，使用 双端队列 来记录数据的使用情况，没使用的排在头部，使用过的塞到队尾，而且把数据从队列中拿出来塞到队尾的时间复杂度也是O(1)，正好符合要求。  

#### 实现：  
```java
/**
 * @author lin
 * @date 2018/8/12 下午2:41
 * @description:
 */
public class LRUCache {
    private int size;
    private Node head;//模拟双端队列头
    private Node rear;//模拟双端队列尾
    private Map<Integer, Node> cache;//缓存容器

    public LRUCache(int capacity) {
        this.size = capacity;
        head = new Node(null, null);
        rear = new Node(null, null);
        head.next = rear;
        rear.pre = head;
        cache = new HashMap<Integer, Node>(capacity);
    }

    public int get(int key) {
        Node node = cache.get(key);
        if (node != null) {
            //当前结点被使用了，所以必须从队列中移出这个结点，塞到队尾
            node.pre.next = node.next;
            node.next.pre = node.pre;
            appendRear(node);
            return node.val;
        }
        return -1;
    }

    public void put(int key, int value) {
        Node node = cache.get(key);
        //如果当前的key已经在容器中存储了，则直接覆盖
        if (node != null) {
            node.val = value;
            cache.put(key, node);
            node.pre.next = node.next;
            node.next.pre = node.pre;
            appendRear(node);
            return;
        }
        //如果容器已经达到存储上限了，则进行 LRU 删除操作
        if (size == cache.size()) {
            cache.remove(head.next.key);
            //tmp 用来释放被删除节点的内存
            Node tmp = new Node(null, null);
            tmp.next = head.next;
            head.next = head.next.next;
            head.next.pre = head;
            //这里最好还是把删除的结点的引用全部置为 null，不然容易出现该结点的内存无法回收的情况
            tmp.next.next = null;
            tmp.next.pre = null;
            tmp.next = tmp.pre = null;
        }
        node = new Node(key, value);
        appendRear(node);
        cache.put(key, node);
    }

    /**
    * 把结点塞到队尾
    */
    private void appendRear(Node node) {
        node.next = rear;
        node.pre = rear.pre;
        rear.pre.next = node;
        rear.pre = node;
    }

    //双端队列自己实现
    class Node {
        Node pre;
        Node next;
        int key;
        int val;

        public Node(int key, int val) {
            this.key = key;
            this.val = val;
        }

        public Node(Node pre, Node next) {
            this.pre = pre;
            this.next = next;
        }
    }

    public static void main(String[] args) {
        LRUCache cache = new LRUCache(1);
        cache.put(2, 1);
        System.out.println(cache.get(2));
        cache.put(3, 2);
        System.out.println(cache.get(2));
    }
}
```

### 总结
因为 local cache 是和应用在同一个进程内部，所以请求缓存的速度会比请求 redis 等要快，毕竟省了网络开销。但是因为 local cache 和应用程序耦合在一起，在多应用场景下是无法直接共享的，再加之每个应用都要独立的存储一份相同的数据，对内存也是一种浪费。