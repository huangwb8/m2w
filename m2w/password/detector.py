"""Helpers for detecting markdown files for Password mode uploads."""

import fnmatch
import os
import re
import sys

from m2w.json2 import read_json_as_dict
from m2w.json2 import save_dict_as_json
from m2w.md5 import get_file_md5


def _compile_ignore(ignore_files):
    """
    Normalize ignore rules.

    Returns a list of dicts with "type" ("glob" | "regex") and "pattern".
    """
    compiled = []
    if not ignore_files:
        return compiled

    if isinstance(ignore_files, str):
        ignore_files = [ignore_files]

    for rule in ignore_files:
        if not rule:
            continue
        if isinstance(rule, str) and rule.startswith("re:"):
            try:
                compiled.append({"type": "regex", "pattern": re.compile(rule[3:])})
            except re.error:
                # Fall back to glob match if regex is invalid
                compiled.append({"type": "glob", "pattern": rule[3:]})
        else:
            compiled.append({"type": "glob", "pattern": rule})
    return compiled


def _should_ignore(path_abs, path_rel, ignore_rules):
    """
    Decide whether to ignore the given path according to compiled rules.
    """
    if not ignore_rules:
        return False

    basename = os.path.basename(path_abs)
    for rule in ignore_rules:
        pattern = rule["pattern"]
        if rule["type"] == "regex":
            if pattern.search(path_abs) or pattern.search(path_rel) or pattern.search(
                basename
            ):
                return True
        else:
            if (
                fnmatch.fnmatch(path_abs, pattern)
                or fnmatch.fnmatch(path_rel, pattern)
                or fnmatch.fnmatch(basename, pattern)
            ):
                return True
    return False


def find_files(path, suffix=".md", ignore_files=None, verbose=False):
    """
    Find all files with specified suffix in the path.

    Parameters
    ----------
    path: String. The path of files. Allow one or more paths.
    suffix: String. The suffix of target files.
    ignore_files: List. Gitignore-like glob patterns or regex (prefix with "re:").
    verbose: Boolean. Whether to output ignored entries.

    Returns
    -------
    List. Paths of target files.
    """
    result = []
    ignore_rules = _compile_ignore(ignore_files)

    def _walk(cur_path, suff=".md"):
        file_list = os.listdir(cur_path)
        for file in file_list:
            next_path = os.path.join(cur_path, file)
            rel_path = os.path.relpath(next_path, path)
            if _should_ignore(next_path, rel_path, ignore_rules):
                if verbose:
                    print(f"Ignored by ignore_files: {rel_path}")
                continue
            if os.path.isdir(next_path):
                _walk(next_path, suff)
            else:
                if next_path.endswith(suff):
                    result.append(next_path)

    _walk(path, suffix)
    return result


def md_detect(path_markdown, path_legacy_json, verbose=True, ignore_files=None):
    """
    Gather paths of brand-new and changed legacy markdown files.

    Parameters
    ----------
    + path_markdown: String. The path of markdown files. Allow one or more paths.
    + path_legacy_json: String. The path of the 'legacy.json' file.
    + verbose: Boolean. Whether output running messages of the function.
    + ignore_files: List. Gitignore-like glob patterns or regex (prefix with "re:").

    Returns
    -------
    Dict. With two keys———"legacy" and "new".
    + The "new" means the brand-new markdown files in the "path_markdown" dir.
    + The "legacy" means the changed legacy markdown files in the "path_markdown" dir.
    """
    if len(path_markdown) == 0:
        if verbose:
            print("No path about markdown files. Please assign at least one.")
        sys.exit(0)

    if not os.path.isfile(path_legacy_json):
        if verbose:
            print("No legacy json. All markdown files would be treated as brand-new ones.")

        new = []
        for path in path_markdown:
            new = new + find_files(path, suffix=".md", ignore_files=ignore_files, verbose=verbose)
        new = sorted(set(new), key=new.index)

        md5_dict = {}
        for filepath in new:
            md5_dict[filepath] = get_file_md5(filepath)
        save_dict_as_json(md5_dict, path_legacy_json)
        if verbose:
            print("Create legacy json for new markdowns!")

        return {"new": new, "legacy": []}

    if verbose:
        print("With legacy.json. Confirm new or changed legacy markdown files.")

    all_files = []
    for path in path_markdown:
        all_files = all_files + find_files(path, suffix=".md", ignore_files=ignore_files, verbose=verbose)

    md5_legacy = read_json_as_dict(path_legacy_json)
    md5_all = {}
    for filepath in all_files:
        md5_all[filepath] = get_file_md5(filepath)
    save_dict_as_json(md5_all, path_legacy_json)

    new = set(md5_all.keys()).difference(set(md5_legacy.keys()))
    if len(new) >= 1:
        for filepath in new:
            if verbose:
                print("New content! " + filepath)
            md5_legacy[filepath] = get_file_md5(filepath)
    else:
        if verbose:
            print("No new markdown files. Ignored.")

    md5_filter = md5_all
    intersect_key = set(sorted(md5_all.keys())) & set(sorted(md5_legacy.keys()))
    for filepath in intersect_key:
        if md5_legacy[filepath] == md5_all[filepath]:
            md5_filter.pop(filepath)
        else:
            if verbose:
                print("Content changed!: ", filepath)
    if len(md5_filter) == 0:
        if verbose:
            print("No changed legacy markdown files. Ignored.")

    return {"new": list(new), "legacy": list(md5_filter.keys())}
