# m2w: Markdown to WordPress

Upload and update local markdown to WordPress via Python

Demo: [https://blognas.hwb0307.com](https://blognas.hwb0307.com)


## Table of Contents

- [Background](#background)
- [Install](#install)
- [Usage](#usage)
- [Related Efforts](#related-efforts)
- [Maintainers](#maintainers)
- [Contributing](#contributing)
- [License](#license)

## Background

Recently, I started to play WordPress blog. I was looking for **an easy-to-use tool for automatical upload & update of  markdown** with minimum operation in WordPress dashboard. Finally, I found the project [nefu-ljw/python-markdown-to-wordpress](https://github.com/nefu-ljw/python-markdown-to-wordpress) available for this need. However, this project does not possess enough automation in updating old Markdown documents. Also, it is necessary for users to declare the same private information among scripts.

m2w is based on [nefu-ljw/python-markdown-to-wordpress](https://github.com/nefu-ljw/python-markdown-to-wordpress) and have some new features：

+ Use `config/user.json` to maintain the user information
+ File management via `new`和`legacy` documents
+ The md5 sum of files in the `legacy` document would be calculated before updating. Only files with changes would be update. New md5 sum of legacy markdowns would be stored in the `config/legacy.json` file.

## Install

+ Dependency

```
pip3 install python-frontmatter
pip3 install markdown
pip3 install python-wordpress-xmlrpc
```

+ Define your `config/user.json`

```json
{
    // Main 
    "main": "E:/Github/m2w/blog",
    
    // Main/new
    "symbol_new": "new",
    
    // Main/legacy
    "symbol_legacy": "legacy",
    
    // Domain, Username, and Password
    "domain": "https://blog.domain.com",
    "username": "user",
    "password": "user_password",
    
    // Default category, tag or status of articles
    "post_metadata": {
        "category": ["test"],
        "tag": ["test"],
        "status": "publish"
    },
    
    // Do not change this setting
    "path_legacy_json": "/config/legacy.json"
}
```

+ Download the Repo and save in `E:/Github/m2w`, for example. Set `path_m2w` as `'E:/Github/m2w'` in every script.

  ```python
  path_m2w = 'E:/Github/m2w'
  ```

+ Scripts `get_posts.py` and `new_posts.py` are only used to test whether you `user.json` really work.

## Usage

+ Document tree:

```
blog
├──legacy
└──new
```

+ Write your new markdown in `new` document. Run `upload.py` to upload new markdonws.
+ Run `update.py` if any changes in `legacy`document.

+ All scripts can be used as:

```bash
python3 <script>.py
```

## Related Efforts

- [nefu-ljw/python-markdown-to-wordpress](https://github.com/nefu-ljw/python-markdown-to-wordpress)

## Maintainers

[@huangwb8](https://github.com/huangwb8)

## Contributing

Feel free to dive in! [Open an issue](https://github.com/huangwb8/m2w/issues/new) or submit PRs.

m2w follows the [Contributor Covenant](http://contributor-covenant.org/version/1/3/0/) Code of Conduct.

### Contributors

Nobody yet.


## License

Getting suggestions from [@nefu-ljw](https://github.com/nefu-ljw)
