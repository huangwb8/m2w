# m2w: Markdown to WordPress - 项目指令

## 项目目标

`m2w` 是一个将本地 Markdown 文章批量上传或更新到 WordPress 的工具。

**核心特性**：
- 支持两种模式：REST API（推荐）和传统 XML-RPC 密码模式
- 异步批量上传/更新文章
- 支持分类、标签、文章状态等元数据配置
- 自动检测 Markdown frontmatter 并合并到 WordPress 字段

**项目定位**：
- 核心入口：[m2w/up.py](m2w/up.py)（异步 orchestrator）
- REST API 逻辑：[m2w/rest_api/](m2w/rest_api/)
- 传统 XML-RPC 逻辑：[m2w/password/](m2w/password/)

## 环境要求

- **Python 版本**：>= 3.7.6
- **核心依赖**（见 [setup.py](setup.py)）：
  - `python-frontmatter`：解析 Markdown frontmatter
  - `markdown`：Markdown 转 HTML
  - `httpx`：异步 HTTP 客户端
  - `python-wordpress-xmlrpc`：传统 XML-RPC 支持

**本地开发安装**：
```bash
pip install -e .
```

## 配置要点

### 主配置文件

运行前需准备 [config/user.json](config/user.json)，可包含多个站点配置。

**配置结构**：
```json
{
    "站点域名": {
        "domain": "https://example.com",
        "username": "用户名",
        "application_password": "WordPress 应用密码",
        "path_markdown": ["本地 Markdown 目录路径"],
        "post_metadata": {
            "category": ["分类"],
            "tag": ["标签"],
            "status": "publish"
        },
        "path_legacy_json": "可选：历史 JSON 文件路径"
    }
}
```

### 配置自动生成

[m2w/config/config.py](m2w/config/config.py) 在缺失配置时会自动生成模板并退出，提醒用户补全。

### 测试配置

[@test/config/user.json](@test/config/user.json) 是实际可用的测试配置示例。

**重要提示**：
- 该文件包含真实凭证，仅供本地演示使用
- 请勿外泄或对生产站点直接运行
- 所有新优化的 m2w 代码，都要在 @test 里通过测试才可以交付

## 常用命令

### 基本使用

```bash
# 运行主程序
python myblog.py

# 或在自定义脚本中调用
from m2w import up
up.run()
```

### 构建与发布

```bash
# 生成发布包
python setup.py sdist bdist_wheel

# 本地验收安装
pip install ./dist/m2w-<ver>.tar.gz

# 发布到 PyPI（参考 setup.py 顶部注释）
twine upload dist/*<ver>*
```

## 验证策略

**当前状态**：暂无自动化测试

**手动测试流程**：
1. 使用 [@test/myblog-test.py](@test/myblog-test.py) 进行演练
2. 使用 [@test/main](@test/main/) 内的 Markdown 文件测试
3. 检查 WordPress 站点文章状态

**注意事项**：
- 测试会实际请求目标站点
- 务必使用测试站点/测试凭证
- 变更上传逻辑后建议手动跑一次完整流程

## 版本管理

### 版本号同步

修改版本号需同时更新：
- [setup.py](setup.py) 中的版本号
- [m2w/__init__.py](m2w/__init__.py) 中的版本号
- [README.md](README.md) 和 [CHANGELOG.MD](CHANGELOG.MD)

### 文档一致性

保持以下文件的一致性：
- README 文档（README.md 和 README.zh-CN.md）
- 示例脚本
- 配置示例

### 文档更新优先级

更新项目文档时遵循以下优先级：
1. **先更新英文版** ([README.md](README.md))：确保技术内容准确完整
2. **再同步到中文版** ([README.zh-CN.md](README.zh-CN.md))：保持与英文版内容一致
3. **同步更新 CHANGELOG.MD**：所有文档变更都需记录在变更日志中

## 提交规范

### 应避免的内容

- 改动 [dist/](dist/)、[m2w.egg-info/](m2w.egg-info/) 等构建生成物
- 引入 Python 3.8+ 专属语法（需保持 3.7 兼容）
- 提交包含真实凭证的配置文件

### 凭证处理

- 使用占位符替代真实凭证
- 确保不提交敏感信息到版本控制
- 测试凭证仅存放在 @test 目录

## 核心工作流

当用户提出与 m2w 相关的需求时，按以下流程执行：

### 1. 需求理解

- 理解用户是想修改上传逻辑、配置格式，还是添加新功能
- 确认是否涉及 REST API 或密码模式
- 识别对现有功能的影响范围

### 2. 执行流程

代码开发 → 测试验证（@test 目录）→ 文档更新 → 版本发布

### 3. 验证要求

**所有代码变更必须在 @test 目录通过测试**：
- 使用 [@test/config/user.json](@test/config/user.json) 作为测试配置
- 运行 [@test/myblog-test.py](@test/myblog-test.py) 验证
- 检查 WordPress 测试站点的实际结果

## 工程原则

本项目遵循以下工程原则：

| 原则 | 核心思想 | 在本项目中的体现 |
|------|----------|------------------|
| **KISS** | Keep It Simple, Stupid | 追求极致简洁，避免过度设计；文档标题不使用序号前缀（用 `##` 而非 `## 1)`） |
| **YAGNI** | You Aren't Gonna Need It | 只实现当前需要的功能 |
| **DRY** | Don't Repeat Yourself | 相似逻辑应抽象复用 |
| **SOLID** | 面向对象设计五大原则 | 单一职责、开闭原则等 |
| **关注点分离** | Separation of Concerns | 不同层次逻辑应分离 |
| **测试驱动** | Test Before Deliver | 所有新优化都要在 @test 里通过测试才可以交付 |

**原则冲突时的决策优先级**：
1. **正确性 > 一切**
2. **简洁性 > 灵活性**
3. **清晰性 > 性能**
4. **扩展性 > 紧凑性**

## 默认语言

除非用户明确要求其他语言，始终使用简体中文与用户对话与撰写文档/说明。

## 联网与搜索

默认优先使用项目内文件与本地上下文；确需联网获取信息时，优先使用本地搜索工具。仅当本地工具不足以满足需求时再使用其它联网手段，并说明原因与保留关键链接。

## 目录结构

```
m2w/
├── @test/                      # 测试目录（所有新代码必须在此通过测试）
│   ├── config/
│   │   └── user.json          # 测试配置示例（实际可用）
│   ├── main/                   # 测试用 Markdown 文章
│   ├── main2/                  # 测试用 Markdown 文章
│   ├── main3/                  # 测试用 Markdown 文章
│   ├── main4/                  # 测试用 Markdown 文章
│   └── myblog-test.py         # 测试脚本
├── config/                     # 配置文件目录
│   └── user.json              # 主配置文件
├── m2w/                        # 核心代码
│   ├── config/                # 配置管理
│   ├── password/              # XML-RPC 密码模式
│   ├── rest_api/              # REST API 模式
│   ├── up.py                  # 核心入口（异步 orchestrator）
│   └── ...
├── AGENTS.md                   # 项目指令（本文件）
├── CLAUDE.md                   # Claude Code 特定适配
├── CHANGELOG.MD                # 变更日志
├── README.md                   # 项目说明
└── setup.py                    # 安装配置
```

## Claude Code 特定说明

### 文件引用规范

在 Claude Code 中引用文件时，使用 markdown 链接语法：
- **文件**：`[filename.md](路径/filename.md)`
- **特定行**：`[filename.md:42](路径/filename.md#L42)`
- **行范围**：`[filename.md:42-51](路径/filename.md#L42-L51)`
- **目录**：`[目录名/](路径/目录名/)`

### 任务管理

- 使用 TodoWrite 工具跟踪复杂任务的进度
- 完成任务后及时标记为 completed
- 拆分大任务为可管理的小步骤

### 代码变更规范

- 修改代码前先使用 Read 工具阅读文件
- 优先使用 Edit 工具进行精确修改
- 避免不必要的格式化或重构

## 变更边界

- 仅修改与当前任务直接相关的文件
- 不主动添加用户未要求的功能
- 保持现有代码风格和结构
- 所有新优化代码必须在 @test 目录通过测试

## 变更记录规范

**重要原则**：凡是项目的更新，都要统一在 [CHANGELOG.MD](CHANGELOG.MD) 里记录。

### 记录范围

每次修改以下内容时，必须更新 CHANGELOG.MD：
- **项目指令文件**：CLAUDE.md、AGENTS.md 的任何修改
- **项目结构变更**：新增/删除/重命名目录或关键文件
- **工作流变更**：核心工作流程的调整
- **工程原则变更**：新增、修改或删除工程原则
- **重要配置变更**：影响项目行为的配置文件修改
- **测试相关变更**：@test 目录的内容变更

### 记录格式

遵循 [Keep a Changelog](https://keepachangelog.com/zh-CN/1.1.0/) 格式：

```markdown
## [版本号] - YYYY-MM-DD

### Added（新增）
- 新增了 XXX 功能/章节：用途是 YYY

### Changed（变更）
- 修改了 XXX 章节：原因是 YYY，具体变更内容是 ZZZ

### Fixed（修复）
- 修复了 XXX 问题：表现是 YYY，修复方式是 ZZZ
```

### 记录时机

- **修改前**：先在 CHANGELOG.MD 的 `[Unreleased]` 部分草拟变更内容
- **修改后**：完善变更描述，添加具体细节和影响范围
- **发布时**：将 `[Unreleased]` 内容移至具体版本号下

## 有机更新原则

当需要更新本文档时：

### 1. 理解意图

首先理解用户需求背后的意图和在工作流中的本质作用

### 2. 定位生态位

每条规则/要求都应找到其在整个文档结构中的"生态位"——它与其他内容的关系、它服务的目标、它影响的其他部分

### 3. 协调生长

更新一个部分时，检查并同步更新相关部分：
- 更新工作流步骤时，同步更新示例和验证清单
- 更新输出规范时，同步更新引用该规范的其他章节
- 更新术语定义时，全局统一替换
- **更新本文档时，必须同步更新 CHANGELOG.MD**
- **更新本文档后，确保 CLAUDE.md 的核心内容保持一致**
- 保持文档格式规范：层级标题不使用序号前缀（用 `##` 而非 `## 1)`），因为 Markdown 本身有层级结构

### 4. 保持呼吸感

文档应该像生物体一样有"呼吸感"——章节之间有逻辑流动，而非割裂的清单

### 5. 定期修剪整合

当某个章节变得过于臃肿时，主动重构

---

**提示**：修改本文档后，请立即在 [CHANGELOG.MD](CHANGELOG.MD) 中记录变更。这是项目管理的强制性要求，不是可选项。
