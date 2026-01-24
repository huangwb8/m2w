



from m2w.rest_api import RestApi
from m2w.rest_api.utils import DEFAULT_TIMEOUT
from m2w.rest_api.rate_limiter import RateLimiter
from m2w.rest_api.progress_manager import ProgressManager

from m2w.password import md_detect, up_password

from m2w.wp import wp_xmlrpc

import sys

import os

import shutil



async def up(

        path_markdown,

        path_legacy_json,

        domain, username, password, application_password, post_metadata,

        last_update_time_change = False, force_upload=False, verbose=True, rest_api=True, max_retries = 10, rest_timeout = DEFAULT_TIMEOUT, ignore_files = None,

        # 新增速率限制参数
        rate_limit_enabled = False,
        request_delay = 1.0,
        batch_size = 10,
        batch_delay = 5.0,
        max_429_retries = 5,
        initial_backoff = 2.0,

        # 新增断点续传参数
        progress_enabled = False,
        progress_file = None

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

    + rest_timeout: Timeout (seconds) for REST API HTTP requests. Default is DEFAULT_TIMEOUT

    + ignore_files: List. Gitignore-like glob patterns or regex (prefix with "re:").

    + rate_limit_enabled: Boolean. Whether to enable rate limiting for requests.

    + request_delay: Float. Delay between requests in seconds. Default is 1.0.

    + batch_size: Integer. Number of files to process per batch. Default is 10.

    + batch_delay: Float. Delay between batches in seconds. Default is 5.0.

    + max_429_retries: Integer. Maximum retries when encountering HTTP 429 errors. Default is 5.

    + initial_backoff: Float. Initial backoff time for 429 errors in seconds. Default is 2.0.

    + progress_enabled: Boolean. Whether to enable progress saving for resumable uploads.

    + progress_file: String. Path to progress file. If None, defaults to legacy.json directory.


    ### Return

    None

    """



    # Backup old legacy*.json

    is_first_legacy_exist = os.path.exists(path_legacy_json)

    if is_first_legacy_exist:

        shutil.copyfile(str(path_legacy_json), str(path_legacy_json) + "_temporary_old")



    # Mode

    if rest_api:

        # REST API Mode

        if verbose:

            print("(ฅ´ω`ฅ) REST API Mode. Very safe!")

        rest = RestApi(

            url=domain, wp_username=username, wp_password=application_password, timeout=rest_timeout

        )

        # 初始化速率限制器
        if rate_limit_enabled:
            rest.rate_limiter = RateLimiter(
                request_delay=request_delay,
                batch_size=batch_size,
                batch_delay=batch_delay,
                max_429_retries=max_429_retries,
                initial_backoff=initial_backoff,
                verbose=verbose
            )

        # 初始化进度管理器
        if progress_enabled:
            progress_path = progress_file or str(os.path.join(os.path.dirname(path_legacy_json), ".m2w_progress.json"))
            rest.progress_manager = ProgressManager(
                progress_file=progress_path,
                enabled=True,
                verbose=verbose
            )

    else:

        # Legacy Password Mode

        if verbose:

            print("Σ( ° △ °|||)︴Legacy Password Mode. Not safe!")

        client = wp_xmlrpc(domain, username, password)

    

    # Gather paths of brand-new and changed legacy markdown files

    res = md_detect(path_markdown, path_legacy_json, verbose=verbose, ignore_files=ignore_files)

    md_upload = res["new"]

    md_update = res["legacy"]



    # Backup the latest legacy*.json

    shutil.copyfile(str(path_legacy_json), str(path_legacy_json) + "_temporary_latest")

    if not is_first_legacy_exist:

        shutil.copyfile(str(path_legacy_json), str(path_legacy_json) + "_temporary_old")



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

                if os.path.exists(str(path_legacy_json) + "_temporary_latest"):

                    shutil.copyfile(str(path_legacy_json) + "_temporary_latest", str(path_legacy_json))     

                break

            except Exception as e:

                print("OOPS, the upload/update process failed!")

                print(f"{e.__class__.__name__}: {e}")

                if os.path.exists(str(path_legacy_json) + "_temporary_old"):

                    shutil.copyfile(str(path_legacy_json) + "_temporary_old", str(path_legacy_json))

                if retry < max_retries - 1:

                    print("Retrying...")

                    continue

                else:

                    print("Maximum retries exceeded. Exiting.")

                    sys.exit(0)

    else:

        if verbose:

            print("Without any new or changed legacy markdown files. Ignored.")
