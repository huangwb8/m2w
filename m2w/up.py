# -*- coding: utf-8 -*-
# @Time : 2022/12/03 16:42
# @Author : huangwb8
# @File : up.py
# @Function: m2w project
# @Software: VSCode
# @Reference: original

import m2w.update
import m2w.upload
from m2w.md5 import get_file_md5
from m2w.json2 import save_dict_as_json 
from m2w.json2 import read_json_as_dict
import sys
import os

####===============================Functions
def find_files(path, suffix = ".md"):
    """
    ### Description
    Find all files with specifed suffix in the path

    ### Parameters
    path: String. The path of files. Allow one or more paths.
    suffix: String. The suffix of target files.

    ### Return
    List. Paths of target files.

    ### Reference
    https://www.cnblogs.com/2bjiujiu/p/7255599.html
    https://www.cnblogs.com/CGRun/p/16309265.html

    """
    # Gather results
    result = []

    # Use a sub function
    def ff(path, suffix = ".md"):
        file_list = os.listdir(path)
        for file in file_list:
            cur_path = os.path.join(path, file)
            # print(cur_path)
            if os.path.isdir(cur_path):
                ff(cur_path, suffix)
            else:
                if cur_path.endswith(suffix):
                    result.append(cur_path)
    
    # Output data
    ff(path, suffix = ".md")
    return result


def md_detect(path_markdown, path_legacy_json, verbose = True):

    """
    ### Description
    Gather paths of brand-new and changed legacy markdown files.

    ### Parameters
    + path_markdown: String. The path of markdown files. Allow one or more paths.
    + path_legacy_json: String. The path of the 'legacy.json' file.
    + verbose: Boolean. Whether output running messages of the function.

    ### Return
    Dict. With two keys———"legacy" and "new". 
    + The "new" means the brand-new markdown files in the "path_markdown" dir. 
    + The "legacy" means the changed legacy markdown files in the "path_markdown" dir. 
    """

    # Test whether the path_markdown has existed
    if len(path_markdown) == 0:
        if verbose: 
            print('No path about markdown files. Please assign at least one.')
        sys.exit(0)

    # Test whether the legacy_json has existed
    if os.path.isfile(path_legacy_json) == False:

        # Warning
        if verbose:
            print('No legacy json. All markdown files would be treated as brand-new ones.')

        # Gather new markdown files
        new = []
        for path in path_markdown:
            new = new + find_files(path, suffix = ".md")
        new = sorted(set(new), key = new.index) # Keep unique elements. Ref: https://blog.csdn.net/u011361880/article/details/76237096

        # md5 sum of new files
        dict = {}
        for i in new:
            dict[i] = get_file_md5(i)
        save_dict_as_json(dict, path_legacy_json)
        if verbose:
            print('Create legacy json for new markdowns!')

        # Output
        result = {"new": new, "legacy": []} # 
        return result
    else:
        if verbose:
            print('With legacy.json. Confirm new or changed legacy markdown files.')

        # all files
        all = []
        for path in path_markdown:
            all = all + find_files(path, suffix = ".md")

        # Compare changes in markdown files
        md5_legacy = read_json_as_dict(path_legacy_json)
        md5_all = {}
        for i in all:
            md5_all[i] = get_file_md5(i)
        save_dict_as_json(md5_all, path_legacy_json) # Update legacy json
        
        # Confirm new files
        new = set(md5_all.keys()).difference(set(md5_legacy.keys()))
        if len(new) >= 1:
            for j in new:
                if verbose:
                    print('New content! ' + j)
                md5_legacy[j] = get_file_md5(j)
        else:
            if verbose:
                print('No new markdown files. Ignored.')
        # print(new)
        # print(list(md5_all.keys()))
        # print(list(md5_legacy.keys()))

        # Confirm changed legacy files
        md5_filter = md5_all
        intersect_key = set(sorted(md5_all.keys())) & set(sorted(md5_legacy.keys()))
        for i in intersect_key:
            if md5_legacy[i] == md5_all[i]:
                md5_filter.pop(i)
            else:
                if verbose:
                    print('Content changed!: ', i)
        if len(md5_filter) == 0:
            if verbose:
                    print('No changed legacy markdown files. Ignored.')


        # Output
        result = {"new": list(new), "legacy": list(md5_filter.keys())} # 
        return result


def up(client, md_upload, md_update, post_metadata, verbose = True):
    """
    ### Description
    Upload or update markdown files to your WordPress site.

    ### Parameters
    + client: The return of m2w.wp.wp_xmlrpc.
    + md_upload: String. The path of new markdown files.
    + md_upload: String. The path of changed legacy markdown files.
    + post_metadata: Dict. The metadata of a post.
    + verbose: Boolean. Whether output running messages of the function.

    ### Return
    None
    """

    # Upload new markdown files
    if len(md_upload) > 0 :
        md_cnt = 0
        all_cnt = len(md_upload)
        process_number = 0
        failpaths = []  # 存储上传失败的文件路径
        for filepath in md_upload:
            process_number = process_number + 1
            post = m2w.upload.make_post(filepath, post_metadata)
            if post is not None:
                m2w.upload.push_post(post, client)
                md_cnt = md_cnt + 1
                if verbose: print('Process number: %d/%d  SUCCESS: Push "%s"' % (process_number, all_cnt, filepath))
            else:
                failpaths.append(filepath)
                if verbose: 
                    print('Process number: %d/%d  WARNING: Can\'t push "%s" because it\'s not Markdown file.' % (process_number, all_cnt, filepath))
        if verbose: print('SUCCESS: %d files have been pushed to your WordPress.' % md_cnt)

        if verbose: 
            if len(failpaths) > 0:
                print('WARNING: %d files haven\'t been pushed to your WordPress.' % len(failpaths))
                print('\nFailure to push these file paths:')
                for failpath in failpaths:
                    print(failpath)


    # Update changed legacy files
    if len(md_update) > 0:
        for filepath in md_update:
            post = m2w.update.find_post(filepath, client)
            if post is not None:
                ret = m2w.update.update_post_content(post, filepath, client)
                if ret:
                    if verbose: print('SUCCESS: Update the file "%s"' % filepath)
                else:
                    if verbose: print('FAILURE: Update the file "%s"' % filepath)
            else:
                if verbose: print('FAILURE to find the post. Please check your User Configuration and the title in your WordPress.')        
