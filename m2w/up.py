

from m2w.rest_api import RestApi
from m2w.up_password import md_detect, up_password
from m2w.wp import wp_xmlrpc
import sys
import os
import shutil

async def up(
        path_markdown, 
        path_legacy_json,
        domain, username, password, application_password, post_metadata,
        last_update_time_change = False, force_upload=False, verbose=True, rest_api=True, max_retries = 10
        ):
    
    """
    ### Description
    Upload or update markdown files to your WordPress site.

    ### Parameters
    + path_markdown: The path of markdown files
    + path_legacy_json: The path of legacy*.json
    + domain, username, password, application_password, post_metadata: The data of a WordPress website
    + last_update_time_change: Boolean. Whether to update the last update time of the post. Only work in REST API mode
    + force_upload: Boolean. Whether check the existence of a new post before uploading. Default is False, which means that every new post would receive checking
    + verbose: Boolean. Whether output running messages of the function
    + rest_api: Whether to use REST API mode
    + max_retries: Integer. The max retry time when meeting failure

    ### Return
    None
    """

    # Backup old legacy*.json
    is_first_legacy_exist = os.path.exists(path_legacy_json)
    if is_first_legacy_exist:
        shutil.copyfile(path_legacy_json, path_legacy_json + "_temporary_old")

    # Mode
    if rest_api:
        # REST API Mode
        if verbose:
            print("(ฅ´ω`ฅ) REST API Mode. Very safe!")
        rest = RestApi(
            url=domain, wp_username=username, wp_password=application_password
        )
    else:
        # Legacy Password Mode
        if verbose:
            print("Σ( ° △ °|||)︴Legacy Password Mode. Not safe!")
        client = wp_xmlrpc(domain, username, password)
    
    # Gather paths of brand-new and changed legacy markdown files
    res = md_detect(path_markdown, path_legacy_json, verbose=verbose)
    md_upload = res["new"]
    md_update = res["legacy"]

    # Backup the latest legacy*.json
    shutil.copyfile(path_legacy_json, path_legacy_json + "_temporary_latest")
    if not is_first_legacy_exist:
        shutil.copyfile(path_legacy_json, path_legacy_json + "_temporary_old")

    # Upload & Update
    if len(md_upload) > 0 or len(md_update) > 0:
        for retry in range(max_retries):
            try:
                if rest_api:
                    # Use REST API mode to upload/update articles
                    await rest.upload_article(
                        md_message=res,
                        post_metadata=post_metadata,
                        verbose=verbose,
                        force_upload=force_upload,
                        last_update=last_update_time_change,
                    )
                else:
                    # Use Password mode to upload/update articles
                    up_password(
                        client,
                        md_upload,
                        md_update,
                        post_metadata,
                        force_upload=force_upload,
                        verbose=verbose,
                    )
                if os.path.exists(path_legacy_json + "_temporary_latest"):
                    shutil.copyfile(path_legacy_json + "_temporary_latest", path_legacy_json)     
                break
            except Exception as e:
                print("OOPS, the upload/update process failed!")
                if os.path.exists(path_legacy_json + "_temporary_old"):
                    shutil.copyfile(path_legacy_json + "_temporary_old", path_legacy_json)
                if retry < max_retries - 1:
                    print("Retrying...")
                    continue
                else:
                    print("Maximum retries exceeded. Exiting.")
                    sys.exit(0)
    else:
        if verbose:
            print("Without any new or changed legacy markdown files. Ignored.")