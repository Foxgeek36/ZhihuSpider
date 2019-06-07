# ZhihuSpider
知乎爬虫，用于爬取知乎上的内容，并且将爬取的内容解析为markdown保存到本地硬盘。

## 支持的内容
目前支持的内容包括：
- 特定问题下的所有回答
- 特定用户的所有回答、文章
- 专栏
- 话题精华
- 收藏夹
- 单个回答
- 单篇文章

## 爬虫工作方式
利用知乎api获得相应的内容，其中回答、文章的的主体内容是以html标签的形式包含在api返回的内容中。提取主体内容，将这部分内容解析转换成markdown文件保存到本地

## 示例：

下面这篇文章是本人发表在知乎的一篇关于循环冗余校验的文章，这里用来做示例。点击文章标题可以阅读在知乎上的原文，点击用户头像可以去到作者的知乎主页。对于回答还会在创作日期右方加上点赞数量，如：

![小鬼](https://pic2.zhimg.com/v2-8526bf36fd355e67836415fdd6458bfc_l.jpg "小鬼")&emsp;**[小鬼](https://www.zhihu.com/people/xiao-gui-55-68) / 2019-04-23** 👍 885

下面是一篇文章的示例：

# [循环冗余校验（CRC）](https://zhuanlan.zhihu.com/p/63409763)

--------------------------------------------------------

![小鬼](https://pic2.zhimg.com/v2-8526bf36fd355e67836415fdd6458bfc_l.jpg "小鬼")&emsp;**[小鬼](https://www.zhihu.com/people/xiao-gui-55-68) / 2019-04-23**

## 循环冗余校验（CRC）

- 加减法：$0 \pm 0 = 0, 0 \pm 1 = 0, 0 \pm 1 = 1, 1 \pm 1 = 0$
- 乘法：按模2加求部分积之和
- 除法：按模2减求部分余数


## 编码规则

1将待编码的$k$位二进制信息位$C_{k-1}C_{k-2}C_{k-3} \cdots C_1C_0$当成是$x$进制(二进制)的数字，将这个数字展开成$x$的多项式，即：


1为了在信息位后拼接$r$位校验位，需要将信息位向左移动$r$位，相当于在信息位后添加$r$个$0$，得到多项式$M(x) \cdot x^r$。
2用多项式$M(x) \cdot x^r$除以生成多项式$G(x)$所得余数$R(x)$作为校验码（按模 2 运算），即：


1将$R(x)$拼接（加）在信息位左移空出的$r$位上，就构成这个有效信息的 CRC 码，其多项式表示形式为$M(x) \cdot x^r + R(x)$(模2加)。
2这个 CRC 码$M(x) \cdot x^r + R(x)$可被生成多项式$G(x)$整除（模2除）。


因此，将收到的 CRC 码除以约定的生成多项式$G(x)$，如果码字没有错误，那么余数$R(x) = 0$，不同位出错，余数不同，可以根据余数的值定位错误码。

