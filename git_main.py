#!/usr/bin/env python3

"""运行实例: 批量更新本地仓库, 并同步 fork 仓库的 upstream/origin."""

import os
import shlex

from git_batch import GitTool
from git_conf import git_repository_dir, git_fork_dir

if __name__ == '__main__':
    logs_dir = os.path.join(os.path.abspath(os.path.dirname(__file__)), "log")

    report_log = os.path.join(logs_dir, "repository.log")
    shells_str = f"cd {{path}} && git pull >> {shlex.quote(report_log)}"

    repository = GitTool(parent_path=git_repository_dir, shells=shells_str,
                         log=report_log)
    repository()

    report_log = os.path.join(logs_dir, "fork.log")
    quoted_log = shlex.quote(report_log)
    shells_str = (f"cd {{path}} && git pull upstream master:master >> {quoted_log}"
                  f" && git push origin master:master >> {quoted_log}")

    repository = GitTool(
        parent_path=git_fork_dir,
        shells=shells_str,
        log=report_log)

    repository.build_tree = True
    repository()
