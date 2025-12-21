from importlib import metadata


def _load_version() -> str:
    try:
        return metadata.version("m2w")
    except metadata.PackageNotFoundError:
        # 回退：源码环境下无法读取已安装包元数据时使用占位符
        return "0.0.0"


__version__ = _load_version()

from .json2 import read_json_as_dict
from .md5 import get_file_md5
from .password import md_detect
from .up import up
from .wp import wp_xmlrpc
