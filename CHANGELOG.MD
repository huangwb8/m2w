# Change

# Change

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
