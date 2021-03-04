## 你好
热爱开源的小伙伴，Hydra 期待你的贡献。如果发现 BUG、你认为可以更好的写法、接入平台数据、更加自动化的行为，
都欢迎你来贡献代码。我为你准备了以下资料：

## 项目结构
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
├── Dockerfile  // Docker 配置文件
├── docker.sh  // docker 启动命令
├── pyproject.toml  // 依赖
└── shell
    ├── format.sh  // 自动修改代码格式等
    ├── lint.sh  // 类型和代码格式检测
    └── test.sh  // 运行测试
```

## 启动有 3 种

1. `main.py`：命令行运行
2. `run.py`：基于 `schedule` 的定时任务
3. [`docker.sh`](docker_template.sh)：docker 方式运行（定时任务方式）：
    - 安装 [docker](https://www.digitalocean.com/community/tutorials/how-to-install-and-use-docker-on-ubuntu-18-04)
    - 命令：
        - 构建镜像：bash run.sh build
        - 启动镜像：bash run.sh up
        - 停止镜像：bash run.sh down
        - 进入镜像：bash run.sh sh

## 贡献代码

准备工作：

1. 安装 commit 钩子：`poetry run pre-commit install`
2. 手动触发钩子：`pre-commit run --all-files`

代码风格自动可以自动处理，但是类型检测和测试覆盖率（95%）不能提交。手动运行自查：

- 检查代码风格和类型：shell/lint.sh
- 自动格式化代码等：shell/format.sh
- 运行测试：shell/test.sh
