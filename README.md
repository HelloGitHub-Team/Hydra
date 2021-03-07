# Hydra（九头蛇）

<p align="center">
  <img width="75%" src="https://cdn.jsdelivr.net/gh/HelloGitHub-Team/Hydra@main/doc/cover.png"/>
  <br><img alt="GitHub Workflow Status" src="https://img.shields.io/github/workflow/status/HelloGitHub-Team/Hydra/hydra?style=flat-square">
  <img alt="Codacy grade" src="https://img.shields.io/codacy/grade/e11ce1e341554699ad523dbfe75be9c6?style=flat-square">
  <img alt="Codacy coverage" src="https://img.shields.io/codacy/coverage/e11ce1e341554699ad523dbfe75be9c6?style=flat-square">
  <br><strong>简单但绝不简陋的 Python3 爬虫项目。</strong>
  <br>参考<a href="https://mp.weixin.qq.com/s/K4RGr5NqMFAUKtB0KFPV5g">「建立完美的 Python 项目」</a> 创建 
</p>

Hydra 力求用最简单的代码实现聚合 HG 多平台的数据。

从本项目中你可以看到：**熟悉的 [Python 基础语法](https://github.com/521xueweihan/python)**、**如何编写爬虫**、**操作数据库**、**常用第三库**、**分析网页**、**解析接口**、**编写单元测试**、**mock 请求**、**异常监控和管理**、**保证代码质量的自动化**、**GitHub Action** 等实战应用。

此项目是汇集「HelloGitHub」在每个平台的账号和内容数据，方便我们的作者们看到自己作品的数据（[投稿吗？](https://www.yuque.com/docs/share/bf781d29-cc94-44dd-b226-9d70fa38fa1c)）。支持平台：[博客园](https://www.cnblogs.com/xueweihan/)、[头条](https://www.toutiao.com/c/user/token/MS4wLjABAAAAigrrKo-3rjLpxaH4Go3BrZRqHTIhLW3e30QjfFXgzNQ/)、[知乎](https://www.zhihu.com/people/xueweihan)、[掘金](https://juejin.cn/user/1574156384091320)、[即刻](https://web.okjike.com/u/ff31a838-6eb9-440d-9970-dabc5b2c0309) 等。

你要[加入](https://mp.weixin.qq.com/s/9FUQ2i0HbemwfIj9sa1p0A)我们吗？

## 一、运行

> 基于 Python 3.9.1 实现，理论上支持 3.7.5+

首先，下载项目：`git clone` or [点击下载 zip 包](https://github.com/HelloGitHub-Team/Hydra/archive/main.zip)

然后，在项目根目录创建配置文件，[.local_env.yaml](/doc/local_env.yaml)。

最后，把玩起来吧！

1. 安装 poetry：`pip install poetry`

2. 安装依赖：在项目根目录执行 `poetry install --no-root`

3. 运行单个爬虫：`poetry run python main.py wechat|cnblogs|toutiao|csdn|zhihu|juejin|jike`

运行遇到问题和更多说明[点这里](/doc/install.md)，贡献代码[看这里](/doc/contribute.md)

## 二、展示
比如：查看某一日发布的原创文章数据

```
SELECT
	summary ,
	clicks_count ,
	platform ,
	publish_date
FROM
	hydra_content
WHERE
	content_type = "article"
AND publish_date = "2021-03-01"
AND(
	is_original = 1
	OR is_original IS NULL
);
```

```
+-----------------------------------------+----------------+------------+----------------+
| summary                                 |   clicks_count | platform   | publish_date   |
|-----------------------------------------+----------------+------------+----------------|
| 更新啦！第 59 期《HelloGitHub》开源月刊 |             77 | csdn       | 2021-03-01     |
| 更新啦！第 59 期《HelloGitHub》月刊     |           5133 | wechat     | 2021-03-01     |
| 更新啦！第 59 期《HelloGitHub》开源月刊 |           1022 | cnblogs    | 2021-03-01     |
| 更新啦！第 59 期《HelloGitHub》开源月刊 |           1053 | toutiao    | 2021-03-01     |
| 更新啦！第 59 期《HelloGitHub》开源月刊 |           1879 | zhihu      | 2021-03-01     |
| 更新啦！第 59 期《HelloGitHub》开源月刊 |            931 | juejin     | 2021-03-01     |
+-----------------------------------------+----------------+------------+----------------+
6 rows in set
Time: 0.050s
```

## 三、声明
<a rel="license" href="https://creativecommons.org/licenses/by-nc-nd/4.0/deed.zh"><img alt="知识共享许可协议" style="border-width: 0" src="https://licensebuttons.net/l/by-nc-nd/4.0/88x31.png"></a><br>本作品采用 <a rel="license" href="https://creativecommons.org/licenses/by-nc-nd/4.0/deed.zh">署名-非商业性使用-禁止演绎 4.0 国际</a> 进行许可。
