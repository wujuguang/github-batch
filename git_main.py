#!usr/bin/env python
# coding: utf-8

import os

from git_batch import GitTool
from git_conf import git_fork_dir, mux_plug_dir

if __name__ == '__main__':
    """运行实例.
    """

    logs_dir = os.path.join(os.path.abspath(os.path.dirname(__file__)), "log")

    report_log = os.path.join(logs_dir, "git.log")
    shells_str = "git pull upstream master:master >> %(log)s && git push origin master:master >> %(log)s"
    shells_str = ''.join(("cd %s && ", shells_str % {"log": report_log}))

    repository = GitTool(parent_path=git_fork_dir, shells=shells_str, log=report_log)
    repository.build_tree = True
    repository()

    report_log = os.path.join(logs_dir, "plugins.log")
    shells_str = "git pull >> %(log)s"
    shells_str = ''.join(("cd %s && ", shells_str % {"log": report_log}))

    repository = GitTool(parent_path=mux_plug_dir, shells=shells_str, log=report_log)
    repository()
