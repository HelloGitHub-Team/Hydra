# Hydra（九头蛇）

<p align="center">
  <img width="75%" src="https://cdn.jsdelivr.net/gh/HelloGitHub-Team/Hydra@main/doc/cover.png"/>
  <br><strong>简单绝不简陋的 Python3 爬虫项目。</strong>
  <br>参考<a href="https://mp.weixin.qq.com/s/K4RGr5NqMFAUKtB0KFPV5g">「建立完美的 Python 项目」</a> 创建 
</p>

Hydra 力求用最简单的代码实现功能，仅实现了爬虫最实用的部分：爬取->入库，爬的部分没有用任何框架。

从本项目中你可以看到：**熟悉的 [Python 基础语法](https://github.com/521xueweihan/python)**、**如何编写爬虫**、**操作数据库**、**常用第三库**、**分析网页**、**解析接口**、**编写单元测试**、**mock 请求**、**异常监控和管理**、**保证代码质量的自动化** 等实战应用。

此项目是汇集「HelloGitHub」在每个平台的账号和内容数据，方便我们的作者们看到自己作品的数据。支持平台：[博客园](https://www.cnblogs.com/xueweihan/)、[头条](https://www.toutiao.com/c/user/token/MS4wLjABAAAAigrrKo-3rjLpxaH4Go3BrZRqHTIhLW3e30QjfFXgzNQ/)、[知乎](https://www.zhihu.com/people/xueweihan)、[掘金](https://juejin.cn/user/1574156384091320)、[即刻](https://web.okjike.com/u/ff31a838-6eb9-440d-9970-dabc5b2c0309) 等。

你要[加入](https://mp.weixin.qq.com/s/9FUQ2i0HbemwfIj9sa1p0A)我们吗？

## 一、运行

> 基于 Python 3.9.1 实现，理论上支持 3.7.5+

首先，下载项目：`git clone` or [点击下载 zip 包](https://github.com/HelloGitHub-Team/Hydra/archive/main.zip)

然后，在项目根目录创建配置文件，[.local_env.yaml](/doc/local_env.yaml)。

最后，把玩起来吧！

1. 安装 poetry：`pip install poetry`
2. 安装依赖：在项目根目录执行 `poetry install --no-root`
3. 运行单个爬虫：`poetry run python main.py wechat|cnblogs|toutiao|csdn|zhihu|juejin|jike`

运行遇到问题和更多说明[点这里](/doc/install.md)，贡献代码[看这里](/doc/contribution.md)

## 二、效果



## 三、声明
<a rel="license" href="https://creativecommons.org/licenses/by-nc-nd/4.0/deed.zh"><img alt="知识共享许可协议" style="border-width: 0" src="https://licensebuttons.net/l/by-nc-nd/4.0/88x31.png"></a><br>本作品采用 <a rel="license" href="https://creativecommons.org/licenses/by-nc-nd/4.0/deed.zh">署名-非商业性使用-禁止演绎 4.0 国际</a> 进行许可。
