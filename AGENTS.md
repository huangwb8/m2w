# AGENTS

- **项目定位**：`m2w` 将本地 Markdown 文章批量上传或更新到 WordPress，支持 REST API 与密码模式。核心入口为 `m2w/up.py`（异步 orchestrator），REST API 逻辑在 `m2w/rest_api/`，传统 XML-RPC 逻辑在 `m2w/password/`。
- **环境要求**：Python >= 3.7.6。依赖见 `setup.py`（`python-frontmatter`/`markdown`/`python-wordpress-xmlrpc`/`httpx`）。本地开发可 `pip install -e .`。
- **配置要点**：运行前需准备 `config/user.json`（可含多个站点配置）。`m2w/config/config.py` 在缺失配置时会自动生成模板并退出，以提醒补全。`@test/config/user.json` 含示例凭证，仅供本地演示，请勿外泄或对生产站点直接运行。
- **常用命令**：`python myblog.py` 或自定义脚本调用 `up` 进行同步；`python setup.py sdist bdist_wheel` 生成发布包，`pip install ./dist/m2w-<ver>.tar.gz` 做本地验收；发布 PyPI 参考 `setup.py` 顶部注释（`twine upload dist/*<ver>*`）。
- **验证策略**：暂无自动化测试；可用 `@test/myblog-test.py` + `@test/main*` 内的 Markdown 做演练，但会实际请求目标站点，务必使用测试站点/凭证。变更上传逻辑后建议手动跑一次并检查 WordPress 侧文章状态。
- **版本与文档**：改版本需同时更新 `setup.py` 与 `m2w/__init__.py` 中的版本号，并同步 `README*.md`/`CHANGELOG.MD`。保持 README、示例脚本与配置示例的字段一致性。
- **提交提示**：避免改动 `dist/`、`m2w.egg-info/` 等生成物；保持 Python 3.7 兼容（勿引入 3.8+ 专属语法）；涉及凭证的文件请使用占位符或确保不提交敏感信息。
- 回复结束时应该使用中文总结。
