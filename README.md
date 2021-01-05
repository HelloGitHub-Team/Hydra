# Hydra（九头蛇）

监控多个平台文章、短内容的表现：阅读、点赞、分享等。支持平台：

- 公众号 

## 一、运行项目

1. 安装 pyenv：`pip install pyenv`
2. 切换本地的 Python 版本：`pyenv local 3.7.5`
3. 安装 poetry：`pip install poetry`
4. 安装依赖：`poetry install --no-root`（项目根目录）
5. 激活环境：`poetry shell`

解释和可能会用到的命令：

1. 保证 Python 版本为 3.7.5：pyenv local 3.7.5
    - `pyenv versions`：列出所有的 Python 版本
    - `pyenv install/uninstall 版本号`：安装对应的版本
    - `pyenv shell/global/local 版本号`：shell/切换全局/本地的 Python 版本（shell > local > global）
2. 安装依赖：`poetry install`（加 `--no-dev` 是安装正式环境的依赖）
    - `poetry env list/remove`：列出/删除 虚拟环境
    - `poetry env info`：查看环境信息（路径：--path）
    - `poetry env use 环境绝对路径`：切换环境
    - `poetry add 库的名称`：增加库到环境中
    - `poetry run 命令`：可以不切换环境直接通过命令运行项目
3. 代码风格检测（后面加到 commit 钩子）
    - 检查代码风格：`sh shell/lint.sh`
    - 自动修改代码：`sh shell/format.sh`

    
## 二、项目依赖的库

### 依赖管理
- [pyenv](https://github.com/pyenv/pyenv)：Python 版本管理
- [poetry](https://github.com/python-poetry/poetry)：环境、依赖管理


### 代码检测
- [flake8](https://gitlab.com/pycqa/flake8)：代码风格、错误检测工具
- [isort](https://github.com/timothycrosley/isort)：自动优化 import 那部分的代码
- [mypy](https://mypy.readthedocs.io/en/latest/index.html)：代码的类型和静态检测
- [black](https://github.com/psf/black)：代码风格检测和纠正

### 依赖的库
[点击查看](pyproject.toml)