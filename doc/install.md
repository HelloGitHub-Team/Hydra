## 一、命令
解释和可能会用到的命令：

1. 保证 Python 版本为 3.9.1：pyenv local 3.9.1
    - `pyenv versions`：列出所有的 Python 版本
    - `pyenv install/uninstall 版本号`：安装对应的版本
    - `pyenv shell/global/local 版本号`：shell/切换全局/本地的 Python 版本（shell > local > global）
2. 安装依赖：`poetry install`（加 `--no-dev` 是安装正式环境的依赖）
    - `poetry env list/remove`：列出/删除 虚拟环境
    - `poetry env info`：查看环境信息（路径：--path）
    - `poetry show`：查看安装的包信息
    - `poetry env use 环境绝对路径`：切换环境
    - `poetry add 库的名称`：增加库到环境中
    - `poetry run 命令`：可以不切换环境直接通过命令运行项目
3. 安装 commit 钩子：`poetry run pre-commit install`
4. 手动运行代码风格检测和钩子：
    - 检查代码风格：`sh shell/lint.sh`
    - 自动修改代码：`sh shell/format.sh`
    - 钩子：`pre-commit run --all-files`

    
## 二、依赖说明

### 依赖管理
- [pyenv](https://github.com/pyenv/pyenv)：Python 版本管理
- [poetry](https://github.com/python-poetry/poetry)：环境、依赖管理


### 代码检测
- [flake8](https://gitlab.com/pycqa/flake8)：代码风格、错误检测工具
- [isort](https://github.com/timothycrosley/isort)：自动优化 import 那部分的代码
- [mypy](https://mypy.readthedocs.io/en/latest/index.html)：代码的类型和静态检测
- [black](https://github.com/psf/black)：代码风格检测和纠正

### 测试
- [pytest](https://docs.pytest.org/en/stable/)：测试框架
- [requests-mock](https://requests-mock.readthedocs.io/en/latest/index.html)：Mock 请求返回的数据
- [pytest-cov](https://pypi.org/project/pytest-cov/)：测试覆盖率

### 其它
- [pre-commit](https://pre-commit.com/)：Git 的钩子

### 依赖的库
[点击查看](pyproject.toml)