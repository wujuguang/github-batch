#!usr/bin/env python
# coding: utf-8

import os
import sys

from git_batch import GitTool
from git_conf import git_repository_dir, git_fork_dir

reload(sys)
sys.setdefaultencoding("utf-8")

if __name__ == '__main__':
    """运行实例.
    """

    logs_dir = os.path.join(os.path.abspath(os.path.dirname(__file__)), "log")

    report_log = os.path.join(logs_dir, "repository.log")
    shells_str = "git pull >> %(log)s"
    shells_str = ''.join(("cd %s && ", shells_str % {"log": report_log}))

    repository = GitTool(parent_path=git_repository_dir, shells=shells_str, log=report_log)
    repository()

    report_log = os.path.join(logs_dir, "fork.log")
    shells_str = "git pull upstream master:master >> %(log)s && git push origin master:master >> %(log)s"
    shells_str = ''.join(("cd %s && ", shells_str % {"log": report_log}))

    repository = GitTool(parent_path=git_fork_dir, shells=shells_str, log=report_log)
    repository.build_tree = True
    repository()
