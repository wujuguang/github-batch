#!/usr/bin/env python3

"""批量更新指定目录下存储的所有Git Repository.
"""

import os
import shlex
import datetime
import subprocess

from treelib import Tree


class GitTool:
    def __init__(self, parent_path, shells, build_tree=False, log=None):
        """初始化操作目录, 操作命令.

            :parameter parent_path: 操作目录
            :parameter shells: 执行shell, 其中{path}为仓库路径占位符
            :parameter build_tree: 是否生成树形导航
            :parameter log: log文件
        """

        self._directory = parent_path
        self._unix_shell = shells
        self._log_file = log
        self._tree = None
        self._build_tree = build_tree

    @property
    def build_tree(self):
        return self._build_tree

    @build_tree.setter
    def build_tree(self, value):
        self._build_tree = value

    def _print(self, info=''):
        if self._log_file:
            with open(self._log_file, 'a', encoding='utf-8') as f:
                f.write(info + '\n')
        else:
            print(info)

    def run_work(self):
        """对指定的目录, 执行指定的操作命令.
        """

        # 如果传入日志路径不存在则创建
        if self._log_file:
            dir_name = os.path.dirname(self._log_file)
            if dir_name:
                os.makedirs(dir_name, exist_ok=True)

        def build_tree(target_path):
            """创建树节点.

                :param target_path: 指定目录
            """

            if not self._build_tree:
                return

            self._tree = Tree()
            parent_name = os.path.basename(target_path.rstrip(os.path.sep)) \
                or target_path
            self._tree.create_node(parent_name, parent_name)

        def exist_node(sub_name):
            """指定节点是否存在, 若存在则返回一个未占用的名字.

                :param sub_name: 指定节点.
            """

            if not self._build_tree:
                return sub_name

            orig, nid = sub_name, 1
            while self._tree.contains(sub_name):
                sub_name = f'{orig}_{nid}'
                nid += 1

            return sub_name

        def report_tree(target_path, out_file=True):
            """输出文件树.

                :param target_path: 根目录路径.
                :param out_file: 是否写入文件, False 时打印到屏幕.
            """

            if not self._build_tree:
                return

            if out_file:
                report_file = os.path.basename(target_path.strip(os.path.sep))
                self._tree.save2file(f'{report_file}.txt')
            else:
                self._tree.show()

        def process_target_path(target_path, target_tag=None, _seen=None):
            """对指定目录执行操作.

                :param target_path: 指定目录
                :param target_tag: 指定标签
                :param _seen: 内部使用, 记录已访问的真实路径以避免软链环
            """

            # 判断路径是否存在
            if not os.path.exists(target_path):
                self._print(f'Directory does not exist: {target_path}')
                return

            # 软链/挂载环检测
            if _seen is None:
                _seen = set()
            real_path = os.path.realpath(target_path)
            if real_path in _seen:
                return
            _seen = _seen | {real_path}

            parent_name = target_tag or (
                os.path.basename(target_path.rstrip(os.path.sep))
                or target_path)

            # 遍历目录下的Git Repository
            try:
                entries = os.listdir(target_path)
            except OSError as exc:
                self._print(f'Skip unreadable directory {target_path}: {exc}')
                return

            for i in entries:
                sub_path = os.path.join(target_path, i)
                sub_name = os.path.basename(sub_path)

                # sub_path类型为目录, 且存在.git(目录或文件), 视为Git Repository
                # .git为文件时对应submodule或worktree
                git_path = os.path.join(sub_path, ".git")
                if os.path.isdir(sub_path):
                    sub_name = exist_node(sub_name)
                    if self._build_tree:
                        self._tree.create_node(
                            sub_name,
                            sub_name,
                            parent=parent_name)

                    if os.path.exists(git_path):
                        pad = max(0, 80 - 10 - len(i) - 1)
                        start_info = f"Starting: {i} {'.' * pad}"
                        self._print(start_info)
                        cmd = self._unix_shell.replace('{path}',
                                                      shlex.quote(sub_path))
                        result = subprocess.run(cmd, shell=True)
                        if result.returncode != 0:
                            self._print(
                                f"Failed: {i} (exit {result.returncode})")
                        self._print()
                    else:
                        process_target_path(sub_path, sub_name, _seen)

        if isinstance(self._directory, str):
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

        self._print("Ok, All work is done!")

    def __call__(self):
        if self._log_file:
            now_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            self._print(f"{'=' * 35} {now_time} {'=' * 35}")

        self.run_work()
