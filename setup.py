from setuptools import setup, find_packages

"""
### 参考

+ [python--如何将自己的包上传到PyPi并可通过pip安装](https://blog.csdn.net/yifengchaoran/article/details/113447773)
+ [花了两天，终于把 Python 的 setup.py 给整明白了](https://zhuanlan.zhihu.com/p/276461821)
+ [Black: 一键美化Python代码 - 知乎](https://zhuanlan.zhihu.com/p/336238526): 美化代码


### 步骤
要将自己的python项目上传到PyPi，需要按照以下步骤操作：

+ 首先，你需要确保你的项目已经打包成了一个可以安装的python包。这通常需要在项目根目录下创建一个名为"setup.py"的文件，并在该文件中指定项目的依赖关系、安装选项等信息。

+ 其次，你需要在PyPi上注册一个账号，并登录。

+ 接下来，打开命令行界面，进入到你的项目根目录。

+ 修改setup.py的版本号。更新README.md。完成Github仓库的更新和加tag。

+ 输入"pip install twine"来安装twine工具。 必要时可更新工具包：pip install --upgrade twine setuptools wheel

+ 使用"python setup.py sdist"命令来生成项目的源代码包。 如果要测试该包，可运行类似命令： python setup.py sdist; pip install .\dist\m2w-2.5.13.tar.gz

+ 使用"python setup.py bdist_wheel"命令来生成项目的长描述。

+ 上传至PyPi。输入"twine upload dist/*2.5.13* --verbose"来上传项目的源代码包。

+ 在上传过程中，你需要输入你在PyPi上注册的用户名和密码。

一旦上传完成，你的项目就已经成功发布到了PyPi上。你可以在PyPi的网站上搜索你的项目名称，找到你的项目，并查看它的安装和使用说明。

### My environment

+ Without Proxy like v2ray
+ conda activate pypi-3.10
+ cat ~./.pypirc

### Package URL
+ https://pypi.org/project/m2w

### How to install
+ pip install --upgrade -i https://pypi.org/simple m2w 
+ pip install -i https://pypi.org/simple m2w==2.5.13
+ pip install m2w 

"""

VERSION = "2.5.13"

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="m2w",
    version=VERSION,
    description=VERSION + ": Optimize organization of m2w configuration. Both password and REST API supported!",
    long_description=long_description,
    long_description_content_type="text/markdown",
    author=["Bensz", "FoxSuzuran"],
    author_email="hwb2012@qq.com",
    url="https://github.com/huangwb8/m2w",
    packages=find_packages(),
    include_package_data=True,
    keywords=["markdown", "wordpress", "xmlrpc"],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    install_requires=[
        "python-frontmatter>=1.0.0",
        "markdown>=3.3.6",
        "python-wordpress-xmlrpc>=2.3",
        "httpx>=0.24.0",
    ],
    python_requires=">=3.7.6",
)
