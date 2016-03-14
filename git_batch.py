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
    def __init__(self, parent_path, shells, build_tree=False, log=None):
        """初始化操作目录, 操作命令.

            :parameter parent_path: 操作目录
            :parameter shells:　执行shell
            :parameter build_tree: 是否生成树形导航
            :parameter log: log文件
        """

        self._directory = parent_path
        self._unix_shell = shells
        self._log_file = log
        self._tree = None
        self._build_tree = build_tree

    def get_build_tree(self):
        return self._build_tree

    def set_build_tree(self, value):
        self._build_tree = value

    build_tree = property(get_build_tree, set_build_tree)

    def _print(self, info=''):
        if self._log_file:
            os.system("echo %s >> %s" % (info, self._log_file))
        else:
            print(info)

    def run_work(self):
        """对指定的操作目录, 执行指定的操作命令.
        """

        # 如果传入日志路径不存在则创建
        if self._log_file:
            dir_name = os.path.dirname(self._log_file)
            if not os.path.exists(dir_name):
                os.makedirs(dir_name)
            if not os.path.exists(self._log_file):
                os.mknod(self._log_file)

        def build_tree(target_path):
            """创建树节点.

                :param target_path: 指定目录
            """

            if not self._build_tree:
                return

            self._tree = Tree()
            parent_name = os.path.basename(target_path)
            self._tree.create_node(parent_name, parent_name)

        def exist_node(sub_name):
            """指定节点是否存在.

                :param sub_name: 指定节点.
            """

            if not self._build_tree:
                return sub_name

            nid = 0
            while self._tree.contains(sub_name):
                sub_name = '_'.join((sub_name, str(nid)))
                nid += 1

            return sub_name

        def report_tree(target_path, out_file=True):
            """输出文件树.

                :param target_path: 指定节点.
                :param out_file: 指定节点.
            """

            if not self._build_tree:
                return

            if out_file:
                report_file = os.path.basename(target_path.strip(os.path.sep))
                self._tree.save2file('%s.txt' % report_file)
            else:
                self._tree.show()

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
                    if self._build_tree:
                        self._tree.create_node(sub_name, sub_name, parent=parent_name)

                    if os.path.exists(git_path) and os.path.isdir(git_path):
                        start_info = "Starting: %(sub_dir)s %(ph)s" % {'sub_dir': i, 'ph': "." * (80 - len(i) - 1)}
                        self._print(start_info)
                        os.system(self._unix_shell % sub_path)
                        self._print()
                    else:
                        process_target_path(sub_path, sub_name)

        if isinstance(self._directory, basestring):
            build_tree(self._directory)
            process_target_path(self._directory)
            report_tree(self._directory)
        elif isinstance(self._directory, (tuple, list)):
            for path in self._directory:
                build_tree(path)
                process_target_path(path)
                report_tree(path)
        else:
            pass

        self._print("Ok,All work is done!\r")

    def __call__(self):
        if self._log_file:
            now_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            self._print("%s %s %s" % ("=" * 35, now_time, "=" * 35))

        self.run_work()
