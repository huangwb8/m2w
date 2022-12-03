

from m2w.json2 import read_json_as_dict
from m2w.up import md_detect, up
from m2w.wp import wp_xmlrpc

####===============================m2w path

# Absolute path of m2w
path_m2w = 'E:/Github/m2w'

####===============================Parameters

# User JSON
# path_user_json = path_m2w + '/@test/config/user.json' # Only for test mode
path_user_json = path_m2w + '/config/user.json'
user = read_json_as_dict(path_user_json)

# Global
path_markdown = user['path_markdown']
path_legacy_json = path_m2w + user['path_legacy_json'] 

# Optional Configuration
post_metadata = user['post_metadata']

####===============================Programe

if __name__ == '__main__':

    websites = user['websites']

    for i in websites:

        # Select a WordPress website
        website = websites[i]

        # Connect the WordPress website
        print('========')
        client = wp_xmlrpc(website['domain'], website['username'], website['password'])

        # # Gather paths of brand-new and changed legacy markdown files
        path_legacy_json2 = path_legacy_json + '_' + i + '.json'
        res = md_detect(path_markdown, path_legacy_json2, verbose = True)
        md_upload = res['new']
        md_update = res['legacy']

        # Upload or Update
        if len(md_upload) > 0 or len(md_update) > 0:
            print(i, ': With new or changed legacy markdown files.')
            up(client, md_upload, md_update, post_metadata, verbose = True)
        else:
            print(i, ': Without any new or changed legacy markdown files. Ignored.')