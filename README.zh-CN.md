# m2w: Markdown to WordPress

<p align="left">
<a href=""><img src="https://img.shields.io/badge/python-3.7%2B-orange"></a>
<a href=""><img src="https://img.shields.io/badge/platform-Windows%7Clinux%7CMacOS-brightgreen"></a>
<a href=""><img src="https://img.shields.io/github/downloads/huangwb8/m2w/total"></a>
<a href=""><img src="https://img.shields.io/github/stars/huangwb8/m2w?style=social"></a>
</p>
基于Python将本地markdown推送和更新至Wordpress，支持REST API和Password模式

:star2::star2::star2: 欢迎 m2w 2.6！REST 上传更稳（taxonomy 缓存/`term_exists` 修正、报错更清晰、避免更新时无限重试），支持可配置超时；Password 模式拆分为模块化结构，旧入口依然可用；项目全面采用 vibe coding 方式维护，保持一致和轻量；可在 `myblog.py` 里过滤本地文件（如 `AGENTS.md`）避免进入上传流程。

中文教程: [Docker系列 WordPress系列 WordPress上传或更新Markdown的最佳实践-m2w 2.0](https://blognas.hwb0307.com/linux/docker/2813)

## 内容列表

- [m2w: Markdown to WordPress](#m2w-markdown-to-wordpress)
  - [内容列表](#内容列表)
  - [背景](#背景)
  - [安装](#安装)
  - [使用](#使用)
    - [开启 REST API](#开启-rest-api)
  - [项目展示](#项目展示)
  - [Q\&A](#qa)
  - [维护者](#维护者)
  - [使用许可](#使用许可)
  - [相关仓库](#相关仓库)

## 背景

`m2w` 是一个简单易用的自动上传和更新 markdown 到 WordPress 的工具，支持REST API (`2.5+`) 和Password模式。

`m2w` 具有以下特点：

+ 支持REST API模式，比传统的Password模式更加安全。如果你喜欢，也可以继续使用Password模式。
+ 可以开心地保留原有的文件结构 (～￣▽￣)～ 。
+ 通过多个`legacy_*.json` 同时管理多个网站。
+ 只需要使用1个 python 脚本 `myblog.py` 而不是两个（`m2w 1.0` 中的 `update.py` 和 `upload.py`）。
+ 忽略重复的新markdown的上传操作（`v2.2.4+`）。

### 2.6 相比 2.5 的变化

- REST API 上传更可靠：统一 taxonomy 缓存与 `term_exists` 处理，报错信息更清晰，避免更新时的无限重试。
- REST 请求支持可配置超时（默认 30s），适配网络较慢的网站。
- Password 模式重构为 `m2w.password.*` 模块，保留 `up_password` 等旧入口，兼容老脚本。
- 代码维护全面引入 vibe coding 方式，保证风格统一、依赖轻量。
- 可以在 `myblog.py` 中忽略特定本地文件（如 `AGENTS.md`、`CLAUDE.md`），防止它们参与上传/更新。

## 安装

> 推荐使用[Miniconda](https://docs.conda.io/en/latest/miniconda.html)来管理Python版本和相关依赖。

- Python >= 3.7.6
- 运行依赖：`python-frontmatter>=1.0.0`、`markdown>=3.3.6`、`python-wordpress-xmlrpc>=2.3`、`httpx>=0.24.0`（详见 `requirements.txt`）
- 采用 `pyproject.toml`（PEP 621 + setuptools）管理元数据和依赖，`setup.py` 仅保留兼容。

在2022年12月10日之后，`m2w` 已经上传到 [PyPi](https://pypi.org/project/m2w/)。直接安装：

```bash
pip install m2w
# 或固定版本
pip install -i https://pypi.org/simple m2w==2.6.2
```

从源码构建与安装：

```bash
python -m pip install --upgrade build
python -m build                       # 在 dist/ 下生成 wheel 与 sdist
python -m pip install dist/m2w-*.whl  # 安装构建产物
# 开发模式安装
python -m pip install -e .
```


## 使用

在 `path01` 目录下创建文件夹 `config`，并在文件夹创建 `user.json`，示例如下

```json
"web01": {
        "domain": "https://domain-01.com",
        "username": "username-01",
        "application_password": "password-01",
        // "password": "password-01",
        "path_markdown": [
            "E:/Github/m2w/@test/main",
            "E:/Github/m2w/@test/main2"
        ],
        "post_metadata": {
            "category": ["test"],
            "tag": ["test"],
            "status": "publish"
        },
        "path_legacy_json": "/config/legacy"
    }
```

参数说明：
  - `domain`: WordPress 站点的域名
  - `username`: WordPress 账户
  - `application_password`: 应用程序密码（推荐），与 `password` 二选一即可。获取方式见下文[开启 REST API](#开启-rest-api)
  - `password`: 账户密码，与 `application_password` 二选一即可，如果二者共存，优先使用 REST API。
  - `path_markdown`: 包含 markdown 文本的文件夹，可以有多个。
  - `post_metadata/path_legacy_json`: 不了解怎么设置的默认即可。

创建脚本 `myblog.py`，这里有一个[示例](https://github.com/huangwb8/m2w/blob/main/myblog.py)，需要将 `path_m2w` 修改为 `config` 文件夹所在的路径。

```python
path_m2w = '<path02>' # config文件夹的路径
```

准备工作完成后，直接运行这个命令即可：

```bash
python <path01>/myblog.py
```

> 想忽略某些本地辅助文件？在 `myblog.py` 里先过滤掉它们再调用 `up`，比如排除 `AGENTS.md` / `CLAUDE.md`，确保 vibe coding 文档不会被上传。
>
> 现在只需在 `myblog.py` 设置 `ignore_files = ["AGENTS.md", "CLAUDE.md"]`（支持 glob 与以 `re:` 开头的正则），无需改动 user.json。

### 忽略文件

- `myblog.py` 默认忽略 `AGENTS.md`、`CLAUDE.md`（避免上传 AI 助手文档）。
- 可添加 glob（如 `"**/draft-*.md"`、`"notes/**"`）或以 `re:` 开头的正则（如 `"re:.*/temp-.*\\.md$"`）。
- 如果不需要忽略，清空或删除 `ignore_files` 变量即可，旧脚本保持兼容。

### 开启 REST API

> 如果你想使用 REST API 模式，则需要这一步。

+ 如果您使用 wordfence 之类的安全插件，请**启用 WordPress 应用程序密码**:

   ![WBrffVs5Ty](https://chevereto.hwb0307.com/images/2023/06/05/WBrffVs5Ty.png)

+ 创建一个新的 REST API: 

   ![sq7kG7Vsqp](https://chevereto.hwb0307.com/images/2023/06/05/sq7kG7Vsqp.png)

+ 安全地保管该API。如果有必要，可以重新生成或删除:

   ![GddR0nP8mn](https://chevereto.hwb0307.com/images/2023/06/05/GddR0nP8mn.png)


## 项目展示

如下图所示，只需要一行`python myblog.py`，即可自动更新或上传markdown喔！

![image-20230609173358533](https://chevereto.hwb0307.com/images/2023/06/09/image-20230609173358533.png)

## Q&A

1. Q：上传文章的时候报错`httpx.ConnectError: [Errno 11001] getaddrinfo failed`

   A：大概是网站地址没有写对，首先检查地址是否配置正确，请不要在`url`后面加资源地址如`https://xxx.com/xx/xx`,只填写到`xx.com`即可

2. Q：使用`REST_API`方式上传的时候可以正常获取**文章、tag**列表，但是上传却一直失败

   A：`REST_API`使用的是应用程序密码，而不是网站的登录密码，请检查**application_password**配置项是否类似`xxxx xxxx xxxx xxxx xxxx`的格式,在最新版本使用`Rest_API`失败后会自动尝试使用`Client`重新上传，所以不用担心。

3. Q：我的服务器在国内但是上传速度慢并且经常失败

   A：如果开了代理，请将自己的网站加入到过滤地址内，尤其是`CFW(clash for windows)`用户。

## 更新日志

- **2025-12-22｜2.6.2**：默认忽略 `AGENTS.md` / `CLAUDE.md`，支持 glob 与以 `re:` 开头的正则；扫描时会输出被忽略的文件路径；未设置 `ignore_files` 时保持旧行为。
- **2025-12-21｜2.6.1**：修复 REST API 更新时的无限重试，统一 taxonomy 缓存与 `term_exists` 处理，REST 请求支持可配置超时；Password 模式模块化并保持兼容。

## 维护者

+ [@huangwb8](https://t.me/hwb0307)
+ [@FoxSuzuran](https://github.com/FoxSuzuran)

## 使用许可

m2w项目采用MIT license。详见[LICENSE](https://github.com/huangwb8/m2w/blob/main/license.txt)。

## 相关仓库

+ [nefu-ljw/python-markdown-to-wordpress](https://github.com/nefu-ljw/python-markdown-to-wordpress)
