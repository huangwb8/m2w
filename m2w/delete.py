
import os
from m2w.json2 import read_json_as_dict
from wordpress_xmlrpc.methods.posts import DeletePost
from m2w.json2 import save_dict_as_json
import importlib

def delete_post(post, filepath, client):
    up_password = importlib.import_module('m2w.up_password')
    md5_legacy = read_json_as_dict(up_password.PATH_LEGACY_JSON)
    md5_legacy.pop(filepath)
    save_dict_as_json(md5_legacy, up_password.PATH_LEGACY_JSON)  # Update legacy json
    os.remove(filepath)
    print("Delete article:", filepath)
    return client.call(DeletePost(post.id))
