# m2w 2: Markdown to WordPress

<p align="left">
<a href=""><img src="https://img.shields.io/badge/python-3.7%2B-orange"></a>
<a href=""><img src="https://img.shields.io/badge/platform-Windows%7Clinux%7CMacOS-brightgreen"></a>
<a href=""><img src="https://img.shields.io/github/downloads/huangwb8/m2w/total"></a>
<a href=""><img src="https://img.shields.io/github/stars/huangwb8/m2w?style=social"></a>
</p>
基于Python将本地markdown推送和更新至Wordpress

教程: [Docker系列 WordPress系列 WordPress上传或更新Markdown的最佳实践-m2w 2.0](https://blognas.hwb0307.com/linux/docker/2813)。

注意：**m2w v2.5将支持WordPress REST API**，但目前还是开发版本。如果m2w v2.5已经开发测试完成，我们会提交一个稳定版本供大家使用。目前仅推荐大家使用[m2w v2.2.11](https://github.com/huangwb8/m2w/releases/tag/v2.2.11)。不便之处，敬请谅解！

## 内容列表

- [展示](#展示)
- [背景](#背景)
- [安装](#安装)
- [使用](#使用)
- [相关仓库](#相关仓库)
- [维护者](#维护者)
- [如何贡献](#如何贡献)
- [使用许可](#使用许可)

## 背景

`m2w` 是一个简单易用的自动上传和更新 markdown 到 WordPress 的工具，`m2w 1.0` 的开发工作已经在 `v1.0.7` 中被冻结。 `m2w 1.0` 对大多数人来说已经足够强大了，但有些特性对使用者不太友好：

+ 必须分配旧的或新的路径来存储博文，这意味着使用者无法随意放置文件。
+ 无法同时对多个站点进行管理。

你仍然可以找到m2w 1.0的使用说明（[中](https://github.com/huangwb8/m2w/blob/main/v1/README.zh-CN.md)/[英](https://github.com/huangwb8/m2w/blob/main/v1/README.md)），但我原则上不再维护`m2w 1.0`了。

现在，更强大的`m2w 2`来和大家见面啦！`m2w 2` 具有以下特点：

+ 与 `m2w 1.0` 相比，使用 和`config/user.json` 略微不同的方式维护用户信息。
+ 可以开心地保留原有的文件结构 (～￣▽￣)～ 。
+ 通过多个`legacy_*.json` 同时管理多个网站。
+ 只需要使用1个 python 脚本 `myblog.py` 而不是两个（`m2w 1.0` 中的 `update.py` 和 `upload.py`）。
+ 忽略重复的新markdown的上传操作（`v2.2.4+`）。该特性对于用户从`m2w 1.0`升级到`m2w 2`十分友好！
+ 像m2w 1.0 稳定且好用！

## 安装
1. poetry 安装方式

   >有关poetry的安装请查看官方文档[Introduction | Documentation | Poetry - Python dependency management and packaging made easy (python-poetry.org)](https://python-poetry.org/docs/)

   1. 下载随2.3.0更新上传的位于`poetry` 目录下的`pyproject.toml`和`poetry.lock`，放在一个你喜欢并且容易找到的文件夹
   2. 在目录下运行`poetry install`
   3. 查看接下来的使用教程部分

2. Anaconda安装

   > 建议使用 [Conda](https://conda.io/projects/conda/en/stable/user-guide/install/download.html) 来管理 Python 版本和相关依赖项。这是一个第3方示例教程：《[win10安装 Anaconda3](https://www.cnblogs.com/syushin/p/15113986.html)》。自己找找，教程很多的 (～￣▽￣)～ 

   依赖项：

   ```python
   # Python 3.7.4 is the version I use m2w. I'm not sure whether it could work well in more advanced Python versions.
   python_requires='>=3.7.4'
   
   # Dependencies
   install_requires=[
       "python-frontmatter>=1.0.0",
       "markdown>=3.3.6",
       "python-wordpress-xmlrpc>=2.3"
   ]
   ```

3. 官方pip安装

   2022-12-10 之后，我将`m2w 2` 上传到 [PyPi](https://pypi.org/project/m2w/)，这样你只需要在Shell中运行`pip install m2w `即可安装。

   考虑到不同源同步延迟的可能性，你可以指定`m2w 2`的版本号和源：

   ```bash
   pip install -i https://pypi.org/simple m2w
   ```

4. 直接下载该仓库中的代码（不推荐）

   如果你采用这种方式，你还需要在环境中安装以下三个包

   `python-frontmatter`,`markdown`,`python-wordpress-xmlrpc`

建议安装最新版本的`m2w 2`。

## 使用

### v2.2.11

1. 通过`pip`或这个Github repotory安装 m2w。
2. 新建文件`<path01>/myblog.py`文件（名字随便取），这是一个[示例](https://github.com/huangwb8/m2w/blob/main/myblog.py)。将`myblog.py`文件中的`path_m2w`赋值为`<path02>`

```python
# Absolute path of m2w
path_m2w = '<path02>'
```

3. 新建文件`<path02>/config/user.json`，这是一个[示例](https://github.com/huangwb8/m2w/blob/main/config/user.json)。根据实际情况修改参数即可。你可以创建很多个类似于`web01`的网站/帐户喔！参数解释如下：
+ **domain,username,password**：WordPress站点相关信息，比如站点URL、帐户名、密码。
+ **path_markdown**：添加任意多的顶级文件夹 (～￣▽￣)～ 
+ **post_metadata**：默认类别信息。有分类（category）、标签（tag）和状态（status）3个属性。
+ **websites**：可以添加任意数量的帐户 (～￣▽￣)～ 
+ **path_legacy_json**：不用改，保持原样。它是记录md5值用的，本质上是一个Python Dict的json版本。

```json
"web01": {
        "domain": "https://domain-01.com",
        "username": "username-01",
        "password": "password-01",
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

4. 最后，运行脚本：

```bash
python '<path01>/myblog.py'
```

### v2.3.0+

1. 在`安装`步骤中部署的环境中（pip安装方式则是系统环境），下载[m2w](https://github.com/huangwb8/m2w)仓库中的`myblog.py`文件到环境所在文件夹下

2. 运行`myblog.py`文件

   1. 首次运行可能会出现提示`配置文件config.ini已在目录下生成,请填写配置后重新启动程序`，以下是相关配置项设置

       ```ini
       [path]
       m2w_path = D:\Programing\GitHub\MyGithub\m2w_test
       
       [upload]
       force_upload = False
       verbose = True
       
       ```

      + **m2w_path**：`安装`步骤中环境文件夹所在的位置，默认生成在`myblog.py`运行的当前文件夹

      + **force_upload**：是否开启强制上传，默认是`False`

      + **verbose**：是否开启控制台打印输出，默认是`True`

   2. 配置好`config.ini`后，再次运行`myblog.py`,有可能出现提示

      `配置文件user.json已在目录{config.ini中配置的地址}\config下生成,请填写配置后重新启动程序`，以下为相关配置项设置

       ```json
       {
           "web_test": {
               "domain": "https://domain-01.com",
               "username": "username-01",
               "password": "password-01",
               "application_password":"xxxxxx",
               "path_markdown": [
                   "E:/Github/m2w/@test/main",
                   "E:/Github/m2w/@test/main2"
               ],
               "post_metadata": {
                   "category": [
                       "test"
                   ],
                   "tag": [
                       "test"
                   ],
                   "status": "publish"
               },
               "path_legacy_json": "/config/legacy"
           }
       }
       ```
      
      + **domain,username,password**：WordPress站点相关信息，比如站点URL、帐户名、密码。
      
      + **application_password**:站点的应用程序密码，入口在`个人资料->应用程序密码`，请和站点密码区别开来。

        _注：如果你配置了应用程序密码，程序将默认使用rest_api方式更新文章，反之则使用client方式_

      + **path_markdown**：添加任意多的顶级文件夹(也就是该路径下存有待上传的.md文件)
      
      + **post_metadata**：默认类别信息。有分类（category）、标签（tag）和状态（status）3个属性。
      
      + **path_legacy_json**：不用改，保持原样。它是记录md5值用的，本质上是一个Python Dict的json版本。
      
      _如果想针对多个网站做同步设置，只需要做如下设置_
      
      ```json
      {
          "web-1":{xxxxxx},
          "web-2":{xxxxxx},
          "web-3":{xxxxxx},
          ………………
      }
      ```
      
      然后根据配置项所需内容给每个网站填写上对应的参数即可

3. 当完成前两步配置后，再次运行`myblog.py`，不出意外的话就会出现上传成功的提示了

## 项目展示

如下图所示，只需要一行`python myblog.py`，即可自动更新或上传markdown喔！

![Typora_zKwwaE10Qe](https://chevereto.hwb0307.com/images/2022/12/14/Typora_zKwwaE10Qe.gif)

## Q&A

1. Q：上传文章的时候报错`httpx.ConnectError: [Errno 11001] getaddrinfo failed`

   A：大概是网站地址没有写对，首先检查地址是否配置正确，请不要在`url`后面加资源地址如`https://xxx.com/xx/xx`,只填写到`xx.com`即可

2. Q：使用`REST_API`方式上传的时候可以正常获取**文章、tag**列表，但是上传却一直失败

   A：`REST_API`使用的是应用程序密码，而不是网站的登录密码，请检查**application_password**配置项是否类似`xxxx xxxx xxxx xxxx xxxx`的格式,在最新版本使用`Rest_API`失败后会自动尝试使用`Client`重新上传，所以不用担心。

3. Q：我的服务器在国内但是上传速度慢并且经常失败

   A：如果开了代理，请将自己的网站加入到过滤地址内，尤其是`CFW(clash for windows)`用户。

## 相关仓库

+ [nefu-ljw/python-markdown-to-wordpress](https://github.com/nefu-ljw/python-markdown-to-wordpress)

## 维护者

[@huangwb8](https://t.me/hwb0307)

## 如何贡献

非常欢迎你的加入！[提一个 Issue](https://github.com/huangwb8/m2w/issues/new) 或者提交一个 Pull Request。


m2w遵循 [Contributor Covenant](http://contributor-covenant.org/version/1/3/0/) 行为规范。

### 贡献者

[@FoxSuzuran](https://github.com/FoxSuzuran)

## 使用许可

m2w项目采用MIT license。详见[LICENSE](https://github.com/huangwb8/m2w/blob/main/license.txt)。
