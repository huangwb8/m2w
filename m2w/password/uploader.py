"""Upload and update helpers for Password mode."""

import m2w.update
import m2w.upload


def up_password(client, md_upload, md_update, post_metadata, force_upload=False, verbose=True):
    """
    Upload or update markdown files to your WordPress site.

    Parameters
    ----------
    + client: The return of m2w.wp.wp_xmlrpc.
    + md_upload: String. The path of new markdown files.
    + md_update: String. The path of changed legacy markdown files.
    + post_metadata: Dict. The metadata of a post.
    + force_upload: Boolean. Whether check the existence of a new post before uploading. Default is False, which means that every new post would receive checking.
    + verbose: Boolean. Whether output running messages of the function.
    """

    def upload_one_post(client, filepath, post_meta, all_cnt, md_cnt, process_number, is_verbose):
        post = m2w.upload.make_post(filepath, post_meta)
        process_number2 = process_number + 1
        if post is not None:
            m2w.upload.push_post(post, client)
            if is_verbose:
                md_cnt2 = md_cnt + 1
                print('Process number: %d/%d  SUCCESS: Push "%s"' % (process_number2, all_cnt, filepath))
        else:
            failpaths.append(filepath)
            if is_verbose:
                print(
                    'Process number: %d/%d  WARNING: Can\'t push "%s" because it\'s not Markdown file.'
                    % (process_number2, all_cnt, filepath)
                )
        return md_cnt2, process_number2

    if force_upload is False:
        if verbose:
            print("You don't want a force uploading. The existence of the post would be checked.")
    else:
        if verbose:
            print("You want a force uploading? Great!")

    if len(md_upload) > 0:
        md_cnt = 0
        process_number = 0
        all_cnt = len(md_upload)
        failpaths = []
        for filepath in md_upload:
            if force_upload is False:
                post_wp = m2w.update.find_post(filepath, client)
                if post_wp is not None:
                    if verbose:
                        print('Warning: This post is existed in your WordPress site. Ignore uploading!')
                else:
                    if verbose:
                        print('This post is exactly a new one in your WordPress site! Try uploading...')
                    res = upload_one_post(client, filepath, post_metadata, all_cnt, md_cnt, process_number, verbose)
                    md_cnt = +res[0]
                    process_number = +res[1]
            else:
                res = upload_one_post(client, filepath, post_metadata, all_cnt, md_cnt, process_number, verbose)
                md_cnt = +res[0]
                process_number = +res[1]

        if verbose:
            print('SUCCESS: %d files have been pushed to your WordPress.' % md_cnt)
            if len(failpaths) > 0:
                print('WARNING: %d files haven\'t been pushed to your WordPress.' % len(failpaths))
                print('\nFailure to push these file paths:')
                for failpath in failpaths:
                    print(failpath)

    if len(md_update) > 0:
        for filepath in md_update:
            post = m2w.update.find_post(filepath, client)
            if post is not None:
                ret = m2w.update.update_post_content(post, filepath, client)
                if ret:
                    if verbose:
                        print('SUCCESS: Update the file "%s"' % filepath)
                else:
                    if verbose:
                        print('FAILURE: Update the file "%s"' % filepath)
            else:
                if verbose:
                    print(
                        'Warning: Could not find the post "%s" in WordPress. '
                        'Treating it as new content and uploading instead...' % filepath
                    )
                res = upload_one_post(client, filepath, post_metadata, 1, 0, 0, verbose)
