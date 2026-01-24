# Change Log

## [2.7.2] - 2026-01-24

### Added（新增）
- **LaTeX 数学公式渲染支持**：新增 `m2w/math.py` 模块，支持 `$...$` 行内公式和 `$$...$$` / `\begin...\end` 块级公式的 LaTeX 渲染
- **Markdown 表格支持**：所有模式下（REST API 和 Password）现已启用 `tables` 扩展
- **GFM Admonition 支持**（可选）：新增对 GitHub 风格提示框（`> [!NOTE]`、`> [!TIP]` 等）的支持，需安装 `markdown-gfm-admonition` 可选依赖
- 感谢 [@Mareep-YANG](https://github.com/Mareep-YANG) 通过 [PR #20](https://github.com/huangwb8/m2w/pull/20) 提供的 LaTeX 公式渲染、表格和 GFM Admonition 功能代码

### Changed（变更）
- 所有 Markdown 处理模块（REST API 的 create/update 和传统模式的 upload/update）统一扩展配置，新增数学公式、表格和 Admonition 支持
- 优化依赖管理：将 `markdown-gfm-admonition` 设为可选依赖（`pip install m2w[admonition]`），未安装时自动回退跳过

## [2.7.1] - 2026-01-24

### Fixed（修复）
- 版本号更正：将版本号从 2.7.0 更新为 2.7.1

## [Unreleased]

### Added（新增）
- 支持 `post_type` 字段：可创建自定义文章类型（如 `shuoshuo`、`page` 等）
- 支持 `slug` 字段：可设置文章 URL 别名
- 支持 `status` 字段修改：可动态修改文章状态（`draft`、`publish` 等）
- 支持 `status: delete` 删除文章：设置后可删除 WordPress 文章和本地 Markdown 文件
- 文章匹配逻辑优化：现在基于 frontmatter 中的 `title` 而非文件名进行匹配
- 感谢 [@Shulelk](https://github.com/Shulelk) 通过 [PR #21](https://github.com/huangwb8/m2w/pull/21) 提供的功能灵感和建议

### Changed（变更）
- 重构项目文档，采用 `/init-project` 规范组织 `AGENTS.md` 和 `CLAUDE.md`
- 新增 `@test` 目录的详细说明，明确测试配置示例 [@test/config/user.json](@test/config/user.json) 的用途
- 新增"测试驱动"工程原则：所有新优化的 m2w 代码，都要在 @test 里通过测试才可以交付
- 优化配置说明，增加配置结构示例和自动生成机制说明
- 统一文件引用规范，使用 markdown 链接语法使路径可点击

## [2.6.2]

1. 默认在 `myblog.py` 忽略 `AGENTS.md`、`CLAUDE.md`，支持 gitignore 样式 glob 和以 `re:` 开头的正则，扫描日志会提示被忽略的文件路径。
2. 忽略列表仅在脚本内配置，未设置 `ignore_files` 的旧脚本保持原始行为。

## [2.6.1]

1. 修复 REST API 模式下文章更新时的无限重试问题，统一 taxonomy 缓存与 term_exists 处理，错误信息更清晰，便于排查。
2. REST API 请求新增可配置超时（默认 30s），避免因超时过短导致的上传失败。
3. Password 模式代码拆分为 `m2w.password.*` 模块，保留 `up_password` 兼容旧入口。

## [2.5.7]

1. 支持REST API/Password模式的一个stable版本。

___

## [2.5.2]
___

1. 修复了一些小小的bug
2. 现在`Rest_api`请求方法在失败后会自动转用`client`方法重新上传

## [2.3.3]
___

1. 增加对`Rest_api`的支持,该方法似乎更慢但是较安全
2. 可以在配置项里面设置启用`Rest_api`,需要提供`应用程序密码`
## [2.3.0]
___

1. 修复了python>=3.9时的`module 'collections' has no attribute 'Iterable’`报错
2. 修复了当出现报错导致上传不成功时仍更新文章`md5`的`json`存储文件的bug(此bug会导致当报错文章未上传成功时且未更新时，不能二次上传的问题)
3. 将配置项和代码分离,只需运行`myblog.py`后填写对应配置即可
4. 增加poetry支持,构建更加简便快捷
5. 优化代码结构，更新`README.zh-CN.md`说明文件
