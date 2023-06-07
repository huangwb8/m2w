# Change

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