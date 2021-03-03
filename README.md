# Hydra（九头蛇）

基于 Python3 实现的汇集 HelloGitHub 在多个平台的账号信息。包含文章、短内容的表现，即阅读、点赞、分享等。

支持：公众号、博客园、头条、CSDN、知乎、掘金、即刻

**注意：** 本项目不是爬虫，仅聚合自己的 HelloGitHub 账号在多个平台的数据，方便查看和分析！

## 一、运行项目

创建配置文件：[.local_env.yaml](/doc/local_env.yaml)

1. 安装 [pyenv](https://github.com/pyenv/pyenv#installation)
2. 安装并切换 Python 版本：`pyenv shell 3.7.5`
3. 安装 poetry：`pip3 install poetry`
4. 安装依赖：在项目根目录执行 `poetry install --no-root`
5. 运行项目：`poetry run python main.py wechat|cnblogs|toutiao|csdn|zhihu|juejin|jike`
    - 检查代码风格等：`shell/lint.sh`
    - 格式化代码等：`shell/format.sh`
    - 测试：`shell/test.sh`

[更多说明](/doc/install.md)

## 二、展示



## 三、声明
<a rel="license" href="https://creativecommons.org/licenses/by-nc-nd/4.0/deed.zh"><img alt="知识共享许可协议" style="border-width: 0" src="https://licensebuttons.net/l/by-nc-nd/4.0/88x31.png"></a><br>本作品采用 <a rel="license" href="https://creativecommons.org/licenses/by-nc-nd/4.0/deed.zh">署名-非商业性使用-禁止演绎 4.0 国际</a> 进行许可。
