
import sys
from wordpress_xmlrpc import Client

def wp_xmlrpc(domain,username, password):
    """
    错误控制相关的Client函数
    :param domain: 网站域名
    :param username: 帐号
    :param password: 该帐号的密码
    """
    try:
        client = Client(domain + '/xmlrpc.php', username, password)  # 客户端
        print('SUCCESS to connect to your WordPress website: ' + domain)
        return client
    except Exception as e:
        print('FAILED to connect to your WordPress website: ' + str(e))
        # 正常退出
        sys.exit(0)