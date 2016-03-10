#!usr/bin/env python
# coding: utf-8

"""批量更新指定目录下存储的所有Git Repository.
"""

from __future__ import print_function, unicode_literals

import os
import os.path
from datetime import datetime
from treelib import Tree


class GitTool(object):
    def __init__(self, parent_path, shells, log=None):
        """初始化操作目录, 操作命令.

            :parameter parent_path: 操作目录
            :parameter shells:　执行shell
            :parameter log: log文件
        """

        self.directory = parent_path
        self.unix_shell = shells
        self.log_file = log
        self.tree = None

    def _print(self, info=''):
        if self.log_file:
            os.system("echo %s >> %s" % (info, self.log_file))
        else:
            print(info)

    def run_work(self):
        """对指定的操作目录, 执行指定的操作命令.
        """

        # 如果传入日志路径不存在则创建
        if self.log_file:
            dir_name = os.path.dirname(self.log_file)
            if not os.path.exists(dir_name):
                os.makedirs(dir_name)
            if not os.path.exists(self.log_file):
                os.mknod(self.log_file)

        def build_tree(target_path):
            """创建树节点.

                :param target_path: 指定目录
            """

            self.tree = Tree()
            parent_name = os.path.basename(target_path)
            self.tree.create_node(parent_name, parent_name)

        def exist_node(sub_name):
            """指定节点是否存在.

                :param sub_name: 指定节点.
            """

            nid = 0
            while self.tree.contains(sub_name):
                sub_name = '_'.join((sub_name, str(nid)))
                nid += 1

            return sub_name

        def report_tree(target_path, out_file=True):
            """输出文件树.

                :param target_path: 指定节点.
                :param out_file: 指定节点.
            """

            if out_file:
                report_file = os.path.basename(target_path)
                self.tree.save2file('%s.txt' % report_file)
            else:
                self.tree.show()

        def process_target_path(target_path, target_tag=None):
            """对指定目录执行操作.

                :param target_path: 指定目录
                :param target_tag: 指定标签
            """

            # 判断路径是否存在
            if not os.path.exists(target_path):
                self._print("Directory does not exist!")
                return

            parent_name = os.path.basename(target_path) if not target_tag else target_tag

            # 遍历目录下的Git Repository
            for i in os.listdir(target_path):
                sub_path = os.path.join(target_path, i)
                sub_name = os.path.basename(sub_path)

                # sub_path类型为目录, 并且存在.git且为目录, 视为Git Repository
                git_path = os.path.join(sub_path, ".git")
                if os.path.isdir(sub_path):
                    sub_name = exist_node(sub_name)
                    self.tree.create_node(sub_name, sub_name, parent=parent_name)

                    if os.path.exists(git_path) and os.path.isdir(git_path):
                        start_info = "Starting: %(sub_dir)s %(ph)s" % {'sub_dir': i, 'ph': "." * (80 - len(i) - 1)}
                        self._print(start_info)
                        os.system(self.unix_shell % sub_path)
                        self._print()
                    else:
                        process_target_path(sub_path, sub_name)

        if isinstance(self.directory, basestring):
            build_tree(self.directory)
            process_target_path(self.directory)
            report_tree(self.directory)
        elif isinstance(self.directory, (tuple, list)):
            for path in self.directory:
                build_tree(path)
                process_target_path(path)
                report_tree(path)
        else:
            pass

        self._print("Ok,All work is done!\r")

    def __call__(self):
        if self.log_file:
            now_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            self._print("%s %s %s" % ("=" * 35, now_time, "=" * 35))

        self.run_work()
