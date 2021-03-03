# Hydra（九头蛇）

<p align="center">
  <img width="75%" src="https://raw.githubusercontent.com/HelloGitHub-Team/Hydra/main/doc/cover.png"/>
  <br>简单绝不简陋的 Python3 爬虫项目。
  <br>参考<a href="https://mp.weixin.qq.com/s/K4RGr5NqMFAUKtB0KFPV5g">「建立完美的 Python 项目」</a> 创建 
</p>

Hydra 力求用最简单的代码实现功能，仅实现了爬虫最实用的部分：爬取->入库，爬的部分没有用任何框架。

从本项目中你可以：**熟悉你已经掌握的各种 [Python 语法](https://github.com/521xueweihan/python)**、**如何编写爬虫**、**操作数据库**、**常用第三库**、**分析网页**、**解析接口**、**编写单元测试**、**mock 请求**、**异常监控和管理**、**保证代码质量的自动化** 等实战应用。

此项目是汇集「HelloGitHub」在每个平台的账号和内容数据，方便我们的作者们看到自己作品的数据。支持平台：[博客园](https://www.cnblogs.com/xueweihan/)、[头条](https://www.toutiao.com/c/user/token/MS4wLjABAAAAigrrKo-3rjLpxaH4Go3BrZRqHTIhLW3e30QjfFXgzNQ/)、[知乎](https://www.zhihu.com/people/xueweihan)、[掘金](https://juejin.cn/user/1574156384091320)、[即刻](https://web.okjike.com/u/ff31a838-6eb9-440d-9970-dabc5b2c0309) 等。

你要[加入](https://mp.weixin.qq.com/s/9FUQ2i0HbemwfIj9sa1p0A)我们吗？

## 一、运行项目

> 基于 Python3 实现

在项目根目录创建配置文件，[.local_env.yaml](/doc/local_env.yaml)。然后：

1. 安装 [pyenv](https://github.com/pyenv/pyenv#installation)
2. 安装并切换 Python 版本：`pyenv shell 3.7.5`
3. 安装 poetry：`pip3 install poetry`
4. 安装依赖：在项目根目录执行 `poetry install --no-root`
5. 运行单个爬虫：`poetry run python main.py wechat|cnblogs|toutiao|csdn|zhihu|juejin|jike`
    - 检查代码风格等：`shell/lint.sh`
    - 格式化代码等：`shell/format.sh`
    - 测试：`shell/test.sh`
6. 启动定时：`poetry run python run.py`

[更多说明](/doc/install.md)

## 三、结构
```
.
├── doc
│   ├── install.md  // 更详细的说明
│   └── local_env.yaml  // 配置参数模版
├── hydra  // 源码在这里
│   ├── config.py  // 配置类
│   ├── db  // 数据库操作
│   │   ├── base.py  
│   │   ├── curd.py
│   │   └── model.py
│   ├── spider  // 爬虫
│   │   ├── base.py  // 基类
│   │   ├── cnblogs.py
│   │   ├── csdn.py
│   │   ├── jike.py
│   │   ├── juejin.py
│   │   ├── toutiao.py
│   │   ├── wechat.py
│   │   └── zhihu.py
│   ├── tests  // 测试
│   └── utils.py  // 工具类
├── logs  // 日志
├── main.py  // 命令行启动（单个）
├── run.py  // 常驻启动（全部）
├── pyproject.toml  // 依赖
└── shell
    ├── format.sh  // 自动修改代码格式等
    ├── lint.sh  // 类型和代码格式检测
    └── test.sh  // 运行测试
```

## 三、声明
<a rel="license" href="https://creativecommons.org/licenses/by-nc-nd/4.0/deed.zh"><img alt="知识共享许可协议" style="border-width: 0" src="https://licensebuttons.net/l/by-nc-nd/4.0/88x31.png"></a><br>本作品采用 <a rel="license" href="https://creativecommons.org/licenses/by-nc-nd/4.0/deed.zh">署名-非商业性使用-禁止演绎 4.0 国际</a> 进行许可。
